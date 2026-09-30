"""add users table

Revision ID: ba5d66990963
Revises: c27ee584a52b
Create Date: 2026-09-29 13:05:40.528898

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'ba5d66990963'
down_revision: Union[str, Sequence[str], None] = 'c27ee584a52b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("email", sa.String(), nullable=False, unique=True),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")