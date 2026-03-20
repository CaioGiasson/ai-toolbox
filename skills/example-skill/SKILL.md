---
name: example-skill
description: Exemplo de skill compartilhada. Substitua pelo conteúdo real e renomeie o arquivo.
---

# Como criar uma skill

Skills são prompts reutilizáveis que o Claude Code pode invocar via `/nome-da-skill`.

## Estrutura mínima

```markdown
---
name: nome-da-skill
description: O que essa skill faz (usado para autocompletar e seleção).
---

Instruções detalhadas para o Claude executar a skill...
```

## Boas práticas

- Um arquivo `.md` por skill, nomeado igual ao `name` no frontmatter.
- Seja específico na `description` — ela é o que aparece no menu do Claude Code.
- Inclua exemplos de uso quando o comportamento não for óbvio.
- Skills de revisão de código, geração de testes e análise de PR são bons candidatos.

## Exemplo real

```markdown
---
name: review-pr
description: Faz code review de um PR seguindo os padrões do time BotPag.
---

Analise o diff do PR atual e forneça feedback estruturado em:
1. Corretude e lógica
2. Aderência aos padrões da stack (Node.js/TypeScript/Prisma)
3. Segurança (OWASP Top 10 básico)
4. Sugestões de melhoria (sem over-engineering)

Seja objetivo. Não repita o código sem necessidade.
```
