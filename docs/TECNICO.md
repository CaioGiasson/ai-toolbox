# ai-toolbox — Documentação técnica

Este documento reúne o que a equipe de desenvolvimento precisa saber para instalar via terminal, manter e evoluir o `ai-toolbox`. Para a visão geral e o catálogo de skills, veja o [README](../README.md).

## O que é sincronizado

| Arquivo / Pasta   | Destino após sync          | Finalidade                                                                                          |
|-------------------|----------------------------|-----------------------------------------------------------------------------------------------------|
| `CLAUDE.md`       | `~/.claude/CLAUDE.md`      | Comportamento, convenções e princípios                                                              |
| `CONTEXT.md`      | `~/.claude/CONTEXT.md`     | Propósito do repo, comunicação e fluxo                                                              |
| `guidelines/*.md` | `~/.claude/guidelines/`    | Guidelines de desenvolvimento por tema                                                              |
| `skills/<nome>/`  | `~/.claude/skills/<nome>/` | Skills invocáveis via `/<nome>` (`SKILL.md` + arquivos de apoio, ex.: `references/`)                |

## Instalação via terminal

```bash
git clone git@github.com:CaioGiasson/ai-toolbox.git ~/projects/ai-toolbox
cd ~/projects/ai-toolbox
npm install        # instala o husky e registra os hooks
npm run sync       # sincroniza imediatamente
```

> `~/projects` é só um exemplo de **pasta pai**: o diretório que contém os demais projetos. O `ai-toolbox` deve ficar no mesmo nível dos outros repositórios, diretamente dentro da pasta pai (ex: `~/projects/ai-toolbox`, `~/projects/boilerplate-webapp`), nunca dentro de outro repositório.

O `npm install` configura o Husky via o script `prepare`. A partir daí, cada `git pull` dispara o hook `post-merge`, que roda o `sync.sh` automaticamente.

No Windows, o `sync.sh` precisa de um `bash` (o Git Bash, que vem com o Git for Windows).

## Atualização e sincronização manual

```bash
git pull           # o hook post-merge já sincroniza
npm run sync       # sincronização manual, se necessário
# ou diretamente:
bash sync.sh
```

## Estrutura de pastas

```
ai-toolbox/
├── .github/
│   └── workflows/
│       └── ci.yml              # valida sintaxe do sync.sh e sincronia dos catálogos
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
│   ├── TECNICO.md              # este documento
│   └── application-assessment-v3.md # fonte dos catálogos de assessment
├── scripts/
│   └── gen-assessment-catalog.py    # gera skills/eval-*/references/checklist.md
├── skills/
│   ├── eval-ai-readiness/      # /eval-ai-readiness (SKILL.md + references/checklist.md)
│   ├── eval-performance/       # /eval-performance
│   ├── eval-privacy/           # /eval-privacy
│   ├── eval-security/          # /eval-security
│   ├── full-assessment/        # /full-assessment
│   ├── issue-refine/           # /issue-refine
│   ├── issue-from-thread/      # /issue-from-thread
│   ├── issue-start/            # /issue-start
│   ├── issue-review/           # /issue-review
│   ├── issue-approve/          # /issue-approve
│   └── example-skill/          # modelo para criar novas skills
├── CLAUDE.md
├── CONTEXT.md
├── legacy.txt                  # itens antigos a remover de ~/.claude no sync
├── sync.sh                     # script principal de sincronização
├── package.json
└── .gitignore
```

## Como adicionar uma skill

Cada skill é um subdiretório dentro de `skills/` com um arquivo `SKILL.md`. O nome do diretório define o comando de invocação.

```
skills/
└── minha-skill/
    └── SKILL.md      # invocada com /minha-skill
```

1. Crie o diretório `skills/<nome-da-skill>/`.
2. Crie o `SKILL.md` dentro dele, seguindo o template em `skills/example-skill/SKILL.md`.
3. Faça commit e push.
4. Quem usa o repositório recebe a skill no próximo `git pull`.

Se o nome já constar no `legacy.txt`, remova a linha de lá. Arquivos de apoio (ex.: `references/`) são copiados junto; referencie-os pelo caminho `~/.claude/skills/<nome>/...`.

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

Ao renomear uma skill, atualize também as referências cruzadas em outras skills, no README e nos exemplos.

## Como atualizar os arquivos de contexto

Edite diretamente `CLAUDE.md` ou `CONTEXT.md`, faça commit e push. Os demais usuários sincronizam no próximo `git pull`.

## Skills de assessment — detalhes técnicos

| Skill | Avalia | Itens |
|---|---|---:|
| `/eval-performance` | Performance, escalabilidade, eficiência, CI/CD, FinOps | 163 |
| `/eval-security` | Segurança (preparação para pentest whitebox) | 153 |
| `/eval-privacy` | Conformidade LGPD e normas conexas | 126 |
| `/eval-ai-readiness` | Prontidão do repositório para agentes de IA | 70 |
| `/full-assessment` | Os quatro pilares + relatório consolidado | 512 |

- Cada execução gera um relatório em `docs/assessments/AAAA-MM-DD-<pilar>.md` no repositório avaliado (use `--skip-report-file` para apenas exibir no chat).
- O relatório começa pelo score (0–100) e pela classificação: Dangerous (0 a <25), Bronze (25 a <50), Silver (50 a <70), Gold (70 a <90), Platinum (≥ 90). Em seguida vêm os itens não compliant, os parciais (Críticos, Importantes e Menores) e os compliant, além de um backlog sugerido.
- A metodologia está em `guidelines/ASSESSMENT.md`.
- Os catálogos `skills/eval-*/references/checklist.md` **nunca** são editados à mão: são gerados a partir de `docs/application-assessment-v3.md` por `scripts/gen-assessment-catalog.py`:

  ```bash
  python -X utf8 scripts/gen-assessment-catalog.py
  ```

  Mudar ID ou severidade de um item quebra a comparação de score entre execuções — registre a mudança na PR. O CI falha se os catálogos divergirem da fonte.

## Skills de fluxo de issues — pré-requisitos

As skills `issue-*` usam por padrão o MCP do GitHub (`mcp__github__*`). Sem ele, caem para o GitHub CLI (`gh`) com um aviso. Configuração do MCP em `~/.claude/settings.json`:

```json
"mcpServers": {
  "github": {
    "type": "stdio",
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-github"],
    "env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "<seu-token>" }
  }
}
```

Fluxo completo: `issue-from-thread` → `issue-refine` → `issue-start` → `issue-review` → `issue-approve`.

## CI

O workflow `.github/workflows/ci.yml` roda em toda pull request e verifica a sintaxe do `sync.sh` e se os catálogos de assessment estão em sincronia com a fonte.
