"""create posts table

Revision ID: 571ebc3a2893
Revises: 
Create Date: 2026-09-29 12:42:47.471198

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '571ebc3a2893'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("content", sa.String(), nullable=False),
        sa.Column("published", sa.Boolean(), nullable=False, server_default=sa.true()),
    )



def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("posts")