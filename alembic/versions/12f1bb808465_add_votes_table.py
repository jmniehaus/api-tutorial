"""add votes table

Revision ID: 12f1bb808465
Revises: 44fa8ed59aba
Create Date: 2026-09-29 13:27:13.572374

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '12f1bb808465'
down_revision: Union[str, Sequence[str], None] = '44fa8ed59aba'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "votes",
        sa.Column(
            "user_id",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            primary_key=True,
        ),
        sa.Column(
            "post_id",
            sa.Integer(),
            sa.ForeignKey("posts.id", ondelete="CASCADE"),
            primary_key=True,
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("votes")