"""merge heads for athletes table

Revision ID: merge_0001_20251204_athletes_merge
Revises: 0001_create_athletes_table, 20251204_create_athletes_table
Create Date: 2025-12-04 00:30:00.000000
"""

# merge-only revision: no op imports required

# revision identifiers, used by Alembic.
revision = "merge_0001_20251204"
down_revision = ("0001_create_athletes_table", "20251204_create_athletes_table")
branch_labels = None
depends_on = None


def upgrade() -> None:
    # This is a merge revision to unify two heads. No schema changes required.
    pass


def downgrade() -> None:
    # Downgrade is not supported for merge-only revisions.
    pass
