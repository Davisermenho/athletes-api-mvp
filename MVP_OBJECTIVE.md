# MVP - Objetivo e Critérios de Aceitação (Fase 0)

Resumo do objetivo
- Construir um MVP que permita cadastro e validação de atletas via API + Postgres, com logs de importação/erros e POC de processamento por IA (opcional). A arquitetura segue as decisões em STACK TECNOLÓGICA.md e ARQUITETURA FINAL DO SISTEMA.md e aplica as regras do MANUAL CANÔNICO COMPLETO.md.

Escopo mínimo (Fase 0 → entregáveis desta fase)
1. Definir e documentar o objetivo do MVP.  
2. Escolher e criar as contas necessárias (Supabase, Vercel, GitHub).  
3. Criar `.env.example` com variáveis necessárias (feito).  
4. Acordar qual método de autenticação usar (Supabase Auth recomendado ou JWT).  
5. Reunir as informações de conexão: DB URL, Supabase URLs/keys, domínio do frontend, repo GitHub.

Critérios de aceitação da Fase 0
- Contas criadas: Supabase, Vercel (ou outro host), GitHub.  
- `.env.example` presente no repositório.  
- Método de autenticação decidido e documentado.  
- Lista de valores/credenciais anotada (podem ser placeholders no repositório), para que eu gere os próximos artefatos.

Checklist rápido (o que você deve executar agora)
- [ ] Criar projeto no Supabase (ou confirmar provedor escolhido).  
- [ ] Criar projeto/site no Vercel (ou confirmar host do frontend).  
- [ ] Criar repositório no GitHub (privado) e adicionar `.env.example`.  
- [ ] Me informar qual método de auth prefere: "Supabase Auth" ou "JWT custom".  
- [ ] Copiar/colar aqui (ou me dar permissão) os valores necessários em forma de placeholders (não envie segredos reais em chat público).

Próximo passo após a Fase 0
- Eu gero OpenAPI spec + SQL CREATE TABLE + Alembic migration inicial e scaffold do FastAPI (Fase 1→3) com base nas decisões tomadas aqui.

Notas de segurança
- Nunca cole chaves secretas em chats públicos. Use placeholders e só grave valores reais como segredos no provedor (Supabase, Vercel, GitHub Secrets).