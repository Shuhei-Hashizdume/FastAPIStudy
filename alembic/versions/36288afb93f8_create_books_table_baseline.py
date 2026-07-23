"""create books table baseline

Revision ID: 36288afb93f8
Revises:
Create Date: 2026-07-23 18:48:06.717290

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "36288afb93f8"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "books",
        sa.Column(
            "book_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column("title", sa.String(), nullable=True),
        sa.Column("author", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("book_id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("books")
