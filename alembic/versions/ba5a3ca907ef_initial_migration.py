"""Initial migration

Revision ID: ba5a3ca907ef
Revises:
Create Date: 2026-10-14 19:16:50.273564

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


revision: str = "ba5a3ca907ef"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "price_records",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column(
            "ticker",
            sa.Enum(
                "btc_usd",
                "eth_usd",
                name="ticker_enum",
                native_enum=False,
                create_constraint=True,
            ),
            nullable=False,
        ),
        sa.Column(
            "price",
            sa.Numeric(precision=20, scale=8),
            nullable=False,
        ),
        sa.Column("timestamp", sa.BigInteger(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "ticker",
            "timestamp",
            name="uq_price_records_ticker_timestamp",
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("price_records")
