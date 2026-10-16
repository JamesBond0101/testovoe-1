# Deribit Price Service

## Разворачивание через Docker Compose

Нужны Docker и Docker Compose. Из корня репозитория:

```bash
cp .env.example .env
docker compose up -d --build
docker compose run --rm web alembic upgrade head
```

На Windows PowerShell:

```powershell
Copy-Item .env.example .env
docker compose up -d --build
docker compose run --rm web alembic upgrade head
```

Проверка:

- API: [http://localhost:8000/health](http://localhost:8000/health)
- Swagger: [http://localhost:8000/docs](http://localhost:8000/docs)

Остановка:

```bash
docker compose down
```

После изменения `.env` контейнеры нужно пересоздать:

```bash
docker compose up -d --force-recreate
```

## Design decisions

### Отдельные процессы для API, Worker и Beat

Задание требует Celery, поэтому двух контейнеров недостаточно. FastAPI только читает данные. Сбор цен выполняется в Worker, расписание — в Beat, брокер — Redis. Так API не блокируется HTTP-запросами к бирже, а падение Worker не роняет HTTP-сервер.

### aiohttp только как HTTP-клиент

Внешнее API написано на FastAPI, как требует задание. aiohttp используется исключительно для запросов к Deribit. Публичный метод `GET /public/get_index_price` не требует авторизации и возвращает `result.index_price`.

### Слой repository / service

SQL не попадает в роуты и в Celery-задачу напрямую. `PriceRepository` работает с `AsyncSession`, `PriceService` готовит ответы API и проверяет бизнес-правила (нет последней цены, некорректный диапазон дат). Задача Celery вызывает репозиторий для записи.

### Сессия БД в FastAPI и в Celery создаётся по-разному

У FastAPI engine живёт в `lifespan` и отдаёт сессию через `Depends`. Celery — отдельный процесс без `Request` и `app.state`. Worker создаёт engine внутри `asyncio.run()`, делает `commit()` и закрывает engine в `finally`. Это безопаснее, чем пытаться переиспользовать FastAPI `get_db()`.

### Celery-задача синхронная, внутри неё запускается asyncio

У Celery нет полноценного нативного выполнения `async def`. Точка входа — обычная функция `prices_collect()`, которая вызывает `asyncio.run(collect_prices())`. Запросы к Deribit для `btc_usd` и `eth_usd` идут параллельно через `asyncio.gather(..., return_exceptions=True)`: ошибка одного тикера не отменяет сохранение второго.

### `task_ignore_result=True`

Результат Celery в Redis не нужен. Цены сохраняются в PostgreSQL, FastAPI читает их оттуда. `expires` у задачи равен интервалу сбора, чтобы при остановленном Worker не копилась просроченная «текущая» цена.

### Цена хранится как `NUMERIC`, не `float`

Index price — финансовое значение. В модели используется `Decimal` и PostgreSQL `NUMERIC(20, 8)`. Из JSON Deribit цена берётся через `Decimal(str(...))`, чтобы не тащить двоичную погрешность `float`.

### UNIX timestamp задаёт приложение

Метод Deribit не возвращает время снимка. Колонка `timestamp` — `BIGINT` без `DEFAULT now()`. Значение вычисляется в задаче как `int(time.time())` один раз на оба тикера, чтобы пара `btc_usd`/`eth_usd` относилась к одному циклу сбора. Уникальность `(ticker, timestamp)` защищает от дублей.

### Тикер — `Enum`

Допустимы только `btc_usd` и `eth_usd`. Enum переиспользуется в модели, клиенте Deribit и query-параметре FastAPI. Неизвестный тикер отклоняется на уровне валидации API.

### Фильтр по дате — диапазон UNIX timestamp

Задание не уточняет, что считать «фильтром по дате». Реализован диапазон `date_from` / `date_to` в секундах: это совпадает с форматом хранения и не требует дополнительных преобразований часовых поясов.

### Пагинация списка цен

История растёт каждую минуту. Для `GET /prices` добавлены необязательные `page` и `page_size`, чтобы ответ не раздувался бесконечно. Параметр `ticker` при этом остаётся обязательным.

### Настройки через pydantic-settings

Конфиг типизирован, обязательные DSN проверяются при старте, объект `Settings` иммутабелен. Значения читаются из переменных с префиксом `APP_`. Глобального изменяемого состояния нет: доступ идёт через `get_settings()`.

### Alembic в корне проекта

Миграции — часть инфраструктуры репозитория, а не пакет `app`. Команда запускается как `alembic upgrade head` из рабочей директории контейнера `/code`.
