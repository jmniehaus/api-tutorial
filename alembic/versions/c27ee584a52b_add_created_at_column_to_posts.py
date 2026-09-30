"""add created_at column to posts

Revision ID: c27ee584a52b
Revises: 571ebc3a2893
Create Date: 2026-09-29 13:00:39.265447

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'c27ee584a52b'
down_revision: Union[str, Sequence[str], None] = '571ebc3a2893'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "posts",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        )
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'created_at')
