# ai-toolbox

Repositório de sincronização de contexto e skills compartilhadas do **Claude Code** para times de desenvolvimento, seguindo padrões de mercado.

## O que está aqui

| Arquivo / Pasta         | Destino após sync                    | Finalidade                                    |
|-------------------------|--------------------------------------|-----------------------------------------------|
| `CLAUDE.md`             | `~/.claude/CLAUDE.md`                | Comportamento, convenções e princípios        |
| `CONTEXT.md`            | `~/.claude/CONTEXT.md`               | Propósito do repo, comunicação e fluxo        |
| `guidelines/*.md`       | `~/.claude/guidelines/`              | Guidelines de desenvolvimento por tema        |
| `skills/<nome>/`        | `~/.claude/skills/<nome>/`           | Skills invocáveis via `/<nome>` no Claude Code (`SKILL.md` + arquivos de apoio, ex.: `references/`)|

## Setup inicial (uma vez por máquina)

```bash
git clone git@github.com:CaioGiasson/ai-toolbox.git ~/projects/ai-toolbox
cd ~/projects/ai-toolbox
npm install        # instala o husky e registra os hooks
npm run sync       # sincroniza imediatamente
```

> `~/projects` é só um exemplo de **pasta pai**: o diretório que contém os demais projetos. O `ai-toolbox` deve ficar no mesmo nível dos outros repositórios, diretamente dentro da pasta pai (ex: `~/projects/ai-toolbox`, `~/projects/boilerplate-webapp`), nunca dentro de outro repositório.

> O `npm install` já configura o Husky via o script `prepare`. A partir daí, cada `git pull` dispara o `post-merge` hook e roda o `sync.sh` automaticamente.

## Sincronização manual

```bash
npm run sync
# ou diretamente:
bash sync.sh
```

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
4. Quem usa o repositório recebe a skill automaticamente no próximo `git pull`.

A skill estará disponível no Claude Code via `/<nome-da-skill>`.

## Skills de assessment

| Skill | Avalia | Itens |
|---|---|---:|
| `/eval-performance` | Performance, escalabilidade, eficiência, CI/CD, FinOps | 163 |
| `/eval-security` | Segurança (preparação para pentest whitebox) | 153 |
| `/eval-privacy` | Conformidade LGPD e normas conexas | 126 |
| `/eval-ai-readiness` | Prontidão do repositório para agentes de IA | 70 |
| `/full-assessment` | Os quatro pilares + relatório consolidado | 512 |

Cada execução gera um relatório em `docs/assessments/AAAA-MM-DD-<pilar>.md` no repositório avaliado, que começa pelo score (0–100) e pela classificação (Dangerous, Bronze, Silver, Gold, Platinum). Em seguida vêm os itens não compliant, os parciais (Críticos, Importantes e Menores) e os compliant, além de um backlog sugerido. A metodologia está em `guidelines/ASSESSMENT.md`. Os catálogos são gerados a partir de `docs/application-assessment-v3.md` por `scripts/gen-assessment-catalog.py`.

## Como adicionar uma guideline

1. Crie um arquivo `.md` na pasta `guidelines/`.
2. Referencie-a no `CLAUDE.md` com o gatilho de leitura adequado.
3. Faça commit e push.

## Como remover ou renomear uma skill/guideline

O `sync.sh` só copia; não apaga nada por conta própria. Ao remover ou renomear, adicione o nome **antigo** ao `legacy.txt`:

```
skill create-issue
guideline ANTIGO.md
```

Na próxima sincronização, o `sync.sh` apaga esses itens de `~/.claude`. Só os nomes listados são removidos, nomes inválidos (com caminho ou `..`) são ignorados, e itens que ainda existem no repositório nunca são apagados.

## Como atualizar os arquivos de contexto

Edite diretamente `CLAUDE.md` ou `CONTEXT.md` neste repositório, faça commit e push. Os demais usuários sincronizam automaticamente.

## Estrutura de pastas

```
ai-toolbox/
├── .husky/
│   └── post-merge              # hook disparado após git pull
├── guidelines/
│   ├── CONVENTIONS.md          # nomenclatura, código limpo, tipagem
│   ├── ARCHITECTURE.md         # camadas, fluxo, persistência
│   ├── ERRORS_AND_VALIDATION.md
│   ├── API_AND_SECURITY.md
│   ├── GUIA_REVISAO_PR_GERAL.md # checklist e formato de code review de PRs
│   ├── QUALITY.md              # observabilidade, testes, documentação, code review
│   ├── DEVOPS.md               # commits, CI/CD, branching, infra
│   └── ASSESSMENT.md           # metodologia, score e relatório das skills de assessment
├── docs/
│   └── application-assessment-v3.md # fonte dos catálogos de assessment
├── scripts/
│   └── gen-assessment-catalog.py    # gera skills/eval-*/references/checklist.md
├── skills/
│   ├── eval-ai-readiness/      # /eval-ai-readiness (SKILL.md + references/checklist.md)
│   ├── eval-performance/       # /eval-performance
│   ├── eval-privacy/           # /eval-privacy
│   ├── eval-security/          # /eval-security
│   ├── full-assessment/
│   │   └── SKILL.md            # /full-assessment
│   ├── issue-approve/
│   │   └── SKILL.md            # /issue-approve
│   ├── issue-refine/
│   │   └── SKILL.md            # /issue-refine
│   ├── example-skill/
│   │   └── SKILL.md            # /example-skill
│   ├── issue-start/
│   │   └── SKILL.md            # /issue-start
│   ├── issue-review/
│   │   └── SKILL.md            # /issue-review
│   └── issue-from-thread/
│       └── SKILL.md            # /issue-from-thread
├── CLAUDE.md
├── CONTEXT.md
├── legacy.txt                  # itens antigos a remover de ~/.claude no sync
├── sync.sh                     # script principal de sincronização
├── package.json
└── .gitignore
```
