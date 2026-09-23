---
name: start-issue
description: Recebe o link de uma issue do GitHub, valida o estado do repositório, troca para a branch da issue na pasta raiz, implementa o prompt da issue, cria testes, faz code review automático com correção de itens críticos, commita, faz push e abre a pull request vinculada.
---

# Skill: start-issue

Você é um engenheiro de software sênior responsável por iniciar a implementação de uma issue de forma autônoma, seguindo as convenções do time e garantindo qualidade antes do primeiro commit.

Esta skill trabalha **na pasta raiz do repositório** e troca a branch local para a branch da issue. Não cria git worktree. Todo desenvolvimento parte de uma issue e termina em pull request (`Closes #N`).

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

## FASE 4 — Implementação

Siga as instruções do prompt da issue, executando todos os comandos a partir de `REPO_ROOT`:

- **O que fazer** — implemente as alterações descritas de forma direta e completa.
- **Regras e restrições** — respeite todas as regras de negócio e restrições técnicas listadas.
- **Edge cases a tratar** — garanta que cada edge case descrito está coberto na implementação.

Aplique os guidelines lidos na Fase 2 durante toda a implementação.

---

## FASE 5 — Testes

Todos os comandos desta fase são executados em `REPO_ROOT`.

1. Detecte se o projeto possui testes configurados — verifique a existência de `jest.config.*`, `vitest.config.*` ou equivalente, e se há uma pasta `tests/` ou `__tests__/` com arquivos de teste.

2. **Se o projeto tiver testes configurados:**
   - Leia testes existentes para entender o padrão do projeto: estrutura de arquivos, uso de factories, nomenclatura de describes e its, bibliotecas de mock utilizadas.
   - Crie testes automatizados para cada alteração implementada na Fase 4, seguindo o padrão identificado.
   - Priorize testes de useCases e policies — cubra happy paths e edge cases da issue.
   - Execute os testes (`npm test` ou equivalente) em `REPO_ROOT`.
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
- Execute os testes novamente após cada rodada de correção (em `REPO_ROOT`).
- Repita até que não haja itens críticos — **máximo de 5 iterações**.
- Se após 5 iterações ainda houver itens críticos: liste-os no resumo e aguarde orientação do usuário antes de continuar.

---

## FASE 7 — Resumo da implementação

Apresente o seguinte resumo ao usuário:

```
✅ Implementação concluída

📋 Issue: <título> (<link>)
🌿 Branch: <nome da branch>
📁 Pasta: <REPO_ROOT>

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

```

Siga para o commit, o push e a pull request sem pedir confirmação extra.

---

## FASE 8 — Commit, push e pull request

Execute na pasta raiz, na branch da issue:

```bash
cd "$REPO_ROOT"
git add .
git commit -m "<prefixo>: <título da feature> (#<número da issue>)"
git push -u origin HEAD
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

Abra a pull request vinculada à issue, em português, com `Closes #<número>` no corpo:

```bash
gh pr create --title "<título>" --body "$(cat <<'EOF'
## Resumo
- <o que foi feito>

## Test plan
- [ ] <como validar>

Closes #<número da issue>
EOF
)"
```

Após o push e a abertura da PR, exiba:
```
✅ Commit e push em: <REPO_ROOT>
   Branch: <BRANCH_NAME>
   PR: <url>
```
