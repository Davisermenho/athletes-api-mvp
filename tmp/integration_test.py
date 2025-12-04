"""Integration test: POST an athlete to the running app and verify DB persistence.

This script uses requests to call the local API and psycopg2 to query the DB.
Run with `PYTHONPATH=. python tmp/integration_test.py` after loading .env.
"""
import os
import time
import json

import requests

from datetime import datetime

DB_URL = os.getenv("DATABASE_URL")
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")


def post_athlete(payload):
    url = f"{API_URL}/athletes"
    r = requests.post(url, json=payload, timeout=10)
    r.raise_for_status()
    return r.json()


def query_db(athlete_id):
    # Query via API endpoint instead of DB driver to avoid needing psycopg2 in this environment.
    url = f"{API_URL}/_debug/athletes/{athlete_id}"
    r = requests.get(url, timeout=10)
    if r.status_code == 404:
        return None
    r.raise_for_status()
    return r.json()


def run():
    example = {
        "athlete_id": f"it_{int(time.time())}",
        "full_name": "Integration Test",
        "main_attack_position": "armadora_central",
    }

    print("Posting example to API:", example)
    resp = post_athlete(example)
    print("API response:", json.dumps(resp, default=str, indent=2))

    print("Querying API for persisted row...")
    row = query_db(example["athlete_id"])
    if not row:
        raise RuntimeError("Row not found after POST via API")
    print("Found via API:", row)


if __name__ == "__main__":
    if not DB_URL:
        print("Error: DATABASE_URL not set in environment. Load .env first.")
        raise SystemExit(1)
    run()
