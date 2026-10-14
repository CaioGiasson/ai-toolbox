# Metodologia de Assessment de Aplicações

Base comum das skills `/eval-performance`, `/eval-security`, `/eval-privacy`, `/eval-ai-readiness` e `/full-assessment`. Cada skill traz o próprio catálogo de critérios em `references/checklist.md` (gerado a partir do *Checklist sênior para assessment de aplicações — v3*). Este arquivo define **como avaliar, pontuar e reportar**, para que execuções sucessivas sejam comparáveis e o score suba à medida que os problemas forem corrigidos.

---

## 1. Princípios

- **Evidência, não declaração.** Um item só é compliant com evidência verificável no repositório: código, configuração, pipeline, teste, script, IaC, relatório ou registro versionado. Fala do time, comentário "TODO" ou intenção não contam.
- **Severidade fixa.** A severidade vem do catálogo e **nunca** é reclassificada pelo avaliador. Isso garante que o score seja comparável entre execuções.
- **Mesmo critério sempre.** Itens são julgados pelo texto do catálogo. Se houver relatório anterior, o veredito anterior só muda quando a evidência mudou — e a mudança é explicada.
- **Somente leitura.** A avaliação não altera código, não roda migrations, não chama produção, não executa scripts destrutivos nem testes de carga contra ambientes compartilhados. Comandos locais seguros (lint, typecheck, testes unitários, build) podem ser executados.
- **Sem dados sensíveis no relatório.** Segredos, tokens e dados pessoais encontrados são citados por localização (arquivo:linha) e tipo, com o valor mascarado.

## 2. Status de cada item

| Status | Quando usar | Pontuação |
|---|---|---|
| **Compliant** | Todos os requisitos do critério estão atendidos e há evidência suficiente (ver §3). | 100% do peso |
| **Parcialmente compliant** | Parte relevante do critério está atendida, **ou** o controle existe mas falta a evidência exigida (ex.: código existe, mas não há teste em item Crítico/Importante), **ou** atende em parte dos componentes/rotas. | 50% do peso |
| **Não compliant** | O controle não existe, existe só em documentação quando o critério exige implementação, ou não foi possível encontrar evidência no repositório. | 0 |
| **N/A** | O item (ou a seção) é condicional (*Se: …*) e a condição comprovadamente não se aplica. Exige justificativa **e** evidência (ex.: busca feita sem ocorrências, inventário da stack). | Excluído do cálculo |

Regras adicionais:

- A condição escrita no título ou no início de uma seção (*Se: …*) vale para **todos** os itens da seção.
- **N/A sem evidência = Não compliant.**
- **Evidência externa.** Itens que dependem de algo fora do repositório (dados de produção, painel de observabilidade, contrato assinado, exercício de DR) só são compliant se houver registro versionado no repositório (ex.: `docs/`, `docs/assessments/evidencias/`) ou se o usuário indicar o caminho da evidência ao invocar a skill. Sem isso, marque **Não compliant** com a tag `evidência externa necessária` e explique na recomendação como registrar a evidência.
- Na dúvida entre dois status, escolha o mais conservador e registre a dúvida no item.

## 3. Evidência mínima por severidade

| Severidade | Evidência mínima para "Compliant" |
|---|---|
| Crítico, Importante | Implementação (código/config/pipeline) **e** prova de funcionamento: teste automatizado, gate de CI, medição ou execução reproduzível. Só documentação ⇒ no máximo Parcial. |
| Menor | Implementação ou documentação/registro versionado coerente com o código. |

Para itens de governança/processo (políticas, planos, RIPD, DRP), a evidência é o documento versionado **mais** o sinal de que é usado (registro de execução, data de revisão, vínculo com o código).

## 4. Pesos e score

| Severidade | Compliant | Parcialmente compliant | Não compliant |
|---|---|---|---|
| Crítico | 3 | 1,5 | 0 |
| Importante | 2 | 1 | 0 |
| Menor | 1 | 0,5 | 0 |

```
score = 100 × (Σ pontos obtidos) ÷ (Σ pontos possíveis dos itens aplicáveis)
pontos possíveis = 3 × críticos + 2 × importantes + 1 × menores   (itens N/A excluídos)
```

Arredonde o score para **uma casa decimal** (vírgula como separador). O relatório sempre mostra a tabela do cálculo, para que qualquer pessoa confira o número.

## 5. Classificação

| Score | Classificação |
|---|---|
| 0 a < 25 | **Dangerous** |
| 25 a < 50 | **Bronze** |
| 50 a < 70 | **Silver** |
| 70 a < 90 | **Gold** |
| ≥ 90 | **Platinum** |

## 6. Comparação com execuções anteriores

Antes de avaliar, procure relatórios anteriores do mesmo pilar em `docs/assessments/`. Se existir:

1. Use o veredito anterior como ponto de partida e reavalie **cada** item com a evidência atual.
2. Registre na seção **Evolução**: score anterior → atual, itens que melhoraram, itens que pioraram (regressões, sempre com causa) e itens novos/removidos do catálogo.
3. Um item só piora se a evidência deixou de existir ou se a avaliação anterior estava errada — nesse caso, diga explicitamente que é correção de avaliação.

## 7. Onde salvar

- Relatório por pilar: `docs/assessments/AAAA-MM-DD-<pilar>.md` na raiz do repositório avaliado (`<pilar>` ∈ `performance`, `security`, `privacy`, `ai-readiness`).
- Relatório consolidado: `docs/assessments/AAAA-MM-DD-full-assessment.md`.
- Se já existir arquivo com o mesmo nome, acrescente sufixo `-2`, `-3`… (nunca sobrescreva histórico).
- Não commite automaticamente: siga as regras de commit do repositório avaliado e do `CLAUDE.md`.

## 8. Formato do relatório (por pilar)

O **score é a primeira informação** do relatório e a **classificação vem logo depois**. Use exatamente esta ordem:

````markdown
# Score: 63,4 / 100
## Classificação: Silver

# Assessment de <Pilar> — <nome do repositório>

| Campo | Valor |
|---|---|
| Data | AAAA-MM-DD |
| Commit avaliado | `<sha curto>` (branch `<branch>`) |
| Catálogo | application-assessment v3 — <N> itens (<N aplicáveis>, <N N/A>) |
| Escopo | <stack detectada, componentes avaliados, o que ficou fora> |
| Execução anterior | <arquivo e score anterior, ou "primeira execução"> |

## Resumo

| Severidade | Compliant | Parcial | Não compliant | N/A | Pontos obtidos / possíveis |
|---|---:|---:|---:|---:|---:|
| Crítico | | | | | x / y |
| Importante | | | | | x / y |
| Menor | | | | | x / y |
| **Total** | | | | | **X / Y = score** |

Principais riscos (3–5 linhas, em linguagem de negócio).

## Evolução
<somente se houver execução anterior: score anterior → atual, melhorias, regressões>

## 1. Itens não compliant

### 1.1 Críticos
### 1.2 Importantes
### 1.3 Menores

## 2. Itens parcialmente compliant

### 2.1 Críticos
### 2.2 Importantes
### 2.3 Menores

## 3. Itens compliant
| ID | Item | Severidade | Evidência |

## 4. Itens N/A
| ID | Item | Justificativa | Evidência da não aplicabilidade |

## 5. Backlog sugerido
| Prioridade | ID | Título da tarefa | Severidade | Esforço | Ganho no score |

## 6. Metodologia e limitações
<comandos executados, o que não pôde ser verificado, evidências externas necessárias>
````

### 8.1 Formato de cada achado (não compliant e parcial)

Cada item não totalmente compliant é escrito como um achado de pentest, com informação suficiente para virar uma tarefa sem nova investigação:

```markdown
#### PERF-4.07 · Timeouts por dependência — Crítico · Não compliant

- **Critério:** <resumo fiel do critério do catálogo>
- **Situação encontrada:** <o que existe e o que falta, objetivo>
- **Motivo do status:** <por que não é compliant/parcial, citando a regra do §2/§3>
- **Evidência:** `src/services/Email.service.ts:42` — `fetch(url)` sem `signal`/timeout; busca `rg "fetch\(" src/` → 7 ocorrências, 5 sem timeout (lista abaixo)
- **Componentes afetados:** <arquivos, rotas, serviços>
- **Impacto / risco:** <consequência técnica e de negócio; cenário de exploração ou de falha>
- **Recomendação:** <passo a passo da correção no ponto certo (boundary correto), com exemplo de código quando útil>
- **Critério de reteste:** <o que precisa ser verdade para o item virar Compliant na próxima execução — ex.: teste X existe e passa; gate Y no CI>
- **Esforço estimado:** P (≤ 1 dia) | M (≤ 1 semana) | G (> 1 semana)
- **Referências:** <ID do catálogo + padrão externo: ASVS, OWASP, artigo da LGPD, Core Web Vitals…>
```

Para itens Parciais, explicite **o que já atende** e **o que falta**.

### 8.2 Backlog sugerido

Ordene por: severidade (Crítico → Menor), depois status (Não compliant antes de Parcial), depois esforço (P antes de G). A coluna **Ganho no score** mostra quantos pontos percentuais o score sobe se o item virar Compliant (`peso_faltante ÷ pontos possíveis × 100`). Agrupe itens que se resolvem com a mesma mudança e diga isso na tarefa.

## 9. Relatório consolidado (`/full-assessment`)

Mesma ordem: **score geral** primeiro, **classificação** logo depois. O score geral usa a mesma fórmula sobre **todos** os itens aplicáveis dos quatro pilares (soma dos pontos obtidos ÷ soma dos pontos possíveis), não a média dos scores. Em seguida: tabela por pilar (score, classificação, críticos abertos), riscos transversais (achados que aparecem em mais de um pilar, ex.: logs com PII em SEC-6.08, PERF-2.14 e PRIV-12.06), backlog consolidado deduplicado e links para os quatro relatórios por pilar.
