# claude-sync

Repositório de sincronização de contexto e skills compartilhadas do **Claude Code** para o time BotPag.

## O que está aqui

| Arquivo / Pasta         | Destino após sync                    | Finalidade                                    |
|-------------------------|--------------------------------------|-----------------------------------------------|
| `CLAUDE.md`             | `~/.claude/CLAUDE.md`                | Comportamento, convenções e princípios        |
| `CONTEXT.md`            | `~/.claude/CONTEXT.md`               | Contexto de empresa, fluxo e serviços         |
| `ARCHITECTURE_MAP.md`   | `~/.claude/ARCHITECTURE_MAP.md`      | Mapa completo de microsserviços               |
| `guidelines/*.md`       | `~/.claude/guidelines/`              | Guidelines de desenvolvimento por tema        |
| `skills/<nome>/SKILL.md`| `~/.claude/skills/<nome>/SKILL.md`   | Skills invocáveis via `/<nome>` no Claude Code|

## Setup inicial (uma vez por máquina)

```bash
git clone git@github.com:BotPag/claude-sync.git ~/botpag-projects/claude-sync
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

## Diagnóstico — hook post-merge não dispara

O hook `post-merge` depende do Git estar apontando para `.husky/` como diretório de hooks. Isso é configurado automaticamente pelo `npm install` (via script `prepare`), mas pode não ter sido executado após o clone.

**Verificar:**
```bash
git config core.hooksPath
# Deve retornar: .husky
```

**Corrigir manualmente:**
```bash
bash sync.sh
# O sync.sh detecta e configura o core.hooksPath automaticamente
```

Ou diretamente:
```bash
git config core.hooksPath .husky
```

Após isso, `git pull` passa a disparar o sync automaticamente.

## Como adicionar uma skill

Cada skill é um subdiretório dentro de `skills/` com um arquivo `SKILL.md` dentro. O nome do diretório define o comando de invocação.

```
skills/
└── minha-skill/
    └── SKILL.md      # invocada com /minha-skill
```

**Passos:**

1. Crie o diretório `skills/<nome-da-skill>/`.
2. Crie o arquivo `SKILL.md` dentro dele, seguindo o template em `skills/example-skill/SKILL.md`.
3. Faça commit e push.
4. O time recebe a skill automaticamente no próximo `git pull`.

A skill estará disponível no Claude Code via `/<nome-da-skill>`.

## Como adicionar uma guideline

1. Crie um arquivo `.md` na pasta `guidelines/`.
2. Referencie-a no `CLAUDE.md` com o gatilho de leitura adequado.
3. Faça commit e push.

## Como atualizar os arquivos de contexto

Edite diretamente `CLAUDE.md`, `CONTEXT.md` ou `ARCHITECTURE_MAP.md` neste repositório, faça commit e push. O restante do time sincroniza automaticamente.

## Estrutura de pastas

```
claude-sync/
├── .husky/
│   └── post-merge              # hook disparado após git pull
├── guidelines/
│   ├── CONVENTIONS.md          # nomenclatura, código limpo, tipagem
│   ├── ARCHITECTURE.md         # camadas, fluxo, persistência
│   ├── ERRORS_AND_VALIDATION.md
│   ├── API_AND_SECURITY.md
│   ├── QUALITY.md              # observabilidade, testes, documentação, code review
│   └── DEVOPS.md               # commits, CI/CD, branching, infra
├── skills/
│   ├── create-issue/
│   │   └── SKILL.md            # /create-issue
│   └── example-skill/
│       └── SKILL.md            # /example-skill
├── CLAUDE.md
├── CONTEXT.md
├── ARCHITECTURE_MAP.md
├── sync.sh                     # script principal de sincronização
├── package.json
└── .gitignore
```
