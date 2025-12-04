# Stack Tecnológica (resumo)

- Linguagem: Python 3.12
- Framework web: FastAPI
- ASGI server: Uvicorn
- ORM / Migrations: SQLAlchemy + Alembic
- Banco de dados: PostgreSQL (versão alvo: 15)
- Container: Docker (image baseada em python:3.12-slim)
- Orquestração local: docker compose
- CI: GitHub Actions (workflows em `.github/workflows/`)
- Testes: pytest
- Lint/format: black, isort, flake8
- Observability: Sentry (opcional; configure via `SENTRY_DSN` secret)

Observações:
- Não incluir segredos em arquivos versionados; use secrets do provider (GitHub Actions Secrets, Render, etc.).
- Migrations devem ser executadas manualmente contra um DB de teste antes de promover para produção.
