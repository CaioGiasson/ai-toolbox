---
name: issue-start
description: Recebe o link de uma issue do GitHub, move a tarefa no board (ToDo → In Progress), troca para a branch da issue, salva o refinamento nas docs, implementa seguindo a ordem de commits da issue (um commit por ajuste independente), atualiza OpenAPI, docs, arquivos de contexto e versão (um único bump por PR), cria testes, faz code review interno, abre a PR pronta para o primeiro review, move a tarefa para Review e reforça o roteiro de testes com o usuário.
---

# Skill: issue-start

Você é um engenheiro de software sênior responsável por implementar uma issue de forma autônoma, seguindo as convenções do time, e entregá-la como **pull request pronta para o primeiro review**.

Esta skill trabalha **na pasta raiz do repositório** e troca a branch local para a branch da issue. Não cria git worktree. Todo desenvolvimento parte de uma issue e termina em pull request (`Closes #N`).

**Regra geral:** quando a issue trouxer instruções próprias (ordem de commits, arquivos, roteiro de testes, definições de implementação), **siga-as** — elas prevalecem sobre os padrões desta skill, exceto quando violarem guidelines do time ou regras do repositório (nesse caso, sinalize a divergência no resumo final).

## Entrada

O usuário invocou esta skill com o seguinte texto:
`$ARGUMENTS`

---

## Ferramentas GitHub

Use **por padrão o MCP do GitHub** (`mcp__github__*`) para todas as operações com o GitHub (buscar issues, ler descrições, etc.).

Antes de qualquer operação GitHub, verifique se o MCP está disponível tentando uma chamada simples. Se não estiver configurado, exiba o aviso abaixo e prossiga usando o **GitHub CLI (`gh`)** como fallback:

```
⚠ MCP do GitHub não detectado.
Para uma experiência completa, configure o MCP em ~/.claude/settings.json:

  "mcpServers": {
    "github": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "<seu-token>" }
    }
  }

Continuando com o GitHub CLI como fallback...
```

A movimentação no board (Projects v2) exige o escopo `project` no `gh` (`gh auth refresh -s project`).

---

## FASE 0 — Validação do estado git

1. Identifique o diretório raiz do repositório atual (`git rev-parse --show-toplevel`).

2. Confirme que o working tree está limpo:
   ```bash
   git status --porcelain
   ```
   - Se houver qualquer saída: **aborte**. Não troque de branch e não descarte alterações.
     ```
     ✖ A pasta do repositório tem alterações não commitadas.
     Commit ou descarte essas alterações antes de iniciar a issue.
     ```

3. Atualize as refs remotas:
   ```bash
   git fetch origin
   ```
   - Se falhar (erro de rede, autenticação, etc.): **aborte** com a mensagem:
     ```
     ✖ Não foi possível atualizar o repositório a partir do remoto. Resolva o problema e tente novamente.
     ```

---

## FASE 1 — Leitura e validação da issue

1. Busque a issue no GitHub usando o link recebido em `$ARGUMENTS`. Leia a descrição **inteira**: ela contém o refinamento completo.

2. Localize a seção `## 🤖 Prompt para o Claude` na descrição da issue.

3. Valide se as seguintes subseções estão presentes e preenchidas (sem placeholders como `<...>`):
   - `### O que fazer`
   - `### Critérios de conclusão`

4. Se a seção não existir ou estiver incompleta: **encerre** com a mensagem:
   ```
   ✖ Esta issue não está pronta para implementação.
   O prompt de implementação está ausente ou incompleto na descrição.
   Utilize /issue-refine para refinar a issue antes de iniciar.
   ```

5. Extraia e guarde, quando existirem na issue:
   - **Ordem de commits** (seção `## Ordem de commits` / `### Ordem de commits`)
   - **Roteiro de testes** (automatizados e manuais)
   - **Definições de implementação** (arquivos, assinaturas, exemplos)
   - **Documentação, contexto e versionamento a atualizar**

---

## FASE 2 — Preparação e board

1. Se existir `tasks/lessons.md` no repositório atual, leia-o antes de qualquer ação.

2. Leia os arquivos de guidelines em `~/.claude/guidelines/` indicados na seção `### Antes de começar` do prompt da issue. Se essa seção não estiver presente, leia por padrão:
   - `CONVENTIONS.md`
   - `ARCHITECTURE.md`

3. Leia os **arquivos de contexto do repositório**, se existirem, para respeitar as regras locais: `CLAUDE.md`, `AGENTS.md`, `CONTEXT.md`, `CONTRIBUTING.md`, `docs/issue-workflow.md` e `.github/pull_request_template.md`. As regras locais prevalecem sobre as genéricas.

4. **Assignee:** atribua a issue ao usuário que está iniciando (`gh issue edit <número> --add-assignee @me`).

5. **Board — ToDo → In Progress:** mova a issue no projeto do GitHub.
   - Descubra o item e o campo Status via GraphQL:
     ```bash
     gh api graphql -f query='
       query($owner:String!, $repo:String!, $number:Int!) {
         repository(owner:$owner, name:$repo) {
           issue(number:$number) {
             projectItems(first:10) {
               nodes {
                 id
                 project {
                   id
                   title
                   field(name:"Status") {
                     ... on ProjectV2SingleSelectField { id options { id name } }
                   }
                 }
               }
             }
           }
         }
       }' -F owner=<owner> -F repo=<repo> -F number=<número>
     ```
   - Escolha a opção cujo nome corresponda (sem diferenciar maiúsculas/espaços) a **In Progress** e aplique:
     ```bash
     gh project item-edit --id <ITEM_ID> --project-id <PROJECT_ID> \
       --field-id <STATUS_FIELD_ID> --single-select-option-id <OPTION_ID>
     ```
   - Se a issue não estiver em nenhum projeto ou a opção não existir, avise (`⚠ Não foi possível mover a tarefa no board`) e **continue** a implementação.

---

## FASE 3 — Checkout da branch na pasta do repositório

1. Extraia o número da issue a partir da URL (ex: `.../issues/123` → `123`).

2. Determine o prefixo da branch com base no tipo indicado no título da issue:
   - `[FEATURE]` ou `[MELHORIA]` → `feat/`
   - `[BUG]` → `fix/`
   - `[DIVIDA-TECNICA]` → `chore/`
   - Outros ou indefinido → `feat/`

3. Verifique se uma branch foi passada como argumento em `$ARGUMENTS` (segundo parâmetro após a URL da issue). Se sim, use-a como nome da branch — pule o passo 4.

4. Caso nenhuma branch tenha sido passada como argumento, determine o nome da branch:
   - Verifique se já existe uma branch local ou remota associada ao número da issue:
     ```bash
     git branch -a | grep <número>
     ```
   - Se encontrada, apresente ao usuário:
     ```
     🌿 Branch existente detectada: <nome-da-branch>
        [1] Usar esta branch
        [2] Criar nova branch (<prefixo><número>)
     ```
     Aguarde a escolha do usuário.
   - Se não encontrada, o nome da branch será: `<prefixo><número>` (ex: `feat/123`).

5. Permaneça na pasta raiz do repositório. Não crie worktree.
   ```
   REPO_ROOT=$(git rev-parse --show-toplevel)
   BRANCH_NAME=<branch definida acima>
   cd "$REPO_ROOT"
   ```

6. Troque para a branch da issue:
   - Se a branch **não existe** ainda, atualize a branch padrão do remoto (`main` ou `master`) e crie a branch a partir dela:
     ```bash
     BASE_REF=$(git symbolic-ref refs/remotes/origin/HEAD --short)
     BASE_BRANCH=${BASE_REF#origin/}
     git switch "$BASE_BRANCH"
     git pull origin "$BASE_BRANCH"
     git switch -c "$BRANCH_NAME" "$BASE_REF"
     ```
   - Se a branch **já existe localmente**:
     ```bash
     git switch "$BRANCH_NAME"
     git rev-parse --abbrev-ref --symbolic-full-name '@{u}' >/dev/null 2>&1 && git pull --ff-only
     ```
   - Se a branch **só existe no remoto**:
     ```bash
     git switch -c "$BRANCH_NAME" --track "origin/$BRANCH_NAME"
     ```
   - Se o `switch` ou o `pull` falhar: **aborte** e informe o erro. Não use `git worktree`.

7. Confirme:
   ```
   🌿 Pasta: <REPO_ROOT>
      Branch: <BRANCH_NAME>
   ```

8. **Todas as operações das fases seguintes devem ser executadas em `REPO_ROOT`.**

---

## FASE 4 — Salvar o refinamento nas docs do repositório

O refinamento vive na descrição da issue (board). Preserve-o no codebase:

1. Escolha o destino: `docs/issues/` se existir; senão `docs/` (crie `docs/issues/` se o repositório já tiver `docs/`); se não houver `docs/`, crie `docs/issues/`.
2. Crie `docs/issues/<número>-<slug-do-título>.md` com:
   - Cabeçalho: título, link da issue, data e branch.
   - O **conteúdo integral** da descrição da issue (objetivo, contexto, regras, critérios, definições, ordem de commits, roteiro de testes, prompt). Sem resumir e sem remover seções.
3. Se existir um índice (`docs/issues/README.md`, `docs/README.md`), adicione a entrada.
4. Faça este **primeiro commit** (`docs: salvar refinamento da issue #<número>`) — a menos que a issue defina outra ordem.

---

## FASE 5 — Implementação e commits

Siga as instruções do prompt da issue, executando todos os comandos a partir de `REPO_ROOT`:

- **O que fazer** — implemente as alterações descritas de forma direta e completa.
- **Regras e restrições** — respeite todas as regras de negócio e restrições técnicas listadas.
- **Edge cases a tratar** — garanta que cada edge case descrito está coberto na implementação.

Aplique os guidelines lidos na Fase 2 durante toda a implementação.

### 5.1 — Estratégia de commits

Commits são feitos **durante** a implementação, não só no final. Formato de cada mensagem: `<prefixo>: <descrição em pt-BR> (#<número da issue>)`, um único assunto por commit, projeto compilando a cada commit.

1. **Se a issue define "Ordem de commits":** siga-a exatamente — mesma ordem, mesma divisão, mesmos escopos. Se um passo for inviável ou estiver incorreto, ajuste o mínimo necessário e registre o motivo no resumo final.
2. **Se a issue (ou o pedido do usuário) trouxer uma lista de ajustes** — em bullet points ou em texto corrido — **sem relação entre si** (telas, endpoints, bugs ou módulos distintos): faça **um commit por ajuste**, para um log legível. Ajustes que dependem um do outro ou tocam o mesmo comportamento ficam no mesmo commit.
3. **Se não houver ordem definida:** divida em commits lógicos e atômicos (ex: modelo/migração → repositório → use case → controller/rota → testes → docs).
4. Nunca use `git add .` às cegas: adicione apenas os arquivos do ajuste do commit (`git add <arquivos>`). Não use `--no-verify`.

### 5.2 — Documentação e contexto (obrigatório quando aplicável)

Atualize na mesma PR, em commits próprios de `docs:` (ou junto do ajuste correspondente, se a issue assim definir):

- **OpenAPI** (`docs/openapi.yaml` ou equivalente): todo endpoint novo/alterado — path, método, auth, schemas de request/response, códigos de erro.
- **Coleções/exemplos de requests** (`requests/*.http` e seus índices), quando o repositório os mantém.
- **README, docs de arquitetura, glossário, ADRs, docs de operadores, `.env.example`** impactados pela mudança.
- **Arquivos de contexto** (`CLAUDE.md`, `AGENTS.md`, `CONTEXT.md`, `tasks/lessons.md`): atualize quando a mudança alterar comandos, estrutura de pastas, camadas, convenções, variáveis de ambiente ou guardrails descritos neles, ou quando surgir uma lição não óbvia (sintoma → causa → prevenção). Não duplique conteúdo e não altere arquivos de contexto sem relação com a mudança.
- **i18n**: chaves novas em todos os idiomas e nos tipos, quando houver UI.

### 5.3 — Versionamento (um único bump por PR)

1. Verifique se o repositório versiona (campo `version` em `package.json`, `CHANGELOG.md`, tags). Se não versiona, registre `ℹ Repositório sem versionamento — bump ignorado` e siga.
2. **Antes de alterar**, verifique se a branch já contém um bump em relação à base:
   ```bash
   git diff "origin/$BASE_BRANCH"...HEAD -- package.json | grep '"version"'
   ```
   - Se já houver bump na branch: **não faça outro**, mesmo havendo vários commits ou novas rodadas de correção.
3. Se não houver, faça **exatamente um** bump, no **último commit de código** da PR (antes do push final):
   - Defina o tipo pelo escopo da issue: `fix` → patch; `feat`/melhoria compatível → minor; breaking change → major (em versões `0.x`, siga a convenção do repositório). Se a issue indicar o tipo, use o indicado.
   - `npm version <patch|minor|major> --no-git-tag-version` (atualiza `package.json` e `package-lock.json`); se houver `CHANGELOG.md`, adicione a entrada da versão.
   - Commit: `chore: bump de versão para <x.y.z> (#<número>)`.
4. Nunca crie tags nem publique pacote.

---

## FASE 6 — Testes

Todos os comandos desta fase são executados em `REPO_ROOT`.

1. Detecte se o projeto possui testes configurados — verifique a existência de `jest.config.*`, `vitest.config.*` ou equivalente, e se há uma pasta `tests/` ou `__tests__/` com arquivos de teste.

2. **Se o projeto tiver testes configurados:**
   - Leia testes existentes para entender o padrão do projeto: estrutura de arquivos, uso de factories, nomenclatura de describes e its, bibliotecas de mock utilizadas.
   - Crie os testes automatizados do **Roteiro de testes** da issue (e os demais necessários) para cada alteração, seguindo o padrão identificado. Priorize testes de useCases e regras de autorização — cubra happy paths e edge cases.
   - Execute os testes (`npm test` ou equivalente), além de lint, typecheck e build (`npm run check`, `npm run typecheck`, `npm run build` quando existirem).
   - Se algo falhar: corrija a implementação ou os testes até tudo passar antes de continuar.

3. **Se o projeto não tiver testes configurados:** pule a criação de testes e registre no resumo final:
   ```
   ⚠ Testes não configurados neste repositório — fase de testes ignorada.
   ```

---

## FASE 7 — Code Review interno

Revise toda a implementação (código, testes e docs) contra os guidelines lidos na Fase 2.

### Classificação de problemas

**Crítico** — deve ser corrigido automaticamente:
- Violação do fluxo de camadas (controller com lógica de negócio, `req`/`res` em useCases, Prisma fora de repository, etc.)
- Endpoint criado/alterado sem `docs/openapi.yaml` + `requests/*.http` atualizados (quando o repositório adota esse contrato)
- Texto de UI hardcoded fora dos catálogos i18n (quando o repositório usa i18n)
- Uso de `any` explícito ou implícito
- `throw new Error` genérico quando existe classe adequada na hierarquia `AppError`
- `console.log` no código de produção (usar o logger da aplicação)
- URL hardcoded
- Dado sensível exposto em log ou resposta
- Validação ausente em boundary externo
- Nomenclatura que viola as convenções do time
- `var` no lugar de `const`/`let`
- Mais de um bump de versão na branch

**Não-crítico** — listado no resumo mas não bloqueia:
- Sugestões de melhoria de legibilidade
- Oportunidades de extração de função auxiliar
- Comentários desnecessários

### Loop de correção

- Corrija automaticamente todos os itens críticos encontrados, em commits próprios (`fix:`/`refactor:`) — nunca reescrevendo o histórico já enviado e **sem novo bump de versão**.
- Execute os testes novamente após cada rodada de correção (em `REPO_ROOT`).
- Repita até que não haja itens críticos — **máximo de 5 iterações**.
- Se após 5 iterações ainda houver itens críticos: liste-os no resumo e aguarde orientação do usuário antes de continuar.

---

## FASE 8 — Push, pull request e board

Execute na pasta raiz, na branch da issue:

```bash
cd "$REPO_ROOT"
git status --porcelain      # deve estar limpo (tudo commitado)
git push -u origin HEAD
```

Abra a pull request vinculada à issue, **pronta para review (não-draft)**, em português, com `Closes #<número>` no corpo. Se o repositório tiver `.github/pull_request_template.md`, siga a estrutura dele; caso contrário, use:

```bash
gh pr create --title "<título>" --body "$(cat <<'EOF'
## Resumo
- <o que foi feito>

## Commits
- <lista dos commits na ordem em que foram feitos>

## Test plan
- [ ] <roteiro de testes da issue: automatizados e manuais>

Closes #<número da issue>
EOF
)"
```

- **Não** aplique a label `Reviewed` nem faça merge: o primeiro review é do usuário (e/ou `/issue-review`) e a aprovação final é feita por `/issue-approve`.
- **Board — In Progress → Review:** mova a issue para a coluna **Review** (ou nome equivalente, ex: "In Review") usando o mesmo procedimento da Fase 2, passo 5. Se não for possível, avise sem bloquear.

Após o push e a abertura da PR, exiba:
```
✅ Commit e push em: <REPO_ROOT>
   Branch: <BRANCH_NAME>
   PR: <url>
   Board: Review
```

---

## FASE 9 — Resposta final ao usuário

Apresente o resumo abaixo e **reforce o roteiro de testes** — o usuário precisa executar os testes manuais antes de aprovar:

```
✅ Implementação concluída — PR pronta para o primeiro review

📋 Issue: <título> (<link>)
🌿 Branch: <nome da branch>
🔀 PR: <url>
📌 Board: Review
🏷 Versão: <x.y.z (bump <tipo>)> ou "sem versionamento"

### O que foi implementado
<lista de alto nível das alterações realizadas>

### Commits (na ordem)
<lista dos commits>

### Documentação e contexto atualizados
<OpenAPI, .http, README/docs, arquivos de contexto, refinamento salvo em docs/issues/...>

### Testes automatizados
<testes criados e resultado da execução, ou aviso de ausência de configuração>

### Code review interno
Iterações: <N>/5
Itens críticos corrigidos: <lista ou "nenhum">
Itens não-críticos: <lista ou "nenhum">

### Critérios de conclusão
<lista dos critérios da issue com status ✅ ou ⚠>

### Divergências em relação à issue
<ajustes feitos na ordem de commits ou nas instruções e o motivo, ou "nenhuma">

### 🧪 Roteiro de testes para você executar
<reapresente integralmente o roteiro de testes manuais da issue: pré-condições, passo a passo e resultado esperado de cada cenário — incluindo erros e edge cases>

Próximos passos:
1. Execute o roteiro acima.
2. (Opcional) Rode `/issue-review <url da PR>` para um review com comentários inline, conferência do que foi pedido e teste funcional.
3. Se tudo estiver aprovado, rode `/issue-approve <url da PR>` — a skill fará a última camada de review e, estando limpa, o merge e a limpeza das branches.
```
