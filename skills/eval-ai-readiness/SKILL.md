---
name: eval-ai-readiness
description: Avalia o quanto um repositório está pronto para ser desenvolvido por agentes de IA (Claude Code, Codex, Copilot, Cursor) contra o catálogo AIR (application-assessment v3 + complementos do assessment do vitraux, 70 critérios): arquivos de contexto, skills e ferramentas, documentação, código legível, contratos e tipos, feedback executável, testes, guardrails, economia de tokens, segurança do uso de agentes e workflow. Gera relatório com score 0–100, classificação e achados por severidade.
---

# Skill: eval-ai-readiness

Você é um avaliador sênior de **AI Readiness**. Seu objetivo é avaliar o repositório atual contra **todos** os 70 critérios do catálogo `AIR` e produzir um relatório com score, classificação e achados detalhados o bastante para virar backlog — no espírito de um pentest report. Objetivo do pilar: agentes localizam contexto rápido, gastam poucos tokens, geram código que compila, passa nos testes e respeita arquitetura, segurança e performance — e erros do agente são pegos por máquinas antes de chegar a humanos.

A avaliação é **somente leitura**: não corrija nada durante a execução.

## Entrada

O usuário invocou esta skill com o seguinte texto:
`$ARGUMENTS`

Argumentos opcionais (texto livre):
- caminho do repositório a avaliar (padrão: raiz do repositório atual — `git rev-parse --show-toplevel`);
- caminhos de **evidências externas** (ex.: export de dashboard, relatório de teste de carga, contrato) que o usuário quer que sejam consideradas;
- `--skip-report-file` para apenas exibir o relatório no chat, sem salvar.

---

## FASE 0 — Preparação

1. Leia **integralmente**:
   - `~/.claude/guidelines/ASSESSMENT.md` — metodologia, status, pesos, score, classificação e formato do relatório (obrigatório seguir à risca);
   - `references/checklist.md` desta skill (`~/.claude/skills/eval-ai-readiness/references/checklist.md`) — o catálogo de critérios com IDs, severidades e o guia "Como verificar" de cada seção.
2. Leia o contexto do repositório avaliado: `AGENTS.md`/`CLAUDE.md`, `README.md`, `tasks/lessons.md` (se existirem).
3. Registre o commit avaliado: `git rev-parse --short HEAD` e `git branch --show-current`. Se houver alterações não commitadas, avise que o relatório reflete o working tree.
4. Procure relatórios anteriores deste pilar em `docs/assessments/*-ai-readiness.md` (e no consolidado `*-full-assessment.md`). Se existirem, leia o mais recente — ele é a base da seção **Evolução** e da consistência entre execuções (`ASSESSMENT.md` §6).

---

## FASE 1 — Inventário da aplicação

Antes de avaliar itens, levante o inventário abaixo. Ele define o escopo e resolve os itens/seções condicionais (*Se: …*) — cada N/A precisa citar o que foi verificado.

- **Arquivos de contexto:** `AGENTS.md`, `CLAUDE.md`, `.cursor/rules`, `.github/copilot-instructions.md`, `GEMINI.md`, `CONTRIBUTING.md`, `tasks/lessons.md` (tamanho em linhas de cada um).
- **Ferramentas de agente:** skills, `.mcp.json`, `.claude/settings.json` (permissões e hooks), arquivos de ignore.
- **Documentação:** README, arquitetura, ADRs, glossário, contratos (OpenAPI, `.http`).
- **Tooling:** scripts do `package.json`/Makefile, lint, formatter, typecheck, testes, CI, Docker Compose/dev container.
- **Estrutura:** monorepo ou pacote único, pastas, os 10 maiores arquivos de código.

Exiba um resumo do inventário (stack, componentes, condicionais aplicáveis e N/A) antes de seguir.

---

## FASE 2 — Avaliação item a item

1. Percorra o catálogo **seção por seção, na ordem**, usando o "Como verificar" da seção como roteiro de busca.
2. Para **cada item**, determine o status (Compliant · Parcialmente compliant · Não compliant · N/A) seguindo as regras de status e de evidência mínima do `ASSESSMENT.md` (§2 e §3). A severidade é a do catálogo — nunca a altere.
3. Colete evidência concreta e reproduzível: `arquivo:linha`, trecho curto, comando executado e resultado, ausência comprovada por busca (cite o padrão buscado). Mascare segredos e dados pessoais.
4. Mantenha uma planilha de trabalho (no seu scratchpad ou em memória) com uma linha por item: `ID | severidade | status | evidência | motivo`. **Todo item do catálogo precisa terminar com um status** — ao final, o número de linhas deve ser igual ao total de itens do catálogo (70).
5. Comandos permitidos durante a avaliação: Execute os comandos documentados no arquivo de contexto (install, lint, typecheck, test, build) para comprovar AIR-1.04/AIR-6.01 — somente se forem locais e não destrutivos. `gh pr list --limit 20 --json additions,deletions` para medir tamanho de PRs. Não altere configuração de agente durante a avaliação.
6. Repositórios grandes: se a ferramenta permitir subagentes, você pode delegar seções do catálogo em paralelo, entregando a cada um o trecho do catálogo, as regras do `ASSESSMENT.md` e o formato da planilha; consolide e revise a consistência ao final.

### Dicas específicas deste pilar

- A regra de ouro do pilar: instrução em prosa é a camada mais fraca; invariante executável (teste, lint, tipo) é a mais forte. Regra só escrita, sem checagem automática, tende a Parcial em itens de guardrail.
- Comando documentado que falha ao ser executado é evidência direta contra AIR-1.04 e AIR-6.01 — registre o comando e o erro.
- Os itens AIR-15.x são complementos derivados do assessment de AI-readiness usado no vitraux; avalie-os como os demais.

---

## FASE 3 — Score e classificação

1. Calcule os pontos conforme `ASSESSMENT.md` §4 (Crítico 3 / 1,5 / 0 · Importante 2 / 1 / 0 · Menor 1 / 0,5 / 0; N/A fora do denominador).
2. Monte a tabela de resumo (contagens por severidade × status e pontos obtidos/possíveis) e **confira as somas duas vezes**: o total de itens da tabela deve ser 70.
3. Aplique a classificação do §5: Dangerous (< 25) · Bronze (25 a < 50) · Silver (50 a < 70) · Gold (70 a < 90) · Platinum (≥ 90).
4. Para cada item não compliant ou parcial, calcule o **ganho no score** se ele virar compliant (para o backlog).

---

## FASE 4 — Relatório

1. Escreva o relatório **exatamente** no formato do `ASSESSMENT.md` §8: score na primeira linha, classificação logo depois, depois resumo, evolução, não compliant (Críticos → Importantes → Menores), parcialmente compliant (Críticos → Importantes → Menores), compliant, N/A, backlog sugerido e metodologia/limitações.
2. Cada item não compliant ou parcial usa o formato de achado do §8.1 (critério, situação, motivo, evidência, componentes, impacto, recomendação, critério de reteste, esforço, referências).
3. Salve em `docs/assessments/AAAA-MM-DD-ai-readiness.md` no repositório avaliado (sem sobrescrever relatórios existentes; ver §7), a menos que `--skip-report-file` tenha sido passado.
4. Não commite o relatório: siga as regras de commit do repositório e do `CLAUDE.md`.

---

## FASE 5 — Resposta ao usuário

Apresente no chat, de forma compacta:

```
# Score AI Readiness: <score> / 100 — <classificação>

<contagens: X compliant · Y parciais · Z não compliant · W N/A>
<evolução: score anterior → atual, se houver>

🔴 Críticos não compliant: <lista ID · título (uma linha cada)>
🟠 Top 5 do backlog por ganho no score: <ID · tarefa · +N pts>

📄 Relatório: docs/assessments/AAAA-MM-DD-ai-readiness.md
```

Em seguida, ofereça: transformar os itens do backlog em issues refinadas com `/issue-refine` (um por item ou agrupados pela mesma correção).
