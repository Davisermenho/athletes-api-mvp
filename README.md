# Athletes API - MVP (skeleton)

Rápido esqueleto FastAPI para desenvolvimento local.

Run locally:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Docker:

```bash
docker build -t athletes-api .
docker run -p 8000:8000 athletes-api
```

Endpoints:

- `GET /` — root
- `GET /health` — health check

## Debug endpoints (safe defaults)

This project exposes debug-only endpoints under the `/_debug` prefix.

- By default these endpoints are NOT included in production. To enable them:
	- Set `ALLOW_DEBUG_ENDPOINTS=1` and `APP_ENV=development` in your environment (local dev).
	- The debug router will be mounted at `/_debug` (for example `GET /_debug/athletes/{athlete_id}`).

- If you need debug/admin endpoints in staging/ops, set `ALLOW_DEBUG_ENDPOINTS=1` and configure
	`ADMIN_API_KEY`. In that case debug endpoints will require the header `x-admin-api-key: <ADMIN_API_KEY>`.
	Additionally, ensure TLS and network ACLs are in place to protect these endpoints in non-development environments.

- Production (`APP_ENV=production`) will never include the debug router even if `ALLOW_DEBUG_ENDPOINTS` is set.

---

## Desenvolvimento local — ambiente isolado e execução de testes

Siga estes passos para criar um ambiente Python isolado, instalar dependências e executar os testes localmente (mesmo fluxo que o CI usa):

1) Criar e ativar um virtual environment

```bash
# preferível: usar o mesmo binário Python do projeto (ex: python3)
python3 -m venv .venv
source .venv/bin/activate
python --version
```

Se `python -m venv` falhar (por exemplo em imagens mínimas), você pode instalar `virtualenv` no modo usuário e criar o ambiente:

```bash
python3 -m pip install --user virtualenv
python3 -m virtualenv .venv
source .venv/bin/activate
```

Observação: em Debian/Ubuntu pode ser necessário instalar `python3-venv`:

```bash
sudo apt update && sudo apt install -y python3-venv
```

2) Instalar dependências (runtime + dev)

```bash
# dentro do venv
python -m pip install --upgrade pip
python -m pip install -r requirements.txt -r requirements-dev.txt
```

Se você quiser apenas rodar os testes rapidamente, instale ao menos `pytest`:

```bash
python -m pip install -r requirements-dev.txt
```

3) Rodar os testes

```bash
# usa o Python do venv para garantir isolamento
python -m pytest -q
```

4) Execução dos testes de integração / debug endpoints

- Para permitir endpoints de debug locais (montados em `/_debug`), exporte as variáveis de ambiente antes de rodar o app/testes:

```bash
export ALLOW_DEBUG_ENDPOINTS=1
export APP_ENV=development
# (opcional) se quiser proteger em staging, defina ADMIN_API_KEY
export ADMIN_API_KEY="sua-chave-secreta"
```

5) Notas sobre CI

- O workflow GitHub Actions incluído (`.github/workflows/ci.yml`) instala dependências e roda `pytest`.
- Existe um job `prod-check` que simula `APP_ENV=production` e `ALLOW_DEBUG_ENDPOINTS=1` para garantir que os endpoints de debug não estejam montados em produção.

6) Alternativa com Docker

- Se preferir isolar tudo em container (recomendado para reproduzir o CI), posso adicionar um `Dockerfile` e `docker-compose.test.yml` que instale as dependências e execute os testes dentro de um container.

7) Boas práticas

- Não habilite `ALLOW_DEBUG_ENDPOINTS` em produção.
- Proteja qualquer rota administrativa (staging/prod) com `ADMIN_API_KEY`, TLS e regras de rede.
- Mantenha `.venv/` em `.gitignore` para não comitar artefatos do ambiente local.
