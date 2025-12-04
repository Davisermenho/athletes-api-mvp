#!/usr/bin/env bash
set -euo pipefail

# Build and run the test environment (Postgres + app)
# Requires Docker and docker-compose (v2) available as `docker compose`.

docker compose -f docker-compose.test.yml up --build --remove-orphans

# Optional: test health endpoint after app is up (may fail if service not ready yet)
# Uncomment or run separately if you want an automated check.
# sleep 2
# curl -v http://localhost:10000/health
