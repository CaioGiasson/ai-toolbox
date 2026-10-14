# Contexto — ai-toolbox

> Sincronizado via `ai-toolbox` para `~/.claude/CONTEXT.md`.

## Sobre este repositório

O `ai-toolbox` é um conjunto de ferramentas de IA (instruções, guidelines e skills do Claude Code) para otimizar o desenvolvimento de software. Ele não pertence a nenhum produto ou sistema específico: o conteúdo aqui é genérico e reutilizável em qualquer projeto.

## Regras de manutenção do ai-toolbox

Valem para qualquer agente ou pessoa que altere este repositório:

- **Renomear ou remover uma skill ou guideline:** o `sync.sh` só copia, nunca apaga por conta própria. Na mesma PR, adicione o nome **antigo** ao `legacy.txt` (`skill <nome>` ou `guideline <arquivo.md>`); o sync o removerá de `~/.claude`. Nunca apague itens de `~/.claude` manualmente nem edite o `sync.sh` para isso.
- **Criar uma skill ou guideline:** siga a `docs/TECNICO.md` (`skills/<nome>/SKILL.md`, referência no `CLAUDE.md` com o gatilho de leitura). Se o nome já constar no `legacy.txt`, remova a linha de lá.
- **Renomear uma skill:** atualize também as referências cruzadas em outras skills, na `docs/TECNICO.md` (estrutura de pastas) e no `README.md` (catálogo) e nos exemplos.
- **Arquivos de apoio de skills:** o `sync.sh` copia o diretório inteiro da skill (ex.: `references/`). Referencie esses arquivos pelo caminho `~/.claude/skills/<nome>/...`.
- **Catálogos de assessment** (`skills/eval-*/references/checklist.md`): nunca edite à mão. Atualize a fonte `docs/application-assessment-v3.md` (ou os complementos/guias no próprio script) e regenere com `python -X utf8 scripts/gen-assessment-catalog.py`. Mudar ID ou severidade de um item quebra a comparação de score entre execuções — registre a mudança na PR.
- **Antes de abrir a PR:** rode `bash -n sync.sh` se o script foi alterado e valide com `HOME` temporário, sem tocar no `~/.claude` real.

## Padrões de comunicação

- Issues e PRs em português (pt-BR).
- Commits em português (pt-BR), com prefixos de conventional commits em inglês (`feat:`, `fix:`, `chore:`, `refactor:`, etc.).
- Branches no padrão `tipo/descricao-curta` (ex: `feat/user-wallet`), vinculadas a uma issue.
- Código em inglês.

## Fluxo de trabalho

Board do ai-toolbox: [https://github.com/users/CaioGiasson/projects/6](https://github.com/users/CaioGiasson/projects/6) — é o board de referência mesmo sendo privado (o repositório é público); issues deste repo são vinculadas a ele.

1. Sem tarefas ad-hoc: refinar → issue no board (com label) → branch → implementar → PR (`Closes #N`).
2. Branch a partir de `main` (`homolog`, quando existir, é só para QA integrado; não há `develop`).
3. Commit e push na branch da issue ao concluir (ou em marcos lógicos), sem esperar pedido.
4. PR com template definido no repositório.
5. Review da PR (bloqueantes/importantes corrigidos, comentário de pós-review e label `Reviewed`) e check de CI verde antes do merge.
6. Merge conforme `DEVOPS.md` (squash preferido, salvo padrão diferente do repositório).

## Variáveis de ambiente

Sempre utilizar o arquivo `.env.example` como referência. Nunca commitar `.env` real.
