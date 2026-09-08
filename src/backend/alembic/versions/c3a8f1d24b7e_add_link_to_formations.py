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
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if "formations" not in inspector.get_table_names():
        op.create_table(
            "formations",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("title", sa.String(), nullable=False),
            sa.Column("level", sa.String(), nullable=False),
            sa.Column("duration", sa.String(), nullable=False),
            sa.Column("payante", sa.Boolean(), nullable=False),
            sa.Column("link", sa.String(), nullable=True),
            sa.PrimaryKeyConstraint("id"),
        )
        op.create_index(op.f("ix_formations_id"), "formations", ["id"], unique=False)
        op.create_index(op.f("ix_formations_title"), "formations", ["title"], unique=False)
        return

    columns = {column["name"] for column in inspector.get_columns("formations")}
    if "link" in columns:
        return

    op.add_column("formations", sa.Column("link", sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column("formations", "link")
