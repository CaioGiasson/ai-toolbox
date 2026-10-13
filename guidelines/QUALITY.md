# Qualidade: Observabilidade, Testes, Documentação e Code Review

## 1. Observabilidade e Logging

- **Proibido `console.log` em produção** — usar o `Log.manager` (`src/managers/Log.manager.ts`) com tags e contexto.
- **Nunca logar dados sensíveis** — PII, tokens, credenciais e secrets fora dos logs.
- **Logs estruturados como event streams** — JSON no stdout, não arquivos gerenciados pela aplicação.
- **Métricas, tracing e APM** — desejáveis (Sentry, Datadog ou equivalente); não bloquear PR por ausência, salvo se a feature exigir SLO.

---

## 2. Testes

- **Ciclo Red → Green → Refactor** — escrever o teste antes ou junto da implementação.
- **Priorizar testes de useCases, middlewares, regras de autorização e DTOs públicos** — cobrir happy paths e edge cases.
- **Factories para testes** — `tests/factories/*.factory.ts` com valores padrão.
- **Cobertura em crons** — sem lógica de negócio sem teste.
- **PR sem testes não pode ser mergeada** — exceção apenas quando task de testes separada é criada e linkada:

```ts
// TODO: Implementar testes - https://github.com/org/repo/issues/123
```

- **Evidência de testes na PR** — colocar evidências dos testes locais na descrição da PR.

---

## 3. Documentação

- **OpenAPI por rota** — toda nova rota atualiza `docs/openapi.yaml`, em português.
- **Arquivos `.http`** — toda nova rota cria um arquivo rest client em `requests/`, organizado por domínio.
- **Lições em `tasks/lessons.md`** — bug não óbvio ou incidente operacional: sintoma → causa → fix/prevenção.
- **Regras de negócio em `/docs`** — toda evolução de regra documentada na pasta `/docs`.
- **JSDoc em services e métodos públicos** — documentar parâmetros, retornos e propósito.
- **ADRs em `/docs/adr/`** — documentar decisões arquiteturais com contexto, opções e motivo da escolha.
- **OpenAPI sincronizado com o código.**

---

## 4. Code Review

- **PRs pequenas e focadas** — idealmente < 500 linhas de diff.
- **Review antes do merge** — bloqueantes e importantes corrigidos na própria PR, comentário de pós-review e label `Reviewed`; CI verde.
- **Níveis de achado** — 🔴 bloqueante · 🟡 importante · 🟢 sugestão (ver `GUIA_REVISAO_PR_GERAL.md`).
- **Descrever o "porquê"** — o autor explica o motivo da mudança, não apenas o que mudou.
- **Sempre linkar com issue** — PR sempre vinculada a uma issue no board do GitHub (`Closes #N`). Sem tarefas ad-hoc.
- **Checklist do reviewer** — correção, legibilidade, performance, segurança, testes.
- **PR templates** — usar checklists via GitHub PR templates.
