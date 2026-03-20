# Qualidade: Observabilidade, Testes, Documentação e Code Review

## 1. Observabilidade e Logging

- **Proibido `console.log` em produção** — usar o `LogManager` (Winston) com tags e contexto.
- **Nunca logar dados sensíveis** — PII, tokens, credenciais e secrets fora dos logs.
- **Integrar com serviço de monitoramento** — Sentry, Datadog ou equivalente.
- **Logs como event streams** — stdout, não arquivos gerenciados pela aplicação.

---

## 2. Testes

- **Ciclo Red → Green → Refactor** — escrever o teste antes ou junto da implementação.
- **Priorizar testes de useCases e policies** — cobrir happy paths e edge cases.
- **Factories para testes** — `tests/factories/*.factory.ts` com valores padrão.
- **Cobertura em workers e crons** — sem lógica de negócio sem teste.
- **PR sem testes não pode ser mergeada** — exceção apenas quando task de testes separada é criada e linkada:

```ts
// TODO: Implementar testes - https://github.com/org/repo/issues/123
```

- **Evidência de testes na PR** — colocar evidências dos testes locais na descrição da PR.

---

## 3. Documentação

- **Swagger por rota** — toda nova rota atualiza o Swagger, em português.
- **Arquivos `.http`** — toda nova rota cria um arquivo rest client em `requests/`, organizado por domínio.
- **Regras de negócio em `/docs`** — toda evolução de regra documentada na pasta `/docs`.
- **JSDoc em services e métodos públicos** — documentar parâmetros, retornos e propósito.
- **ADRs em `/docs/adr/`** — documentar decisões arquiteturais com contexto, opções e motivo da escolha.
- **Runbooks em `/docs/runbooks/`** — documentação operacional para incidentes comuns. Nunca com credenciais.
- **OpenAPI/Swagger sincronizado com o código.**

---

## 4. Code Review

- **PRs pequenas e focadas** — idealmente < 400 linhas de diff.
- **Mínimo 1 aprovação antes de merge.**
- **Descrever o "porquê"** — o autor explica o motivo da mudança, não apenas o que mudou.
- **Sempre linkar com task** — PR sempre vinculada a uma task no board do GitHub.
- **Checklist do reviewer** — correção, legibilidade, performance, segurança, testes.
- **PR templates** — usar checklists via GitHub PR templates.
