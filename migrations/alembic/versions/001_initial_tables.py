"""initial tables

Revision ID: 001
Revises:
Create Date: 2026-02-07
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "repeating_tasks",
        sa.Column("id", sa.Text, primary_key=True),
        sa.Column("name", sa.Text, nullable=False),
        sa.Column("repeats_every_days", sa.Integer, nullable=False),
        sa.Column("created_at", sa.DateTime, nullable=False),
    )

    op.create_table(
        "task_completions",
        sa.Column("id", sa.Text, primary_key=True),
        sa.Column(
            "task_id",
            sa.Text,
            sa.ForeignKey("repeating_tasks.id"),
            nullable=False,
        ),
        sa.Column("done_at", sa.DateTime, nullable=False),
    )


def downgrade() -> None:
    op.drop_table("task_completions")
    op.drop_table("repeating_tasks")
