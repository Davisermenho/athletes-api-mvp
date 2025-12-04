-- SQL: create_table_athletes.sql
-- Cria a tabela `athletes` com campos essenciais e índices recomendados.
-- Usa extensão pgcrypto para gerar UUIDs (Supabase/PG comum suporta).

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

-- Índices recomendados
CREATE INDEX IF NOT EXISTS idx_athletes_created_at ON athletes (created_at);
CREATE INDEX IF NOT EXISTS idx_athletes_row_uuid ON athletes (row_uuid);
CREATE INDEX IF NOT EXISTS idx_athletes_country_code ON athletes (country_code);
CREATE INDEX IF NOT EXISTS idx_athletes_lower_email ON athletes ((lower(email)));

-- Trigger auxiliar para manter `updated_at`
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

-- Observações:
--  - Ajuste campos NOT NULL / CHECKs conforme MANUAL CANÔNICO COMPLETO.md.
--  - Para enums fortes, crie tipos SQL ou tabelas referenciadas.
