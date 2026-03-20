# claude-sync

Repositório de sincronização de contexto e skills compartilhadas do **Claude Code** para o time BotPag.

## O que está aqui

| Arquivo / Pasta       | Destino após sync         | Finalidade                                      |
|-----------------------|---------------------------|-------------------------------------------------|
| `CLAUDE.md`           | `~/.claude/CLAUDE.md`     | Comportamento e convenções do Claude no time    |
| `CONTEXT.md`          | `~/.claude/CONTEXT.md`    | Contexto de empresa, fluxo e serviços           |
| `ARCHITECTURE_MAP.md` | `~/.claude/ARCHITECTURE_MAP.md` | Mapa completo de microsserviços           |
| `skills/*.md`         | `~/.claude/skills/`       | Skills compartilhadas invocáveis via `/skill`   |

## Setup inicial (uma vez por máquina)

```bash
git clone <url-do-repo> ~/botpag-projects/claude-sync
cd ~/botpag-projects/claude-sync
npm install        # instala o husky e registra os hooks
npm run sync       # sincroniza imediatamente
```

> O `npm install` já configura o Husky via o script `prepare`. A partir daí, cada `git pull` dispara o `post-merge` hook e roda o `sync.sh` automaticamente.

## Sincronização manual

```bash
npm run sync
# ou diretamente:
bash sync.sh
```

## Como adicionar uma skill

1. Crie um arquivo `.md` na pasta `skills/` seguindo o template em `skills/example-skill.md`.
2. Faça commit e push.
3. O time recebe a skill automaticamente no próximo `git pull`.

A skill ficará disponível no Claude Code via `/nome-da-skill`.

## Como atualizar os arquivos de contexto

Edite diretamente `CLAUDE.md`, `CONTEXT.md` ou `ARCHITECTURE_MAP.md` neste repositório, faça commit e push. O restante do time sincroniza automaticamente.

## Estrutura de pastas

```
claude-sync/
├── .husky/
│   └── post-merge          # hook disparado após git pull
├── skills/
│   └── *.md                # skills compartilhadas do time
├── CLAUDE.md
├── CONTEXT.md
├── ARCHITECTURE_MAP.md
├── sync.sh                 # script principal de sincronização
├── package.json
└── .gitignore
```
