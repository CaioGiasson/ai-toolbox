# Contexto — ai-toolbox

> Sincronizado via `ai-toolbox` para `~/.claude/CONTEXT.md`.

## Sobre este repositório

O `ai-toolbox` é um conjunto de ferramentas de IA (instruções, guidelines e skills do Claude Code) para otimizar o desenvolvimento de software. Ele não pertence a nenhum produto ou sistema específico: o conteúdo aqui é genérico e reutilizável em qualquer projeto.

## Padrões de comunicação

- Issues e PRs em português (pt-BR).
- Commits em português (pt-BR), com prefixos de conventional commits em inglês (`feat:`, `fix:`, `chore:`, `refactor:`, etc.).
- Branches no padrão `tipo/descricao-curta` (ex: `feat/user-wallet`), vinculadas a uma issue.
- Código em inglês.

## Fluxo de trabalho

1. Sem tarefas ad-hoc: refinar → issue no board (com label) → branch → implementar → PR (`Closes #N`).
2. Branch a partir de `main` (`homolog`, quando existir, é só para QA integrado; não há `develop`).
3. Commit e push na branch da issue ao concluir (ou em marcos lógicos), sem esperar pedido.
4. PR com template definido no repositório.
5. Review da PR (bloqueantes/importantes corrigidos, comentário de pós-review e label `Reviewed`) e check de CI verde antes do merge.
6. Merge conforme `DEVOPS.md` (squash preferido, salvo padrão diferente do repositório).

## Variáveis de ambiente

Sempre utilizar o arquivo `.env.example` como referência. Nunca commitar `.env` real.
