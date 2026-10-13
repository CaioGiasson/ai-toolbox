# DevOps, Infraestrutura e Fluxo de Trabalho

## 1. Tooling e CI/CD

- **Versão do Node fixada** — `.nvmrc` e `package.json` → `engines.node`.
- **Pre-commit checks** — Husky + lint-staged para formatação e linting automático. Nunca pular hooks (`--no-verify`) sem pedido explícito.
- **`npm test`, `npm run check` e `npm run build` devem passar antes de qualquer PR.**
- **CI em pull requests** — pipeline (lint → typecheck → test → build) roda em `pull_request`; o gate é a PR. Merge só com o check de CI verde.
- **Docker Compose** — orquestração com health checks, `depends_on` e volumes.

---

## 2. Conventional Commits

Prefixos obrigatórios, com **mensagem em pt-BR**:

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
- **Branch base `main`** — branch de QA integrado (`homolog`) é opcional; não há `develop`.
- **Proteção** — `main` com CI verde obrigatório. Quando o plano do GitHub não permite branch protection, vale política humana: sem push direto que contorne a CI.
- **Nunca `git push --force` em `main`/`master`.**
- **Commit e push contínuos** — na branch da issue, ao concluir ou em marcos lógicos.
- **Merge** — preferir squash (`--delete-branch`), salvo padrão diferente do repositório; após o merge, atualizar `main` local e apagar a branch local e remota.

---

## 4. Boas Práticas de Infraestrutura

- **Dependências com versão fixa** — nunca `"latest"` no `package.json`.
- **Crons centralizados** — em `scripts/cron/`, com jobs separados por domínio.
- **Scripts operacionais** — destrutivos exigem `--confirm`; preferir `--dry-run`; recusar execução em produção quando aplicável.
- **Graceful shutdown** — fechar conexões de DB antes do processo encerrar.

### Twelve-Factor App
- Config via variáveis de ambiente.
- Backing services (banco, cache) como recursos substituíveis via URL.
- Dev/prod parity — ambientes o mais parecidos possível.
- Logs para stdout.
- Startup rápido e graceful shutdown.
