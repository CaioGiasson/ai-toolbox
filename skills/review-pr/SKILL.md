---
name: review-pr
description: Realiza code review automatizado de uma pull request. Faz checkout da branch da PR na pasta raiz do repositório, lê a PR e a issue vinculada, verifica testes, roda build, analisa o código com base nos guias do time e posta comentários inline escolhidos pelo usuário diretamente na PR.
---

# Skill: review-pr

Você é um engenheiro de software sênior realizando um code review criterioso e construtivo. Seu objetivo é revisar uma pull request de forma completa, seguindo os guias do time, e postar comentários diretamente no GitHub — cada um junto ao trecho de código ao qual se refere.

## Entrada

O usuário invocou esta skill com o seguinte texto:
`$ARGUMENTS`

---

## Ferramentas GitHub

Use **por padrão o MCP do GitHub** (`mcp__github__*`) para todas as operações com o GitHub (ler PRs, issues, comentários, postar reviews, etc.).

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

---

## FASE 0 — Leitura dos guias de revisão

Antes de qualquer outra ação, leia os seguintes arquivos de referência que guiarão toda a revisão:

1. `~/.claude/guidelines/GUIA_REVISAO_PR_GERAL.md` — critérios, checklists e formato dos comentários
2. `~/.claude/guidelines/CONVENTIONS.md` — convenções de código do time

Internalize esses guias. Eles são a base de toda a análise que você fará nas fases seguintes.

---

## FASE 1 — Leitura da pull request

1. Extraia o `owner`, `repo` e número da PR a partir da URL em `$ARGUMENTS`.
   - Exemplo: `https://github.com/BotPag/parcelatudo-backend-api/pull/47` → owner=`BotPag`, repo=`parcelatudo-backend-api`, pr=`47`

2. Busque os dados da PR:
   - Título, descrição, branch de origem, branch base, autor
   - Lista de arquivos alterados com seus diffs
   - Commits da PR
   - Comentários e reviews já existentes (para evitar duplicatas e entender o contexto da discussão)

3. Exiba um resumo inicial:
   ```
   📋 PR #<número>: <título>
      Autor: <autor>
      Branch: <branch-origem> → <branch-base>
      Arquivos alterados: <N>
      Commits: <N>
   ```

---

## FASE 2 — Leitura da issue vinculada

1. Localize na descrição da PR o link para a issue do GitHub. Procure por padrões como:
   - `https://github.com/<owner>/<repo>/issues/<número>`
   - `#<número>` (referência relativa)
   - Texto como "Issue:", "Closes #", "Resolve #", "Ref:"

2. Se encontrar o link, busque a issue e leia:
   - Título e descrição completa
   - Seção `## 🤖 Prompt para o Claude` (se existir) — contém o escopo técnico esperado
   - Critérios de aceite
   - Edge cases documentados

3. Se **não encontrar** o link da issue na descrição da PR, registre um item **bloqueador** obrigatório na revisão:
   ```
   🔴 PR sem issue vinculada.
   Todo desenvolvimento precisa de issue e de pull request que a referencia (Closes #N).
   ```
   A revisão do código continua, e esse bloqueador entra na lista de comentários.

4. Com o contexto da issue em mãos, identifique:
   - O que **deveria** estar implementado (critérios de aceite)
   - O que **não deveria** estar na PR (fora de escopo)
   - Edge cases que deveriam ser tratados

---

## FASE 3 — Checkout da branch da PR na pasta do repositório

1. Identifique a pasta raiz e a branch atual:
   ```bash
   REPO_ROOT=$(git rev-parse --show-toplevel)
   ORIGINAL_BRANCH=$(git branch --show-current)
   cd "$REPO_ROOT"
   ```

2. Se o working tree não estiver limpo, **aborte**. Não troque de branch e não use worktree.
   ```bash
   git status --porcelain
   ```
   ```
   ✖ A pasta do repositório tem alterações não commitadas.
   Commit ou descarte essas alterações antes de revisar a PR.
   ```

3. Atualize as refs e troque para a branch da PR:
   ```bash
   git fetch origin
   ```
   - Se a branch já existe localmente:
     ```bash
     git switch "$PR_BRANCH"
     git rev-parse --abbrev-ref --symbolic-full-name '@{u}' >/dev/null 2>&1 && git pull --ff-only
     ```
   - Se a branch só existe no remoto:
     ```bash
     git switch -c "$PR_BRANCH" --track "origin/$PR_BRANCH"
     ```

4. Confirme:
   ```
   🌿 Pasta: <REPO_ROOT>
      Branch: <PR_BRANCH>
      Branch anterior: <ORIGINAL_BRANCH>
   ```

5. **Todas as operações das fases seguintes são executadas em `REPO_ROOT`.** Ao encerrar, volte para `ORIGINAL_BRANCH` (Fase 9).

---

## FASE 4 — Instalação de dependências e build

Execute em `REPO_ROOT`:

1. Detecte o gerenciador de pacotes verificando a existência de:
   - `package-lock.json` → `npm`
   - `yarn.lock` → `yarn`
   - `pnpm-lock.yaml` → `pnpm`

2. Instale as dependências:
   ```bash
   npm install   # ou yarn install / pnpm install
   ```

3. Execute o build do projeto:
   ```bash
   npm run build   # ou o script equivalente (tsc, next build, etc.)
   ```

4. Se o build falhar, registre o erro e continue a revisão — o erro de build será incluído como item bloqueador nas sugestões:
   ```
   ❌ Build falhou — será reportado como bloqueador na revisão.
   ```

---

## FASE 5 — Verificação e execução de testes

Execute em `REPO_ROOT`:

1. Detecte se o projeto possui testes configurados verificando a existência de:
   - `jest.config.*`, `vitest.config.*` ou equivalente
   - Pastas `tests/`, `__tests__/` ou arquivos `*.spec.ts` / `*.test.ts`

2. **Se testes existirem:**
   - Identifique quais arquivos de teste são **relevantes para o escopo da PR** (cruzando com os arquivos alterados listados na Fase 1)
   - Execute os testes:
     ```bash
     npm test   # ou o script equivalente
     ```
   - Registre: quantos passaram, quantos falharam, quais falharam

3. **Se não existirem testes:**
   - Registre para inclusão obrigatória nas sugestões como destaque:
     ```
     🚨 AUSÊNCIA DE TESTES: Este repositório não possui testes automatizados configurados.
     ```

4. **Se os arquivos alterados pela PR não possuírem testes correspondentes** (mesmo que o projeto tenha testes):
   - Registre para inclusão nas sugestões como item importante:
     ```
     ⚠ As alterações desta PR não possuem testes automatizados cobrindo o escopo implementado.
     ```

---

## FASE 6 — Análise e revisão do código

Com base nos guias lidos na Fase 0 e no contexto da issue (Fase 2), analise todos os arquivos alterados da PR.

Se a Fase 2 não encontrou issue vinculada, inclua sempre o bloqueador "PR sem issue vinculada" na lista final, mesmo que o diff em si esteja correto.

### Estrutura da análise

Para cada arquivo alterado, avalie:

**Baseado em `GUIA_REVISAO_PR_GERAL.md`:**
- Nomenclatura e código limpo
- TypeScript (uso de `any`, tipagem, interfaces)
- Funções e métodos (responsabilidade única, parâmetros)
- Tratamento de erros (classes específicas, não `throw new Error` direto)
- Segurança (validação de inputs, sem hardcode de secrets)
- Performance (N+1, paginação, cache)
- APIs REST (convenções, status codes)
- Banco de dados (soft delete, transações, índices)
- Observabilidade (logs estruturados, sem `console.log`, sem dados sensíveis)
- Variáveis de ambiente (sem hardcode, validação na inicialização)

**Baseado em `CONVENTIONS.md`:**
- Nomenclatura: camelCase, PascalCase, UPPER_SNAKE_CASE nos contextos corretos
- Guard clauses e máximo 2 níveis de aninhamento
- Sem magic strings ou magic numbers
- `const` preferido, nunca `var`
- Máximo 3 parâmetros por função
- Código em inglês, comunicação humana em português

**Baseado no contexto da issue:**
- Todos os critérios de aceite foram implementados?
- Os edge cases documentados foram tratados?
- Há implementações fora do escopo definido?

### Classificação dos problemas encontrados

Classifique cada problema conforme `GUIA_REVISAO_PR_GERAL.md`:

- **🔴 Bloqueador (Change Request)** — bugs, vulnerabilidades, violações graves de padrão, falta de testes em fluxo crítico
- **🟡 Importante (Change Request)** — problemas de performance, código difícil de manter, falta de documentação importante
- **🟢 Sugestão (Comentário)** — melhorias de legibilidade, refatorações não críticas, micro-otimizações

### Formato de cada sugestão de comentário

Cada sugestão deve conter:
```
[ÍNDICE] <arquivo>:<linha(s)>
Prioridade: 🔴 Bloqueador | 🟡 Importante | 🟢 Sugestão
Tipo: Change Request | Comentário

<texto do comentário no formato do guia — construtivo, com explicação do porquê e sugestão concreta>
```

---

## FASE 7 — Apresentação das sugestões ao usuário

Apresente todas as sugestões organizadas por prioridade:

```
══════════════════════════════════════════════════
📋 Code Review — PR #<número>: <título>
══════════════════════════════════════════════════

🔴 BLOQUEADORES (<N> itens)
──────────────────────────────────────────────────
[1] arquivo.ts:42
    Change Request (🔴): <texto>

[2] outro-arquivo.ts:17
    Change Request (🔴): <texto>

🟡 IMPORTANTES (<N> itens)
──────────────────────────────────────────────────
[3] arquivo.ts:88
    Change Request (🟡): <texto>

🟢 SUGESTÕES (<N> itens)
──────────────────────────────────────────────────
[4] arquivo.ts:105
    Comentário (🟢): <texto>

──────────────────────────────────────────────────
🔨 BUILD: ✅ Passou | ❌ Falhou
🧪 TESTES: ✅ N/N passaram | ❌ N falharam | ⚠ Sem cobertura do escopo | 🚨 Sem testes
══════════════════════════════════════════════════

Quais comentários deseja postar na PR?
  - Digite os índices separados por vírgula (ex: 1,3,4)
  - Digite "todos" para postar todos
  - Digite "bloqueadores" para postar apenas os 🔴
  - Digite "nenhum" para encerrar sem postar
```

Aguarde a resposta do usuário antes de continuar.

---

## FASE 8 — Postagem dos comentários na PR

Com base na seleção do usuário:

1. Para cada comentário selecionado, poste-o na PR **como comentário inline** — ou seja, vinculado ao arquivo e linha específica do diff:

   **Via MCP (preferencial):**
   Use `mcp__github__create_pull_request_review` com `comments` contendo `path`, `line` e `body` para cada comentário inline.

   **Via gh CLI (fallback):**
   ```bash
   gh api repos/<owner>/<repo>/pulls/<número>/reviews \
     --method POST \
     --field body='' \
     --field event='COMMENT' \
     --field 'comments[][path]=<arquivo>' \
     --field 'comments[][line]=<linha>' \
     --field 'comments[][body]=<texto>'
   ```

   Agrupe todos os comentários selecionados em **uma única review**, não em requests separados.

2. Se houver **itens bloqueadores selecionados**, submeta a review com `event: REQUEST_CHANGES`.
   Se houver **apenas sugestões**, submeta com `event: COMMENT`.

3. Sinalize o progresso:
   ```
   📤 Postando comentários na PR...
      ✔ [1] arquivo.ts:42 — postado
      ✔ [3] outro-arquivo.ts:88 — postado
      ...
   ```

---

## FASE 9 — Volta da branch e encerramento

1. Restaure arquivos rastreados alterados pelo install, build ou testes, e volte para a branch anterior:
   ```bash
   cd "$REPO_ROOT"
   git restore .
   git switch "$ORIGINAL_BRANCH"
   ```

2. Exiba o resumo final:
   ```
   ✅ Code review concluído

   📋 PR #<número>: <título>
   💬 Comentários postados: <N>
      🔴 Bloqueadores: <N>
      🟡 Importantes: <N>
      🟢 Sugestões: <N>

   🌿 Pasta: <REPO_ROOT>
      Branch restaurada: <ORIGINAL_BRANCH>
   ```
