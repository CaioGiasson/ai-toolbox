# Contexto — ai-toolbox

> Sincronizado via `ai-toolbox` para `~/.claude/CONTEXT.md`.

## Sobre este repositório

O `ai-toolbox` é um conjunto de ferramentas de IA (instruções, guidelines e skills do Claude Code) para otimizar o desenvolvimento de software. Ele não pertence a nenhum produto ou sistema específico: o conteúdo aqui é genérico e reutilizável em qualquer projeto.

## Padrões de comunicação

- Issues e PRs em português.
- Commits em português, com prefixos de conventional commits em inglês (`feat:`, `fix:`, `chore:`, `refactor:`, etc.).
- Branches no padrão `tipo/descricao-curta` (ex: `feat/user-wallet`).

## Fluxo de trabalho

1. Branch a partir de `main` ou `develop` (depende do repositório).
2. PR com template definido no repositório.
3. Review obrigatório de ao menos 1 pessoa.
4. Merge commit (sem squash), conforme `DEVOPS.md`.

## Variáveis de ambiente

Sempre utilizar o arquivo `.env.example` como referência. Nunca commitar `.env` real.
