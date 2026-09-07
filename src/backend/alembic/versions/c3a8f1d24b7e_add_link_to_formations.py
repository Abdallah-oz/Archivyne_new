"""add link to formations

Revision ID: c3a8f1d24b7e
Revises: b7c4e2d91f6a
Create Date: 2026-09-07

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c3a8f1d24b7e"
down_revision: Union[str, Sequence[str], None] = "b7c4e2d91f6a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("formations", sa.Column("link", sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column("formations", "link")
