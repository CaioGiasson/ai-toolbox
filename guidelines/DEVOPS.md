# DevOps, Infraestrutura e Fluxo de Trabalho

## 1. Tooling e CI/CD

- **Pre-commit checks** — Husky + lint-staged para formatação e linting automático.
- **`npm run build` e `npm test` devem passar antes de qualquer PR.**
- **CI/CD ativo** — pipeline validando build, lint e testes em PRs.
- **Docker Compose** — orquestração com health checks, `depends_on` e volumes.

---

## 2. Conventional Commits

Prefixos obrigatórios:

```
feat:     nova funcionalidade
fix:      correção de bug
refactor: refatoração sem mudança de comportamento
docs:     documentação
test:     testes
chore:    manutenção, dependências
ci:       configuração de pipeline
```

---

## 3. Gitflow e Branching

- **Branches descritivas** — `feat/create-person-endpoint`, `fix/cpf-validation`.
- **Branches protegidas** — `main` e `develop` com CI passando e aprovações obrigatórias.
- **Merge commit** — não squash.

---

## 4. Boas Práticas de Infraestrutura

- **Dependências com versão fixa** — nunca `"latest"` no `package.json`.
- **Crons centralizados** — via `CronManager`, com jobs separados por domínio.
- **Mensageria isolada** — RabbitMQ em `src/queues/` ou `src/workers/`. Mensagens persistentes.
- **Graceful shutdown** — fechar conexões de DB e filas antes do processo encerrar.

### Twelve-Factor App
- Config via variáveis de ambiente.
- Backing services (banco, fila, cache) como recursos substituíveis via URL.
- Dev/prod parity — ambientes o mais parecidos possível.
- Logs para stdout.
- Startup rápido e graceful shutdown.
