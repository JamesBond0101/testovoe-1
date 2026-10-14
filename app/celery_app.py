from celery import Celery

from app.core.config import Settings, get_settings


def create_celery_app(settings: Settings) -> Celery:
    application = Celery(
        "deribit_price_service",
        broker=str(settings.celery_broker_url),
        include=["app.tasks.price_tasks"],
    )

    application.conf.update(
        broker_connection_retry_on_startup=True,
        beat_schedule={
            "collect-prices-every-minute": {
                "task": "prices.collect",
                "schedule": float(
                    settings.collection_interval_seconds
                ),
                "options": {
                    "expires": settings.collection_interval_seconds,
                },
            },
        },
        timezone="UTC",
        enable_utc=True,
        task_ignore_result=True,
        task_serializer="json",
        accept_content=["json"],
    )

    return application


celery_app = create_celery_app(get_settings())