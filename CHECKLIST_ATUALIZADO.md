# CHECKLIST ATUALIZADO — MVP: API + Postgres

Este arquivo é uma cópia anotada do `CHECKLIST_Version3.txt` com o status atual baseado na varredura do repositório.

Legenda: [DONE] — implementado / evidência no repositório (arquivo/path ou resultado de teste)
[ PENDING ] — não implementado ou precisa de verificação manual
[ NOT APPLICABLE ] — não se aplica ao projeto atual

---

## Fase 0 — Preparação e decisões iniciais
- Definir objetivo do MVP: [DONE] — documentação encontrada: `README.md` / `CHECKLIST_Version3.txt`.
-- Revisar decisões tecnológicas em STACK TECNOLÓGICA.md: [PENDING] — arquivo não encontrado explicitamente.
-- Criar `.env.example`: [PENDING] — não encontrado; criar manualmente com VARS mínimas.

## Fase 1 — Modelagem de dados (schema)
-- Mapear e documentar schema `athletes`: [PENDING] — migrations e alembic estão presentes (`alembic/versions/`), mas revisar conteúdo.
-- JSON Schema / Pydantic models: [DONE] parcialmente — `schemas.py` (ver `app/schemas.py` / `app/schemas.py`).

## Fase 2 — Provisionamento do banco
- Criar projeto no provedor (Supabase/RDS): [NOT APPLICABLE]
-- Rodar `CREATE TABLE`: [PENDING] — existem migrations em `alembic/` que devem ser aplicadas manualmente.

---

## Preparação antes da Fase 3
-- Gerar OpenAPI: [DONE] — FastAPI produz OpenAPI automaticamente (`/openapi` dir exists).
-- Configurar migrations (Alembic): [DONE] — `alembic.ini` and `alembic/versions/` presentes.
-- Adicionar `Dockerfile` e `docker-compose.yml` para dev local: [DONE] — `Dockerfile`, `docker-compose.test.yml`, `run-local.sh` e `CLEANUP.md` presentes.

## Fase 3 — Desenvolvimento da API
-- Implementar endpoints básicos: [DONE] — `app/routes.py` e `app/main.py` existentes (inclui `/health`).
-- Integrar com Postgres via SQLAlchemy: [DONE] — `app/db.py` usa SQLAlchemy.
-- Validar payloads com Pydantic: [DONE] — `schemas.py` presente.
-- Migrations e seed: [PENDING] — migrations existem, mas rodar/validar é manual.

## Fase 4 — Autenticação e segurança
-- Autenticação: [PENDING] — não detectado provider (Supabase) configurado.
-- Health check `/health`: [DONE] — adicionado em `app/main.py` (testado localmente: `3 passed` no suite de testes).

## Fase 5–12 (resumo)
- Frontend, importadores, ETL, workers, monitoramento: [PENDING] — referência em docs, mas não implementado integralmente.

---

## Como rodar localmente (comandos)
1. Criar venv e instalar deps:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Rodar tests:

```bash
# Recomendo criar e ativar um virtualenv, instalar deps e rodar:
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
pytest -q
```

No ambiente deste workspace executei os testes com sucesso (com `PYTHONPATH=.` ou após adicionar `pytest.ini`); resultado: `3 passed`.

Interpretação:
- Saída com `N passed` e código 0 → OK
- Falhas → revisar tracebacks e corrigir

## Como rodar migrations (manual)

- Com alembic local:

```bash
alembic upgrade head
```

- Com docker compose (exemplo):

```bash
docker compose -f docker-compose.test.yml run --rm app alembic upgrade head
```

**Aviso:** não execute migrations automaticamente no start do container — isso pode bloquear o startup e causar timeout no health check (Render).

## Deploy no Render — passos rápidos
1. Remova qualquer `PORT` fixo configurado manualmente no painel do Render.
2. No campo "Docker Command" do Render cole o conteúdo de `RENDER_DOCKER_COMMAND.txt` ou deixe o `Dockerfile` iniciar com `CMD [...]` que usa `${PORT}`.
3. Verifique logs pelo painel do Render e a rota `/health`.

---

## Evidências encontradas (paths)
- FastAPI instância: `app/main.py` (rota `/health` adicionada)
- Dockerfile: `Dockerfile` (CMD atualizado para usar `${PORT}`)
- Migrations: `alembic.ini`, `alembic/versions/`
- Requirements: `requirements.txt`, `requirements-dev.txt`
- Tests: `tests/` (`tests/test_debug_routes.py`) — suite passou localmente (`3 passed`).
- CI: `.github/workflows/ci.yml` and `.github/workflows/test.yml` (skeleton added)

Arquivos de apoio antes mantidos na branch `system` agora fazem parte da branch de trabalho atual (`work`):
- `MIGRATIONS.md` — instruções para executar migrations manualmente
- `RENDER_DOCKER_COMMAND.txt` — comando para Render
- `docker-compose.test.yml`, `run-local.sh`, `CLEANUP.md` — helpers para testes locais com Postgres
- `pytest.ini` — configura pytest para encontrar o pacote `app`

