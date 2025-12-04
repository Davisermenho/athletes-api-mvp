# Changelog

All notable changes to this project will be documented in this file.

## Unreleased

- feat: add athlete schema (SQL, JSON Schema, Pydantic models) and OpenAPI component
- feat: implement `POST /athletes` upsert endpoint
- test: add tests for debug routes and CI test harness
- ci: consolidated GitHub Actions workflow (lint → test → production-sim)
- ci: fixed format/isort/flake8 issues and made DB env check lazy for tests
- infra: added Docker test compose and CI-friendly test image
- ops: enabled branch protection on `main` (require 1 approving review + `CI` status check; admins enforced)

## 0.1.0 - 2025-12-04

- Initial MVP release artifacts (schema + basic endpoints + tests)
