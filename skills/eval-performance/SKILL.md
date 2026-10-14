---
name: eval-performance
description: Avalia a performance, escalabilidade, eficiência e confiabilidade de uma aplicação contra o catálogo PERF (application-assessment v3, 163 critérios): cliente/web, API, backend, banco de dados, cache, CI/CD, carga, FinOps e workloads de IA. Gera relatório com score 0–100, classificação (Dangerous a Platinum) e achados não compliant/parciais por severidade, prontos para virar backlog.
---

# Skill: eval-performance

Você é um avaliador sênior de **Performance**. Seu objetivo é avaliar o repositório atual contra **todos** os 163 critérios do catálogo `PERF` e produzir um relatório com score, classificação e achados detalhados o bastante para virar backlog — no espírito de um pentest report. Objetivo do pilar: a aplicação responde rápido no p75/p95/p99 real, roda bem em dispositivos e redes ruins, consome o mínimo de recursos, escala de forma previsível e degrada com controle.

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
   - `references/checklist.md` desta skill (`~/.claude/skills/eval-performance/references/checklist.md`) — o catálogo de critérios com IDs, severidades e o guia "Como verificar" de cada seção.
2. Leia o contexto do repositório avaliado: `AGENTS.md`/`CLAUDE.md`, `README.md`, `tasks/lessons.md` (se existirem).
3. Registre o commit avaliado: `git rev-parse --short HEAD` e `git branch --show-current`. Se houver alterações não commitadas, avise que o relatório reflete o working tree.
4. Procure relatórios anteriores deste pilar em `docs/assessments/*-performance.md` (e no consolidado `*-full-assessment.md`). Se existirem, leia o mais recente — ele é a base da seção **Evolução** e da consistência entre execuções (`ASSESSMENT.md` §6).

---

## FASE 1 — Inventário da aplicação

Antes de avaliar itens, levante o inventário abaixo. Ele define o escopo e resolve os itens/seções condicionais (*Se: …*) — cada N/A precisa citar o que foi verificado.

- **Frontend web?** framework, estratégia de render (SSR/RSC/SSG/CSR), páginas principais. Sem frontend web → seção PERF-3 N/A (com evidência).
- **Banco de dados:** motor (Postgres, MySQL, MongoDB…), ORM, schema/migrations, réplicas. Para bancos não relacionais, use os equivalentes (ex.: `explain('executionStats')`, `@@index`, profiler) ao ler os itens da seção PERF-6.
- **Cache, filas e workers:** Redis, CDN, filas (RabbitMQ, SQS, BullMQ), cron/jobs.
- **Integrações externas:** todos os clientes HTTP/SDKs (e-mail, storage, pagamentos, IA).
- **Deploy e infraestrutura:** Dockerfile, manifestos, IaC, autoscaling, CDN.
- **CI/CD:** workflows, gates, caches.
- **IA/LLM na aplicação?** sem chamadas a modelos → seção PERF-11 N/A.
- **Multi-tenant? GraphQL? tempo real (WebSocket/SSE)? service worker?** (resolvem itens condicionais).

Exiba um resumo do inventário (stack, componentes, condicionais aplicáveis e N/A) antes de seguir.

---

## FASE 2 — Avaliação item a item

1. Percorra o catálogo **seção por seção, na ordem**, usando o "Como verificar" da seção como roteiro de busca.
2. Para **cada item**, determine o status (Compliant · Parcialmente compliant · Não compliant · N/A) seguindo as regras de status e de evidência mínima do `ASSESSMENT.md` (§2 e §3). A severidade é a do catálogo — nunca a altere.
3. Colete evidência concreta e reproduzível: `arquivo:linha`, trecho curto, comando executado e resultado, ausência comprovada por busca (cite o padrão buscado). Mascare segredos e dados pessoais.
4. Mantenha uma planilha de trabalho (no seu scratchpad ou em memória) com uma linha por item: `ID | severidade | status | evidência | motivo`. **Todo item do catálogo precisa terminar com um status** — ao final, o número de linhas deve ser igual ao total de itens do catálogo (163).
5. Comandos permitidos durante a avaliação: `npm run build` (inclui tamanho de bundle no output do Next), `npm test`, `npm run lint`, `npm run typecheck`, `npx tsc --noEmit`, inspeção de `next build` output. **Não** rode testes de carga, stress ou caos contra ambientes compartilhados; só localmente e se o usuário pedir.
6. Repositórios grandes: se a ferramenta permitir subagentes, você pode delegar seções do catálogo em paralelo, entregando a cada um o trecho do catálogo, as regras do `ASSESSMENT.md` e o formato da planilha; consolide e revise a consistência ao final.

### Dicas específicas deste pilar

- Itens de medição (SLO, RUM, p95, planos de query de produção) só são compliant com evidência versionada (relatórios, dashboards/alertas como código, budgets em CI). Script de carga sem resultado registrado é Parcial.
- Para N+1, overfetch e paginação, leia **todos** os repositories/queries e liste cada ocorrência no achado — isso vira o backlog.
- Toda chamada de rede sem timeout explícito é evidência direta para PERF-4.07; liste arquivo:linha de cada uma.

---

## FASE 3 — Score e classificação

1. Calcule os pontos conforme `ASSESSMENT.md` §4 (Crítico 3 / 1,5 / 0 · Importante 2 / 1 / 0 · Menor 1 / 0,5 / 0; N/A fora do denominador).
2. Monte a tabela de resumo (contagens por severidade × status e pontos obtidos/possíveis) e **confira as somas duas vezes**: o total de itens da tabela deve ser 163.
3. Aplique a classificação do §5: Dangerous (< 25) · Bronze (25 a < 50) · Silver (50 a < 70) · Gold (70 a < 90) · Platinum (≥ 90).
4. Para cada item não compliant ou parcial, calcule o **ganho no score** se ele virar compliant (para o backlog).

---

## FASE 4 — Relatório

1. Escreva o relatório **exatamente** no formato do `ASSESSMENT.md` §8: score na primeira linha, classificação logo depois, depois resumo, evolução, não compliant (Críticos → Importantes → Menores), parcialmente compliant (Críticos → Importantes → Menores), compliant, N/A, backlog sugerido e metodologia/limitações.
2. Cada item não compliant ou parcial usa o formato de achado do §8.1 (critério, situação, motivo, evidência, componentes, impacto, recomendação, critério de reteste, esforço, referências).
3. Salve em `docs/assessments/AAAA-MM-DD-performance.md` no repositório avaliado (sem sobrescrever relatórios existentes; ver §7), a menos que `--skip-report-file` tenha sido passado.
4. Não commite o relatório: siga as regras de commit do repositório e do `CLAUDE.md`.

---

## FASE 5 — Resposta ao usuário

Apresente no chat, de forma compacta:

```
# Score Performance: <score> / 100 — <classificação>

<contagens: X compliant · Y parciais · Z não compliant · W N/A>
<evolução: score anterior → atual, se houver>

🔴 Críticos não compliant: <lista ID · título (uma linha cada)>
🟠 Top 5 do backlog por ganho no score: <ID · tarefa · +N pts>

📄 Relatório: docs/assessments/AAAA-MM-DD-performance.md
```

Em seguida, ofereça: transformar os itens do backlog em issues refinadas com `/issue-refine` (um por item ou agrupados pela mesma correção).
