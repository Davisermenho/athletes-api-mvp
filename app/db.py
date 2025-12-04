import os
from typing import Any, Dict, Optional

from sqlalchemy import create_engine, text


def _get_database_url() -> str:
    """Return DATABASE_URL from env or raise when actually needed.

    This defers the runtime check so importing `app.db` in tests
    (where we monkeypatch helpers) doesn't raise at import time.
    """
    url = os.getenv("DATABASE_URL")
    if not url:
        raise RuntimeError(
            "DATABASE_URL is not set. Set DATABASE_URL to a Postgres URL before using the DB helpers."
        )
    return url


def _get_engine():
    # use SQLAlchemy sync engine (sufficient for basic upsert operations)
    return create_engine(_get_database_url(), future=True)


def upsert_athlete(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Upsert an athlete by athlete_id. Returns the full row as a dict.

    This implementation requires a Postgres database (uses ON CONFLICT).
    """
    # validate DATABASE_URL when we actually perform DB work
    url = _get_database_url()
    if "postgres" not in url and "postgresql" not in url:
        raise RuntimeError(
            "upsert_athlete currently supports Postgres only (DATABASE_URL must be Postgres)."
        )

    engine = _get_engine()

    # Coerce/format a few common types
    def _date_to_iso(val):
        if val is None:
            return None
        if hasattr(val, "isoformat"):
            return val.isoformat()
        return str(val)

    sql = text(
        """
        INSERT INTO athletes (
            athlete_id, row_uuid, full_name, nickname, birth_date, age_display, category,
            main_attack_position, secondary_attack_position, main_defensive_position, secondary_defensive_position,
            jersey_number, date_joined, date_left, active_flag, height_cm, weight_kg,
            medical_notes, social_notes, physical_notes, mental_notes, external_reference
        ) VALUES (
            :athlete_id,
            COALESCE(CAST(:row_uuid AS uuid), gen_random_uuid()),
            :full_name, :nickname, :birth_date, :age_display, :category,
            :main_attack_position, :secondary_attack_position, :main_defensive_position, :secondary_defensive_position,
            :jersey_number, :date_joined, :date_left, :active_flag, :height_cm, :weight_kg,
            :medical_notes, :social_notes, :physical_notes, :mental_notes, :external_reference
        )
        ON CONFLICT (athlete_id) DO UPDATE SET
            row_uuid = COALESCE(athletes.row_uuid, EXCLUDED.row_uuid),
            full_name = EXCLUDED.full_name,
            nickname = EXCLUDED.nickname,
            birth_date = EXCLUDED.birth_date,
            age_display = EXCLUDED.age_display,
            category = EXCLUDED.category,
            main_attack_position = EXCLUDED.main_attack_position,
            secondary_attack_position = EXCLUDED.secondary_attack_position,
            main_defensive_position = EXCLUDED.main_defensive_position,
            secondary_defensive_position = EXCLUDED.secondary_defensive_position,
            jersey_number = EXCLUDED.jersey_number,
            date_joined = EXCLUDED.date_joined,
            date_left = EXCLUDED.date_left,
            active_flag = EXCLUDED.active_flag,
            height_cm = EXCLUDED.height_cm,
            weight_kg = EXCLUDED.weight_kg,
            medical_notes = EXCLUDED.medical_notes,
            social_notes = EXCLUDED.social_notes,
            physical_notes = EXCLUDED.physical_notes,
            mental_notes = EXCLUDED.mental_notes,
            external_reference = EXCLUDED.external_reference,
            updated_at = now()
        RETURNING *;
        """
    )

    params = {
        "athlete_id": payload.get("athlete_id"),
        "row_uuid": str(payload.get("row_uuid")) if payload.get("row_uuid") else None,
        "full_name": payload.get("full_name"),
        "nickname": payload.get("nickname"),
        "birth_date": _date_to_iso(
            payload.get("birth_date") or payload.get("birth_date")
        ),
        "age_display": payload.get("age_display"),
        "category": payload.get("category"),
        "main_attack_position": payload.get("main_attack_position"),
        "secondary_attack_position": payload.get("secondary_attack_position"),
        "main_defensive_position": payload.get("main_defensive_position"),
        "secondary_defensive_position": payload.get("secondary_defensive_position"),
        "jersey_number": payload.get("jersey_number"),
        "date_joined": _date_to_iso(payload.get("date_joined")),
        "date_left": _date_to_iso(payload.get("date_left")),
        "active_flag": payload.get("active_flag", True),
        "height_cm": payload.get("height_cm"),
        "weight_kg": payload.get("weight_kg"),
        "medical_notes": payload.get("medical_notes"),
        "social_notes": payload.get("social_notes"),
        "physical_notes": payload.get("physical_notes"),
        "mental_notes": payload.get("mental_notes"),
        "external_reference": payload.get("external_reference"),
    }

    with engine.begin() as conn:
        result = conn.execute(sql, params)
        row = result.fetchone()
        if not row:
            return None
        # convert Row to dict
        keys = result.keys()
        return {k: row[idx] for idx, k in enumerate(keys)}


def get_athlete_by_athlete_id(athlete_id: str) -> Optional[Dict[str, Any]]:
    """Return a single athlete row as dict by `athlete_id`, or None if not found."""
    engine = _get_engine()
    sql = text("SELECT * FROM athletes WHERE athlete_id = :athlete_id LIMIT 1")
    with engine.begin() as conn:
        result = conn.execute(sql, {"athlete_id": athlete_id})
        row = result.fetchone()
        if not row:
            return None
        keys = result.keys()
        return {k: row[idx] for idx, k in enumerate(keys)}
