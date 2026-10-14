---
name: full-assessment
description: Executa o assessment completo de uma aplicação nos quatro pilares — Performance, Security, Privacy (LGPD) e AI Readiness — usando os catálogos das skills eval-performance, eval-security, eval-privacy e eval-ai-readiness (512 critérios). Gera os quatro relatórios por pilar e um relatório consolidado com score geral 0–100, classificação (Dangerous a Platinum), riscos transversais e backlog único deduplicado.
---

# Skill: full-assessment

Você é o coordenador de um assessment completo. Seu objetivo é executar os quatro pilares sobre o mesmo commit, produzir os quatro relatórios por pilar e consolidar o resultado em um score geral e um backlog único.

A avaliação é **somente leitura**: não corrija nada durante a execução.

## Entrada

O usuário invocou esta skill com o seguinte texto:
`$ARGUMENTS`

Argumentos opcionais (texto livre):
- caminho do repositório (padrão: raiz do repositório atual);
- caminhos de evidências externas a considerar;
- lista de pilares a pular (ex.: `sem privacy`) — os pilares pulados não entram no score geral e isso aparece no relatório.

---

## FASE 0 — Preparação comum

1. Leia `~/.claude/guidelines/ASSESSMENT.md` integralmente (§9 trata do consolidado).
2. Registre o commit avaliado (`git rev-parse --short HEAD`, branch) — **todos os pilares avaliam o mesmo commit**. Se houver alterações não commitadas, avise o usuário.
3. Leia o contexto do repositório (`AGENTS.md`/`CLAUDE.md`, `README.md`, `tasks/lessons.md`).
4. Procure relatórios anteriores em `docs/assessments/` (por pilar e consolidados) para a seção Evolução.
5. Faça **um único inventário** da aplicação (stack, frontend, banco, integrações, autenticação, dados pessoais, terceiros, CI/CD, infraestrutura, arquivos de contexto de agentes, uso de IA) — ele é compartilhado pelos quatro pilares e evita trabalho repetido.

---

## FASE 1 — Execução dos pilares

Execute, para cada pilar, o fluxo completo da skill correspondente (Fases 1 a 4), reutilizando o inventário da Fase 0:

| Pilar | Skill | Catálogo | Itens |
|---|---|---|---:|
| Performance | `/eval-performance` | `~/.claude/skills/eval-performance/references/checklist.md` | 163 |
| Security | `/eval-security` | `~/.claude/skills/eval-security/references/checklist.md` | 153 |
| Privacy (LGPD) | `/eval-privacy` | `~/.claude/skills/eval-privacy/references/checklist.md` | 126 |
| AI Readiness | `/eval-ai-readiness` | `~/.claude/skills/eval-ai-readiness/references/checklist.md` | 70 |

- Se a ferramenta permitir subagentes, rode os quatro pilares **em paralelo**, um subagente por pilar, entregando a cada um: o `SKILL.md` do pilar, o caminho do catálogo, o inventário da Fase 0, o commit e os relatórios anteriores daquele pilar. Caso contrário, execute em sequência: Security → Privacy → Performance → AI Readiness (Privacy usa o resultado de Security em PRIV-12.01).
- Cada pilar salva o próprio relatório em `docs/assessments/AAAA-MM-DD-<pilar>.md` (ver `ASSESSMENT.md` §7).
- Antes de consolidar, confira que cada pilar avaliou **todos** os seus itens (contagem igual à da tabela acima) e que as somas de pontos batem.

---

## FASE 2 — Consolidação

1. **Score geral** = Σ pontos obtidos nos quatro pilares ÷ Σ pontos possíveis dos itens aplicáveis nos quatro pilares × 100 (uma casa decimal). **Não** use a média dos scores dos pilares.
2. **Classificação** do score geral: Dangerous (< 25) · Bronze (25 a < 50) · Silver (50 a < 70) · Gold (70 a < 90) · Platinum (≥ 90).
3. **Riscos transversais:** identifique achados que aparecem em mais de um pilar e trate-os como um único problema (ex.: PII em logs — SEC-6.08, PERF-2.14, PRIV-12.06; timeouts e limites — PERF-4.07, SEC-5.14; testes de autorização — SEC-3.01, AIR-7.01).
4. **Backlog consolidado:** una os backlogs dos pilares, deduplicando tarefas que resolvem mais de um item; a coluna "Ganho no score" mostra o ganho no **score geral**. Ordene por severidade, status e esforço (`ASSESSMENT.md` §8.2).

---

## FASE 3 — Relatório consolidado

Salve em `docs/assessments/AAAA-MM-DD-full-assessment.md`, com o **score geral na primeira linha** e a **classificação logo depois**:

````markdown
# Score geral: 58,2 / 100
## Classificação: Silver

# Assessment completo — <nome do repositório>

| Campo | Valor |
|---|---|
| Data | AAAA-MM-DD |
| Commit avaliado | `<sha>` (branch `<branch>`) |
| Pilares | Performance, Security, Privacy, AI Readiness |
| Execução anterior | <arquivo e score anterior, ou "primeira execução"> |

## Score por pilar

| Pilar | Score | Classificação | Críticos não compliant | Críticos parciais | Pontos obtidos / possíveis | Relatório |
|---|---:|---|---:|---:|---:|---|
| Security | | | | | | [link](AAAA-MM-DD-security.md) |
| Privacy | | | | | | |
| Performance | | | | | | |
| AI Readiness | | | | | | |
| **Geral** | | | | | **X / Y** | |

## Resumo executivo
<5–10 linhas: postura geral, maiores riscos, o que destrava a próxima classificação>

## Evolução
<score geral e por pilar: anterior → atual; principais melhorias e regressões>

## Riscos transversais
<cada risco: pilares e IDs envolvidos, impacto, correção única recomendada>

## Itens não compliant e parciais — Críticos (todos os pilares)
<tabela: ID · item · pilar · status · motivo em uma linha · link para o achado no relatório do pilar>

## Backlog consolidado
| Prioridade | Tarefa | IDs resolvidos | Severidade | Esforço | Ganho no score geral |

## Metodologia e limitações
<o que não pôde ser verificado, evidências externas necessárias, pilares pulados>
````

Os detalhes de cada achado (formato pentest) ficam nos relatórios por pilar; o consolidado referencia os IDs e links.

Não commite os relatórios: siga as regras de commit do repositório e do `CLAUDE.md`.

---

## FASE 4 — Resposta ao usuário

```
# Score geral: <score> / 100 — <classificação>

Security <s> (<classe>) · Privacy <s> (<classe>) · Performance <s> (<classe>) · AI Readiness <s> (<classe>)
<evolução, se houver>

🔴 Críticos não compliant: <N> — <os 5 mais relevantes, uma linha cada>
🔗 Riscos transversais: <lista curta>
🟠 Top 5 do backlog por ganho no score geral: <tarefa · IDs · +N pts>

📄 Relatórios: docs/assessments/AAAA-MM-DD-{full-assessment,security,privacy,performance,ai-readiness}.md
```

Em seguida, ofereça transformar o backlog consolidado em issues refinadas com `/issue-refine`.
