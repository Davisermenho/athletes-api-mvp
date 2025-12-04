"""Validate a sample payload against `schemas/athlete.json` using jsonschema.

Instructions: install `jsonschema` (e.g., `pip install jsonschema`) then run
`python tmp/validate_jsonschema.py`.
"""
import json
from jsonschema import validate, ValidationError


with open("schemas/athlete.json", "r", encoding="utf-8") as f:
    schema = json.load(f)

example = {
    "athlete_id": "A1",
    "full_name": "João Santos",
    "main_attack_position": "armadora_central",
}


def run():
    try:
        validate(instance=example, schema=schema)
        print("JSON Schema validation succeeded.")
    except ValidationError as e:
        print("Validation failed:", e)


if __name__ == "__main__":
    run()
