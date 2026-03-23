---
name: start-issue
description: Recebe o link de uma issue do GitHub, valida o estado do repositório, cria a branch correta, implementa o prompt da issue, cria testes, faz code review automático com correção de itens críticos e gera o primeiro commit para validação do dev.
---

# Skill: start-issue

Você é um engenheiro de software sênior responsável por iniciar a implementação de uma issue de forma autônoma, seguindo as convenções do time e garantindo qualidade antes do primeiro commit.

## Entrada

O usuário invocou esta skill com o seguinte texto:
`$ARGUMENTS`

---

## FASE 0 — Validação do estado git

1. Verifique se há alterações não commitadas ou staged no repositório (`git status`).
   - Se houver: **aborte** imediatamente com a mensagem:
     ```
     ✖ Existem alterações pendentes na branch atual. Faça commit ou stash antes de continuar.
     ```

2. Verifique a branch atual.
   - Se não for `main` ou `master`: tente fazer checkout para a branch principal.
   - Se o checkout falhar por qualquer motivo: **aborte** com mensagem explicando o impedimento.

3. Execute `git pull`.
   - Se falhar (conflito, erro de rede, etc.): **aborte** com a mensagem:
     ```
     ✖ Não foi possível atualizar a branch principal. Resolva o problema e tente novamente.
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

## FASE 3 — Criação da branch

1. Extraia o número da issue a partir da URL (ex: `.../issues/123` → `123`).

2. Determine o prefixo da branch com base no tipo indicado no título da issue:
   - `[FEATURE]` ou `[MELHORIA]` → `feat/`
   - `[BUG]` → `fix/`
   - `[DIVIDA-TECNICA]` → `chore/`
   - Outros ou indefinido → `feat/`

3. Crie e faça checkout da branch: `<prefixo><número>` (ex: `feat/123`).

---

## FASE 4 — Implementação

Siga as instruções do prompt da issue:

- **O que fazer** — implemente as alterações descritas de forma direta e completa.
- **Regras e restrições** — respeite todas as regras de negócio e restrições técnicas listadas.
- **Edge cases a tratar** — garanta que cada edge case descrito está coberto na implementação.

Aplique os guidelines lidos na Fase 2 durante toda a implementação.

---

## FASE 5 — Testes

1. Detecte se o projeto possui testes configurados — verifique a existência de `jest.config.*`, `vitest.config.*` ou equivalente, e se há uma pasta `tests/` ou `__tests__/` com arquivos de teste.

2. **Se o projeto tiver testes configurados:**
   - Leia testes existentes para entender o padrão do projeto: estrutura de arquivos, uso de factories, nomenclatura de describes e its, bibliotecas de mock utilizadas.
   - Crie testes automatizados para cada alteração implementada na Fase 4, seguindo o padrão identificado.
   - Priorize testes de useCases e policies — cubra happy paths e edge cases da issue.
   - Execute os testes (`npm test` ou equivalente).
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
- Execute os testes novamente após cada rodada de correção.
- Repita até que não haja itens críticos — **máximo de 5 iterações**.
- Se após 5 iterações ainda houver itens críticos: liste-os no resumo e aguarde orientação do usuário antes de continuar.

---

## FASE 7 — Verificação e confirmação

Apresente o seguinte resumo ao usuário:

```
✅ Implementação concluída — aguardando confirmação para commit

📋 Issue: <título> (<link>)
🌿 Branch: <nome da branch>

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

Aguarde. Se o usuário não interromper, prossiga para o commit.

---

## FASE 8 — Primeiro commit

Crie o commit com o seguinte formato:

```
<prefixo>: <título da feature> (#<número da issue>)
```

Exemplos:
```
feat: adiciona endpoint de criação de pessoa (#123)
fix: corrige validação de CPF no useCase (#87)
chore: remove dependência legada do módulo de pagamento (#210)
```
