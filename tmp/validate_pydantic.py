"""Small script to validate an example against Pydantic models.

This script is intentionally read-only and does not modify the repo.
Run locally with your environment activated (do NOT commit virtualenvs).

Example:
  python tmp/validate_pydantic.py
"""

from datetime import date

from app.schemas import AthleteCreate

example = {
    "athlete_id": "A1",
    "full_name": "Maria Silva",
    "main_attack_position": "armadora_central",
}


def run():
    obj = AthleteCreate(**example)
    print("Pydantic validation succeeded. Instance:")
    # Support both pydantic v2 (model_dump) and v1 (dict())
    try:
        data = obj.model_dump()
    except Exception:
        data = obj.dict()
    print(data)


if __name__ == "__main__":
    run()
