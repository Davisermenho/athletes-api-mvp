import importlib

from fastapi.testclient import TestClient


def _make_client(monkeypatch, env_overrides=None):
    """Set environment, monkeypatch DB helper, reload app and return TestClient."""
    env_overrides = env_overrides or {}
    # apply env overrides
    for k, v in env_overrides.items():
        monkeypatch.setenv(k, v)

    # Ensure the DB helper used by debug route returns a predictable value
    import app.db as dbmod

    def _fake_get(athlete_id: str):
        return {
            "athlete_id": athlete_id,
            "row_uuid": "00000000-0000-0000-0000-000000000000",
            "full_name": "Test Athlete",
            "main_attack_position": None,
            "nickname": None,
            "birth_date": None,
            "age_display": None,
            "category": None,
            "secondary_attack_position": None,
            "main_defensive_position": None,
            "secondary_defensive_position": None,
            "jersey_number": None,
            "date_joined": None,
            "date_left": None,
            "active_flag": True,
            "height_cm": None,
            "weight_kg": None,
            "medical_notes": None,
            "social_notes": None,
            "physical_notes": None,
            "mental_notes": None,
            "external_reference": None,
            "created_at": None,
            "updated_at": None,
            "last_sync_at": None,
            "id": 1,
        }

    monkeypatch.setattr(dbmod, "get_athlete_by_athlete_id", _fake_get, raising=False)

    # Reload modules to pick up environment changes and router mounting
    import app.main as am

    importlib.reload(am)
    return TestClient(am.app)


def test_debug_route_included_in_development(monkeypatch):
    client = _make_client(
        monkeypatch,
        {
            "ALLOW_DEBUG_ENDPOINTS": "1",
            "APP_ENV": "development",
        },
    )
    r = client.get("/_debug/athletes/test123")
    assert r.status_code == 200
    data = r.json()
    assert data["athlete_id"] == "test123"


def test_debug_route_not_in_production(monkeypatch):
    client = _make_client(
        monkeypatch,
        {"ALLOW_DEBUG_ENDPOINTS": "1", "APP_ENV": "production"},
    )
    r = client.get("/_debug/athletes/test123")
    # route should not be mounted in production
    assert r.status_code == 404


def test_debug_route_disabled_by_default(monkeypatch):
    # No ALLOW_DEBUG_ENDPOINTS set -> should be absent
    # Ensure APP_ENV is development but ALLOW_DEBUG_ENDPOINTS is not set
    monkeypatch.delenv("ALLOW_DEBUG_ENDPOINTS", raising=False)
    client = _make_client(monkeypatch, {"APP_ENV": "development"})
    r = client.get("/_debug/athletes/test123")
    assert r.status_code == 404
