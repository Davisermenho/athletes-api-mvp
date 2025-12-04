import os
import json
from typing import Any, Dict, Optional

from sqlalchemy import create_engine, text


DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set. Set DATABASE_URL to a Postgres URL before using the DB helpers.")


def _get_engine():
    # use SQLAlchemy sync engine (sufficient for basic upsert operations)
    return create_engine(DATABASE_URL, future=True)


def upsert_athlete(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Upsert an athlete by athlete_id. Returns the full row as a dict.

    This implementation requires a Postgres database (uses ON CONFLICT).
    """
    if "postgres" not in DATABASE_URL and "postgresql" not in DATABASE_URL:
        raise RuntimeError("upsert_athlete currently supports Postgres only (DATABASE_URL must be Postgres).")

    engine = _get_engine()

    # ensure metadata is JSON string
    metadata_val = payload.get("metadata") or {}
    if isinstance(metadata_val, str):
        metadata = metadata_val
    else:
        metadata = json.dumps(metadata_val)

    # coerce dob to ISO string if it's a date/datetime
    dob_val = payload.get("dob")
    if dob_val is not None:
        if hasattr(dob_val, "isoformat"):
            dob_param = dob_val.isoformat()
        else:
            dob_param = str(dob_val)
    else:
        dob_param = None

    sql = text(
        """
        INSERT INTO athletes (
            athlete_id, row_uuid, first_name, last_name, email, dob, country_code, category, gender, metadata
        ) VALUES (
            :athlete_id,
            COALESCE(CAST(:row_uuid AS uuid), gen_random_uuid()),
            :first_name,
            :last_name,
            :email,
            :dob,
            :country_code,
            :category,
            :gender,
            CAST(:metadata AS jsonb)
        )
        ON CONFLICT (athlete_id) DO UPDATE SET
            row_uuid = COALESCE(athletes.row_uuid, EXCLUDED.row_uuid),
            first_name = EXCLUDED.first_name,
            last_name = EXCLUDED.last_name,
            email = EXCLUDED.email,
            dob = EXCLUDED.dob,
            country_code = EXCLUDED.country_code,
            category = EXCLUDED.category,
            gender = EXCLUDED.gender,
            metadata = athletes.metadata || EXCLUDED.metadata,
            updated_at = now()
        RETURNING id, athlete_id, row_uuid, first_name, last_name, email, dob, country_code, category, gender, metadata, created_at, updated_at;
        """
    )

    params = {
        "athlete_id": payload.get("athlete_id"),
        "row_uuid": str(payload.get("row_uuid")) if payload.get("row_uuid") else None,
        "first_name": payload.get("first_name"),
        "last_name": payload.get("last_name"),
        "email": payload.get("email"),
        "dob": dob_param,
        "country_code": payload.get("country_code"),
        "category": payload.get("category"),
        "gender": payload.get("gender"),
        "metadata": metadata,
    }

    with engine.begin() as conn:
        result = conn.execute(sql, params)
        row = result.fetchone()
        if not row:
            return None
        # convert Row to dict
        keys = result.keys()
        return {k: row[idx] for idx, k in enumerate(keys)}
