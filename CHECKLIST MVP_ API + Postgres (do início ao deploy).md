**CHECKLIST MVP: API \+ Postgres (do início ao deploy)**

Fase 0 — Preparação e decisões iniciais (30–90 min) — Prioridade: Alta

*  Definir objetivo do MVP (o que o MVP deve resolver exatamente; ex.: cadastro e validação de atletas \+ logs \+ POC IA).  
*  Escolher provedor para o banco/API/hosting (recomendado inicial: Supabase para Postgres \+ Vercel para frontend).  
*  Criar conta(s) necessárias (Supabase, Vercel, GitHub).  
  Tempo estimado: 0.5–1.5h Critério de aceitação: contas criadas e informações de conexão anotadas (DB URL, API key, project id).

Fase 1 — Modelagem de dados (schema) (1–3 horas) — Prioridade: Alta

*  Definir e documentar o schema da tabela athletes (colunas, tipos, NOT NULL, UNIQUE).  
*  Criar JSON Schema para validação de payloads da API (campos obrigatórios, formatos de data, enums como category).  
*  Definir chaves naturais/identificadores (athlete\_id e row\_uuid) e timestamps (created\_at/updated\_at).  
  Tempo estimado: 1–3h Critério de aceitação: arquivo SQL e JSON Schema aprovados.

Fase 2 — Provisionamento do banco (30–60 min) — Prioridade: Alta

*  Criar projeto no Supabase (ou outro provedor escolhido).  
*  Rodar o script CREATE TABLE (criar tabela athletes \+ índices/constraints).  
*  Habilitar extensão pgvector se planejar RAG e embeddings (opcional).  
  Tempo estimado: 0.5–1h Critério de aceitação: tabela criada e acessível (pode executar SELECT).

**Antes da Fase 3 (após Fase 2):**

Criar arquivo OpenAPI (contrato) com os endpoints e exemplos de payload.  
Configurar migrations (Alembic) junto com o repositório.

**Fase 3 — Desenvolvimento da API (backend) (1–3 dias) — Prioridade: Alta**

Criar repositório Git (GitHub).  
Implementar API básica (recomendado FastAPI em Python):

1. GET /athletes (lista, paginado)  
2. GET /athletes/{athlete\_id}  
3. POST /athletes (cria/upsert)  
4. PUT /athletes/{athlete\_id} (atualiza)  
5. POST /forms/{form\_id}/responses (recebe respostas de formulário)  
6.  Adicionar GitHub Actions para rodar lint/testes.  
7.  Criar Dockerfile básico (opcional, facilita deploy).  
8.  Implementar logging estruturado e integração com Sentry.  
9.  Implementar migrations (Alembic) e rotina de seed/test data.  
10. Integrar com Postgres (SQLAlchemy / asyncpg / Supabase client) e criar camada de upsert por athlete\_id/row\_uuid.  
11. Validar payloads com Pydantic usando o JSON Schema / modelos Pydantic.  
12. Implementar logs básicos e tratamento de erros (400/422/500).

Tempo estimado: 1–3 dias Critério de aceitação: endpoints funcionando localmente; testes unitários básicos (ex.: criar/ler/atualizar atleta).

Fase 4 — Autenticação e segurança da API (2–8 horas) — Prioridade: Alta

1.  Decidir método de autenticação (JWT simple, Supabase Auth ou API keys para começo).  
2.  Implementar autenticação nas rotas que escrevem dados (POST/PUT).  
3.  Habilitar CORS restrito (origens permitidas: frontend URL e Apps Script URL se usar).  
4.  Não expor credenciais no código; usar variáveis de ambiente / Secret Manager.  
5.  Decidir e documentar mecanismo de autenticação (Supabase Auth ou JWT).  
6.  Criar rota de health check e configurar CORS estrito.

Tempo estimado: 2–8h Critério de aceitação: apenas requests autenticados conseguem criar/atualizar.

**Fase 5 — Frontend leve / Dashboard (1–5 dias) — Prioridade: Média-Alta**

1. Escolher abordagem: Next.js (recomendado) ou ferramenta low-code (se quer mais rápido).  
2. Implementar formulário de cadastro de atleta que chame POST /athletes.  
3. Implementar listagem e busca via GET /athletes.  
4. Implementar autenticação básica no frontend (login / token).  
   

**Tempo estimado: 1–5 dias (depende da complexidade) Critério de aceitação: usuário autentica e cria/lista atletas via UI.**

**Fase 6 — Integração com Google Sheets (opcional, para transição) (2–6 horas) — Prioridade: Média**

1. Criar Apps Script POC que, ao editar/submit na planilha, faz POST /athletes para a API.  
2.  Registrar logs na planilha (status da entrega, resposta da API, codes).  
3.  Usar Service Account ou token de API para autenticar o Apps Script (nunca colocar chaves públicas).  
4. Apps Script deve usar o contrato OpenAPI e autenticar via API key ou service account.

**Tempo estimado: 2–6h Critério de aceitação: alterações na planilha enviadas ao backend e persistidas no Postgres.**

**Fase 7 — ETL / Migração inicial de dados (2–6 horas) — Prioridade: Média**

*  Escrever script ETL (Python) idempotente que:  
  * lê a aba machine‑readable do Google Sheet (via Google Sheets API),  
  * normaliza campos (datas → YYYY‑MM‑DD, números),  
  * valida contra JSON Schema,  
  * faz upsert no Postgres (ON CONFLICT DO UPDATE).  
  *  Implementar \--dry-run e logs; processar em batches; garantir re‑rodabilidade sem duplicação.  
* Rodar migração para dados históricos (fazer em lotes e validar amostras).  
  Tempo estimado: 2–6h Critério de aceitação: dados migrados sem perda (amostra comparada entre sheet e DB).  
* 

Fase 8 — Worker / Processamento assíncrono (opcional POC) (4–16 horas)

Implementar fila/worker mínimo (Redis \+ RQ ou Celery) para processar respostas longas (ex.: IA).  
 Criar tarefa que chama LLM com prompt (POC direto) e grava processed\_responses na tabela.  
Se quiser RAG no futuro, planejar indexação e embeddings (pgvector/pinecone).  
Implementar primeiro como job leve (sem infra complexa) e medir latência/throughput. Só então decidir Celery/Redis.

Tempo estimado: 4–16h (POC direto menor) Critério de aceitação: worker processa jobs e grava resultado no DB.

Fase 9 — Testes, QA e validação (4–12 horas) — Prioridade: Alta

* Testes manuais ponta a ponta (form → API → DB → UI).  
* Testes de erro: payloads inválidos; duplicidade; datas erradas.  
* Testes automatizados básicos (unit \+ integração para endpoints críticos).  
* Testar idempotência no ETL (rodar duas vezes sem duplicados).  
  Tempo estimado: 4–12h Critério de aceitação: testes automatizados passam e testes manuais aprovados.  
* Criar staging environment e deploy pipeline; testar rollback.  
* Habilitar backups automáticos e testar restore.

Fase 10 — Deploy e operação (1–4 horas) — Prioridade: Alta

*    
* Deploy do backend (Railway/Render/Vercel Serverless) com variáveis de ambiente.  
* Deploy do frontend (Vercel/Netlify).  
* Configurar backups automáticos do Postgres (fornecidos pelo provedor) e monitoramento básico (Sentry / logs).  
* Habilitar HTTPS e revisão de permissões (IAM).  
  Tempo estimado: 1–4h Critério de aceitação: sistema disponível em URL pública e todas as rotas básicas funcionando em produção.  
* 

Fase 11 — Segurança, compliance e observability (2–8 horas) — Prioridade: Alta

* Garantir que chaves/segredos estão em Secret Manager ou variáveis de ambiente seguras.  
* Configurar roles/permissions para DB (apenas a API tem credenciais de escrita).  
* Habilitar logs de auditoria (quem criou/alterou o quê).  
* Revisar requisitos de privacidade (LGPD) e adicionar campo de consentimento no formulário.  
  Tempo estimado: 2–8h Critério de aceitação: conformidade básica verificada e logs disponíveis.  
* 

Fase 12 — Monitoramento e manutenção (contínuo)

* Configurar alertas de erro (Sentry) e monitoramento de saúde (uptime).  
* Planejar manutenção e backups periódicos.  
* Reuniões regulares para priorizar melhorias e migrar partes do Apps Script para o backend, conforme necessário.  
* Ao longo:   
  Documentar consentimento, política de retenção e como executar restore.  
* 