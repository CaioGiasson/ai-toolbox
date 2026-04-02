---
name: start-issue
description: Recebe o link de uma issue do GitHub, valida o estado do repositório, cria um worktree isolado com a branch correta, implementa o prompt da issue, cria testes, faz code review automático com correção de itens críticos e gera o primeiro commit para validação do dev.
---

# Skill: start-issue

Você é um engenheiro de software sênior responsável por iniciar a implementação de uma issue de forma autônoma, seguindo as convenções do time e garantindo qualidade antes do primeiro commit.

Esta skill usa **git worktree** para isolar o trabalho em um diretório separado, permitindo que múltiplos agentes operem em paralelo no mesmo repositório sem conflito de branches.

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

---

## FASE 0 — Validação do estado git

1. Identifique o diretório raiz do repositório atual (`git rev-parse --show-toplevel`).

2. Verifique se a branch principal (`main` ou `master`) está acessível:
   ```bash
   git fetch origin
   git pull origin main   # ou master, conforme o repo
   ```
   - Se falhar (erro de rede, conflito, etc.): **aborte** com a mensagem:
     ```
     ✖ Não foi possível atualizar a branch principal. Resolva o problema e tente novamente.
     ```

3. **Não é necessário** que o working tree atual esteja limpo nem que a branch atual seja `main` — cada agente trabalhará em seu próprio worktree isolado.

---

## FASE 1 — Leitura e validação da issue

1. Busque a issue no GitHub usando o link recebido em `$ARGUMENTS`.

2. Localize a seção `## 🤖 Prompt para o Claude` na descrição da issue.

3. Valide se as seguintes subseções estão presentes e preenchidas (sem placeholders como `<...>`):
   - `### O que fazer`
   - `### Critérios de conclusão`

4. Se a seção não existir ou estiver incompleta: **encerre** com a mensagem:
   ```
   ✖ Esta issue não está pronta para implementação.
   O prompt de implementação está ausente ou incompleto na descrição.
   Utilize /create-issue para refinar a issue antes de iniciar.
   ```

---

## FASE 2 — Preparação

1. Se existir `tasks/lessons.md` no repositório atual, leia-o antes de qualquer ação.

2. Leia os arquivos de guidelines em `~/.claude/guidelines/` indicados na seção `### Antes de começar` do prompt da issue. Se essa seção não estiver presente, leia por padrão:
   - `CONVENTIONS.md`
   - `ARCHITECTURE.md`

---

## FASE 3 — Criação do worktree e branch

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

5. Defina o path do worktree com base na raiz do repositório:
   ```
   REPO_ROOT=$(git rev-parse --show-toplevel)
   REPO_NAME=$(basename $REPO_ROOT)
   BRANCH_NAME=<branch definida acima>
   WORKTREE_PATH="$REPO_ROOT/../${REPO_NAME}-worktrees/${BRANCH_NAME//\//-}"
   ```
   Exemplo: se o repo está em `~/projetos/api` e a branch é `feat/123`, o worktree ficará em `~/projetos/api-worktrees/feat-123`.

6. Crie o worktree:
   - Se a branch **não existe** ainda:
     ```bash
     git worktree add "$WORKTREE_PATH" -b "$BRANCH_NAME" origin/main
     ```
   - Se a branch **já existe** localmente ou remotamente:
     ```bash
     git worktree add "$WORKTREE_PATH" "$BRANCH_NAME"
     ```

7. Confirme a criação:
   ```
   🌿 Worktree criado em: <WORKTREE_PATH>
      Branch: <BRANCH_NAME>
   ```

8. **Todas as operações das fases seguintes devem ser executadas dentro de `WORKTREE_PATH`.**

---

## FASE 4 — Implementação

Siga as instruções do prompt da issue, executando todos os comandos a partir de `WORKTREE_PATH`:

- **O que fazer** — implemente as alterações descritas de forma direta e completa.
- **Regras e restrições** — respeite todas as regras de negócio e restrições técnicas listadas.
- **Edge cases a tratar** — garanta que cada edge case descrito está coberto na implementação.

Aplique os guidelines lidos na Fase 2 durante toda a implementação.

---

## FASE 5 — Testes

Todos os comandos desta fase são executados dentro de `WORKTREE_PATH`.

1. Detecte se o projeto possui testes configurados — verifique a existência de `jest.config.*`, `vitest.config.*` ou equivalente, e se há uma pasta `tests/` ou `__tests__/` com arquivos de teste.

2. **Se o projeto tiver testes configurados:**
   - Leia testes existentes para entender o padrão do projeto: estrutura de arquivos, uso de factories, nomenclatura de describes e its, bibliotecas de mock utilizadas.
   - Crie testes automatizados para cada alteração implementada na Fase 4, seguindo o padrão identificado.
   - Priorize testes de useCases e policies — cubra happy paths e edge cases da issue.
   - Execute os testes (`npm test` ou equivalente) dentro de `WORKTREE_PATH`.
   - Se algum teste falhar: corrija a implementação ou os testes até todos passarem antes de continuar.

3. **Se o projeto não tiver testes configurados:** pule esta fase e registre no resumo final:
   ```
   ⚠ Testes não configurados neste repositório — fase de testes ignorada.
   ```

---

## FASE 6 — Code Review

Revise toda a implementação (código e testes) contra os guidelines lidos na Fase 2.

### Classificação de problemas

**Crítico** — deve ser corrigido automaticamente:
- Violação do fluxo de camadas (controller com lógica de negócio, `req`/`res` em useCases, etc.)
- Uso de `any` explícito ou implícito
- `throw new Error` direto sem classe de erro específica
- `console.log` no código de produção
- URL hardcoded
- Dado sensível exposto em log ou resposta
- Validação ausente em boundary externo
- Nomenclatura que viola as convenções do time
- `var` no lugar de `const`/`let`

**Não-crítico** — listado no resumo mas não bloqueia:
- Sugestões de melhoria de legibilidade
- Oportunidades de extração de função auxiliar
- Comentários desnecessários

### Loop de correção

- Corrija automaticamente todos os itens críticos encontrados.
- Execute os testes novamente após cada rodada de correção (dentro de `WORKTREE_PATH`).
- Repita até que não haja itens críticos — **máximo de 5 iterações**.
- Se após 5 iterações ainda houver itens críticos: liste-os no resumo e aguarde orientação do usuário antes de continuar.

---

## FASE 7 — Verificação e confirmação

Apresente o seguinte resumo ao usuário:

```
✅ Implementação concluída — aguardando confirmação para commit

📋 Issue: <título> (<link>)
🌿 Branch: <nome da branch>
📁 Worktree: <WORKTREE_PATH>

### O que foi implementado
<lista de alto nível das alterações realizadas>

### Testes
<lista de testes criados, ou aviso de ausência de configuração>

### Code review
Iterações: <N>/5
Itens críticos corrigidos: <lista ou "nenhum">
Itens não-críticos: <lista ou "nenhum">

### Critérios de conclusão
<lista dos critérios da issue com status ✅ ou ⚠>

---
Revise o diff e confirme para commitar, ou interrompa para ajustes.
```

Aguarde confirmação explícita do usuário antes de prosseguir para o commit.

---

## FASE 8 — Primeiro commit

Execute o commit dentro de `WORKTREE_PATH`:

```bash
cd "$WORKTREE_PATH"
git add .
git commit -m "<prefixo>: <título da feature> (#<número da issue>)"
```

Formato do commit:
```
<prefixo>: <título da feature> (#<número da issue>)
```

Exemplos:
```
feat: adiciona endpoint de criação de pessoa (#123)
fix: corrige validação de CPF no useCase (#87)
chore: remove dependência legada do módulo de pagamento (#210)
```

Após o commit, exiba:
```
✅ Commit criado em: <WORKTREE_PATH>
   Branch: <BRANCH_NAME>

Para remover o worktree após o merge do PR:
  git worktree remove <WORKTREE_PATH>
  git branch -d <BRANCH_NAME>
```
