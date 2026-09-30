"""add owner_id to posts

Revision ID: 44fa8ed59aba
Revises: ba5d66990963
Create Date: 2026-09-29 13:09:23.824354

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '44fa8ed59aba'
down_revision: Union[str, Sequence[str], None] = 'ba5d66990963'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "posts",
        sa.Column(
            "owner_id",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False
        ),
    )
    pass 


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("posts", "owner_id")
