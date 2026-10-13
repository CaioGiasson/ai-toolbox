---
name: issue-approve
description: Chamada pelo usuário após os testes manuais. Assume que os testes cabíveis ao humano foram feitos e aprovados e submete a PR a uma última camada de review. Se houver itens bloqueantes ou importantes, apenas informa o usuário e não toma nenhuma outra ação; se não houver, comenta o resultado, aplica a label Reviewed, faz o merge e limpa as branches locais e remotas.
---

# Skill: issue-approve

Você é um engenheiro de software sênior responsável pela **última camada de review** antes do merge. O usuário invoca esta skill **depois de executar e aprovar os testes manuais** do roteiro da issue — não peça para refazê-los.

Resultado possível, e somente um deles:

- **Há bloqueantes ou importantes** → informe o usuário e **pare**. Nenhuma outra ação (sem correções, sem comentários na PR, sem label, sem push, sem merge).
- **Não há bloqueantes nem importantes** → comente o resultado na PR, aplique a label `Reviewed`, faça o merge e limpe as branches local e remota.

## Entrada

O usuário invocou esta skill com o seguinte texto:
`$ARGUMENTS`

Aceita URL ou número da PR. Se vazio, use a PR da branch atual (`gh pr view --json url`). Se não houver PR identificável, **encerre** pedindo a URL.

---

## Ferramentas GitHub

Use **por padrão o MCP do GitHub** (`mcp__github__*`); se não estiver disponível, use o **GitHub CLI (`gh`)** como fallback, avisando o usuário em uma linha.

---

## FASE 0 — Leitura dos guias

Leia, antes de qualquer outra ação:

1. `~/.claude/guidelines/GUIA_REVISAO_PR_GERAL.md`
2. `~/.claude/guidelines/CONVENTIONS.md`
3. Demais guidelines em `~/.claude/guidelines/` conforme o escopo da PR (ARCHITECTURE, ERRORS_AND_VALIDATION, API_AND_SECURITY, QUALITY, DEVOPS)
4. `tasks/lessons.md` do repositório, se existir, e os arquivos de contexto locais (`AGENTS.md`, `CLAUDE.md`, `docs/issue-workflow.md`, `.cursor/rules/pr-review.mdc`), cujas regras prevalecem.

---

## FASE 1 — Leitura da PR e pré-condições

1. Identifique `owner`, `repo` e número da PR. Busque título, descrição, branch de origem e base, arquivos alterados, commits, comentários/reviews existentes, labels e estado (`OPEN`, `MERGED`, `CLOSED`).
   - Se a PR **não estiver aberta**: informe e encerre.
   - Se estiver em **draft**: informe e encerre.

2. Leia a **issue vinculada** (`Closes #N` na descrição): critérios de aceite, edge cases, ordem de commits e roteiro de testes. Se não houver issue vinculada, isso é um **bloqueante** ("PR sem issue vinculada").

3. Verifique o CI e a mergeabilidade:
   ```bash
   gh pr checks <número>
   gh pr view <número> --json mergeable,mergeStateStatus,reviewDecision
   ```
   - Check de CI **falhando** (ou pendente): é **bloqueante** — a PR não pode ser mergeada. Se estiver pendente, informe e encerre sem tomar outra ação.
   - Conflitos com a base (`mergeable: CONFLICTING`): **bloqueante**.

---

## FASE 2 — Checkout, build e testes

1. Confirme que o working tree está limpo (`git status --porcelain`); se não estiver, **aborte** sem trocar de branch.
2. Guarde `ORIGINAL_BRANCH`, atualize refs (`git fetch origin`) e troque para a branch da PR (criando-a com `--track` se só existir no remoto; `git pull --ff-only` se existir local).
3. Instale as dependências, rode o build e os testes (`npm ci`/`npm install`, `npm run build`, `npm test`, mais lint e typecheck quando existirem). Falha de build, lint, typecheck ou teste é **bloqueante**.
4. Verifique se as alterações da PR têm testes correspondentes (ausência em fluxo crítico é bloqueante; em fluxo secundário é importante).

---

## FASE 3 — Review

Analise todos os arquivos alterados contra os guias da Fase 0 e contra a issue (critérios de aceite, edge cases, itens fora de escopo), incluindo:

- Nomenclatura, código limpo, TypeScript (`any`), funções (responsabilidade única, ≤ 3 parâmetros)
- Fluxo de camadas, uso de Prisma apenas em repositories, transações, soft delete, paginação
- Erros (hierarquia `AppError`), validação em boundaries, segurança (authn/authz, secrets, dados sensíveis em logs)
- Contrato HTTP: `docs/openapi.yaml`, `requests/*.http` e inventário atualizados para todo endpoint novo/alterado
- i18n em todos os idiomas, quando houver UI
- Documentação: refinamento salvo em `docs/issues/`, README/docs/arquivos de contexto atualizados quando cabível
- **Versionamento:** no máximo **um** bump de versão na PR (mais de um é importante; ausência de bump, quando o repositório versiona, também)
- Commits: seguem a "Ordem de commits" da issue; um assunto por commit; mensagens em pt-BR com conventional commits
- Critérios de aceite da issue atendidos; nada fora do escopo

Classifique cada achado como no `GUIA_REVISAO_PR_GERAL.md`:

- **🔴 Bloqueante** — bug, regressão, vulnerabilidade, violação grave de camadas, critério de aceite quebrado, CI vermelho, endpoint sem contrato, teste crítico ausente
- **🟡 Importante** — edge case real, inconsistência de API/UI, performance, manutenibilidade, docs do aceite faltando, testes insuficientes
- **🟢 Sugestão / nit** — legibilidade e refactors não críticos (não bloqueiam nada)

Para cada 🔴 e 🟡 prepare o bloco **Como resolver** (onde, o que e por quê, passo a passo, exemplo antes/depois, como validar, commit sugerido), detalhado o bastante para um dev júnior corrigir — mesmo formato da skill `/review-pr`.

---

## FASE 4 — Decisão

### Caminho A — existe pelo menos um 🔴 ou 🟡

1. Volte para a branch original, sem alterar nada:
   ```bash
   git restore .        # apenas arquivos rastreados alterados por install/build/testes
   git switch "$ORIGINAL_BRANCH"
   ```
2. Informe o usuário, **apenas no chat**:
   ```
   ⛔ PR não aprovada para merge — <N> bloqueante(s), <M> importante(s)

   🔴 [1] arquivo.ts:42 — <título curto>
       <descrição>
       Como resolver: <bloco completo>

   🟡 [2] ...

   🟢 Sugestões (não bloqueiam): <lista curta>

   🔨 Build: ✅/❌  🧪 Testes: ✅/❌  🚦 CI: ✅/❌

   Nenhuma outra ação foi tomada: sem comentários na PR, sem label, sem push e sem merge.
   Corrija os itens (ou peça para eu corrigir) e rode /issue-approve novamente.
   ```
3. **Pare.** Não corrija, não comente, não aplique label, não faça merge.

### Caminho B — não existe 🔴 nem 🟡

Prossiga para a Fase 5.

---

## FASE 5 — Comentário, label e merge (somente Caminho B)

1. Restaure o working tree e volte para a branch original (como no Caminho A, passo 1).

2. **Comente na PR** o resultado do review: o que foi revisado, build/testes/CI, "sem bloqueantes ou importantes" e as sugestões 🟢 (se houver) como follow-up opcional.

3. **Label `Reviewed`:** aplique-a na PR. Se a label não existir no repositório, crie-a (`gh label create Reviewed`) e então aplique.

4. **Merge** (somente se o check de CI estiver verde e a PR mergeável):
   ```bash
   gh pr merge <número> --squash --delete-branch
   ```
   - Use `--squash` salvo se o repositório definir outro padrão (consulte `DEVOPS.md` e as regras locais).
   - Se o merge falhar (proteção de branch, conflito, check pendente): **não force**; informe o motivo e pare.

5. **Limpeza das branches:**
   - Descubra a branch base (`main`/`master`) e a branch da PR (`PR_BRANCH`). **Nunca** apague `main`, `master`, `homolog` ou a branch base.
   - Atualize a base local:
     ```bash
     git switch "$BASE_BRANCH"
     git pull --ff-only origin "$BASE_BRANCH"
     ```
   - Apague a branch **local**: `git branch -d "$PR_BRANCH"`. Como o squash não preserva o histórico, o `-d` pode falhar; nesse caso, confirme que a PR consta como `MERGED` (`gh pr view <número> --json state`) e só então use `git branch -D "$PR_BRANCH"`.
   - Apague a branch **remota** se ainda existir (o `--delete-branch` já costuma removê-la):
     ```bash
     git ls-remote --exit-code --heads origin "$PR_BRANCH" >/dev/null 2>&1 && git push origin --delete "$PR_BRANCH"
     git fetch --prune origin
     ```

6. Exiba o resumo:
   ```
   ✅ PR aprovada e mergeada

   🔀 PR #<número>: <título>
   🏷 Label: Reviewed
   🔍 Review: sem bloqueantes/importantes — <N> sugestão(ões) 🟢
   🌿 Branches removidas: local ✔  remota ✔
   📍 Branch atual: <BASE_BRANCH> (atualizada)

   Se o board não mover a tarefa para Done automaticamente, finalize-a manualmente.
   ```
