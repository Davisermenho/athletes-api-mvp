"""Alembic migration skeleton to create the athletes table.

NOTE: This file is a skeleton. Review the SQL and adjust paths or revision
IDs to match your Alembic setup before running `alembic upgrade`.
"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '20251204_create_athletes_table'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # This reads the SQL file at repository path `sql/create_table_athletes.sql`.
    # Depending on how you run Alembic, you may need to adjust the relative path.
    with open('sql/create_table_athletes.sql', 'r', encoding='utf-8') as f:
        sql = f.read()
    op.execute(sql)


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS athletes CASCADE;")
