-- SQL: create_table_athletes.sql
-- Cria a tabela `athletes` com campos essenciais e índices recomendados.
-- Usa extensão pgcrypto para gerar UUIDs (Supabase/PG comum suporta).
-- SQL: create_table_athletes.sql
-- Fonte de verdade para o schema de atletas do MVP.
-- Uso recomendado: rode este arquivo em um banco Postgres de desenvolvimento.
-- Observação sobre UUIDs: este script usa pgcrypto's gen_random_uuid();
-- alternativa: use uuid-ossp e uuid_generate_v4() se preferir.

-- Habilita extensão necessária (pgcrypto) — é um comentário-sugestão,
-- execute manualmente em ambientes gerenciados se não tiver permissões.
CREATE EXTENSION IF NOT EXISTS pgcrypto;

/*
  Valores permitidos para posições (padronizados).
  Se detectar grafias alternativas em dados históricos (ex: "latera_direita")
  documente e normaliza antes de aplicar transformações; preferimos
  "lateral_direita" como valor padrão.
*/

CREATE TABLE IF NOT EXISTS athletes (
    id BIGSERIAL PRIMARY KEY,
    athlete_id TEXT NOT NULL UNIQUE,
    row_uuid UUID NOT NULL DEFAULT gen_random_uuid(),
    full_name TEXT NOT NULL,
    nickname TEXT,
    birth_date DATE,
    age_display TEXT,
    category TEXT,
    main_attack_position TEXT,
    secondary_attack_position TEXT,
    main_defensive_position TEXT,
    secondary_defensive_position TEXT,
    jersey_number INTEGER,
    date_joined DATE,
    date_left DATE,
    active_flag BOOLEAN NOT NULL DEFAULT true,
    height_cm INTEGER,
    weight_kg NUMERIC(6,2),
    medical_notes TEXT,
    social_notes TEXT,
    physical_notes TEXT,
    mental_notes TEXT,
    external_reference TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    last_sync_at TIMESTAMPTZ,

    -- CHECK constraints to enforce allowed enum values for positions
    CONSTRAINT chk_main_attack_position CHECK (main_attack_position IS NULL OR main_attack_position IN ('armadora_central','lateral_esquerda','lateral_direita','ponta_esquerda','ponta_direita','pivo')),
    CONSTRAINT chk_secondary_attack_position CHECK (secondary_attack_position IS NULL OR secondary_attack_position IN ('central','lateral_esquerda','lateral_direita','ponta_esquerda','ponta_direita','pivo')),
    CONSTRAINT chk_main_defensive_position CHECK (main_defensive_position IS NULL OR main_defensive_position IN ('1_defensora','2_defensora','defensora_base','goleira','defensora_avancada')),
    CONSTRAINT chk_secondary_defensive_position CHECK (secondary_defensive_position IS NULL OR secondary_defensive_position IN ('1_defensora','2_defensora','defensora_base','goleira','defensora_avancada')),
    CONSTRAINT chk_jersey_number CHECK (jersey_number IS NULL OR jersey_number >= 0),
    CONSTRAINT chk_height_cm CHECK (height_cm IS NULL OR height_cm >= 0),
    CONSTRAINT chk_weight_kg CHECK (weight_kg IS NULL OR weight_kg >= 0)
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_athletes_athlete_id ON athletes (athlete_id);
CREATE INDEX IF NOT EXISTS idx_athletes_row_uuid ON athletes (row_uuid);
CREATE INDEX IF NOT EXISTS idx_athletes_created_at ON athletes (created_at);

-- Trigger function to update updated_at on row modification
CREATE OR REPLACE FUNCTION touch_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_touch_updated_at ON athletes;
CREATE TRIGGER trg_touch_updated_at
BEFORE UPDATE ON athletes
FOR EACH ROW
EXECUTE PROCEDURE touch_updated_at();

-- Comments/descriptions
COMMENT ON TABLE athletes IS 'Tabela principal de atletas para o MVP; fontes: MANUAL CANONICO; schema gerado a partir do cabeçalho fornecido.';
COMMENT ON COLUMN athletes.row_uuid IS 'UUID gerado usando pgcrypto.gen_random_uuid(); alternativa: uuid-ossp/uuid_generate_v4()';
COMMENT ON COLUMN athletes.athlete_id IS 'Identificador de negócio do atleta (externo), único e não nulo.';
COMMENT ON COLUMN athletes.full_name IS 'Nome completo do atleta (obrigatório).';

-- Observação de manutenção:
--  - Reveja constraints NOT NULL e CHECKs conforme regras de negócio.
--  - Para enums (category, positions) considere criar tipos ou tabelas de referência.

