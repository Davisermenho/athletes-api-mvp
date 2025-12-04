"""create athletes table

Revision ID: 0001_create_athletes_table
Revises:
Create Date: 2025-12-04 00:00:00.000000
"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "0001_create_athletes_table"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    sql = """
    CREATE EXTENSION IF NOT EXISTS pgcrypto;

    CREATE TABLE IF NOT EXISTS athletes (
        id BIGSERIAL PRIMARY KEY,
        athlete_id TEXT NOT NULL UNIQUE,
        row_uuid UUID NOT NULL DEFAULT gen_random_uuid(),
        first_name TEXT,
        last_name TEXT,
        email TEXT,
        dob DATE,
        country_code TEXT,
        category TEXT,
        gender TEXT,
        metadata JSONB DEFAULT '{}',
        created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
        updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
    );

    CREATE INDEX IF NOT EXISTS idx_athletes_created_at ON athletes (created_at);
    CREATE INDEX IF NOT EXISTS idx_athletes_row_uuid ON athletes (row_uuid);
    CREATE INDEX IF NOT EXISTS idx_athletes_country_code ON athletes (country_code);
    CREATE INDEX IF NOT EXISTS idx_athletes_lower_email ON athletes ((lower(email)));

    CREATE OR REPLACE FUNCTION trigger_set_timestamp()
    RETURNS TRIGGER AS $$
    BEGIN
      NEW.updated_at = now();
      RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;

    DROP TRIGGER IF EXISTS set_timestamp ON athletes;
    CREATE TRIGGER set_timestamp BEFORE UPDATE ON athletes
    FOR EACH ROW EXECUTE FUNCTION trigger_set_timestamp();
    """
    op.execute(sa.text(sql))


def downgrade() -> None:
    op.execute(sa.text("DROP TABLE IF EXISTS athletes CASCADE;"))
