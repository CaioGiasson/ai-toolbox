---
name: eval-privacy
description: Avalia a conformidade de uma aplicação com a LGPD e normas conexas (ECA Digital, Marco Civil, resoluções da ANPD) contra o catálogo PRIV (application-assessment v3, 126 critérios rastreáveis a artigo de lei): papéis, inventário, bases legais, consentimento, dados sensíveis, crianças, transparência e cookies, direitos dos titulares, retenção, segurança, IA, terceiros, transferência internacional, incidentes, DPO e RIPD. Gera relatório com score 0–100, classificação e achados por severidade.
---

# Skill: eval-privacy

Você é um avaliador sênior de **Privacy (LGPD)**. Seu objetivo é avaliar o repositório atual contra **todos** os 126 critérios do catálogo `PRIV` e produzir um relatório com score, classificação e achados detalhados o bastante para virar backlog — no espírito de um pentest report. Objetivo do pilar: identificar toda lacuna que impeça a aplicação e a operação de estar em conformidade com a LGPD, avaliando o comportamento real do sistema (o que é coletado, enviado, armazenado e apagado), não apenas a política publicada.

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
   - `references/checklist.md` desta skill (`~/.claude/skills/eval-privacy/references/checklist.md`) — o catálogo de critérios com IDs, severidades e o guia "Como verificar" de cada seção.
2. Leia o contexto do repositório avaliado: `AGENTS.md`/`CLAUDE.md`, `README.md`, `tasks/lessons.md` (se existirem).
3. Registre o commit avaliado: `git rev-parse --short HEAD` e `git branch --show-current`. Se houver alterações não commitadas, avise que o relatório reflete o working tree.
4. Procure relatórios anteriores deste pilar em `docs/assessments/*-privacy.md` (e no consolidado `*-full-assessment.md`). Se existirem, leia o mais recente — ele é a base da seção **Evolução** e da consistência entre execuções (`ASSESSMENT.md` §6).

---

## FASE 1 — Inventário da aplicação

Antes de avaliar itens, levante o inventário abaixo. Ele define o escopo e resolve os itens/seções condicionais (*Se: …*) — cada N/A precisa citar o que foi verificado.

- **Dados pessoais no schema:** modelos/campos com dados pessoais e sensíveis (inclusive inferidos), por categoria de titular.
- **Coleta:** formulários, APIs, eventos de analytics, cookies e storage do navegador, SDKs e pixels.
- **Terceiros e regiões:** todo serviço que recebe dados (e-mail, storage, hosting, banco gerenciado, analytics, IA) e onde fica.
- **Documentos legais:** aviso de privacidade, termos, ROPA, RIPD, políticas de retenção e incidente, contato do encarregado.
- **Fluxos de direitos:** export, correção, exclusão, revogação/oposição.
- **Público:** produto direcionado ou de acesso provável por crianças/adolescentes? (PRIV-8). Órgão público? (PRIV-21). Decisões automatizadas? (PRIV-14). Usa consentimento ou legítimo interesse? (PRIV-5/6).

Exiba um resumo do inventário (stack, componentes, condicionais aplicáveis e N/A) antes de seguir.

---

## FASE 2 — Avaliação item a item

1. Percorra o catálogo **seção por seção, na ordem**, usando o "Como verificar" da seção como roteiro de busca.
2. Para **cada item**, determine o status (Compliant · Parcialmente compliant · Não compliant · N/A) seguindo as regras de status e de evidência mínima do `ASSESSMENT.md` (§2 e §3). A severidade é a do catálogo — nunca a altere.
3. Colete evidência concreta e reproduzível: `arquivo:linha`, trecho curto, comando executado e resultado, ausência comprovada por busca (cite o padrão buscado). Mascare segredos e dados pessoais.
4. Mantenha uma planilha de trabalho (no seu scratchpad ou em memória) com uma linha por item: `ID | severidade | status | evidência | motivo`. **Todo item do catálogo precisa terminar com um status** — ao final, o número de linhas deve ser igual ao total de itens do catálogo (126).
5. Comandos permitidos durante a avaliação: Leitura de código, schema, documentos legais e configuração; `npm test` para comprovar fluxos de direitos e retenção. **Não** acesse bancos com dados reais nem exporte dados de titulares.
6. Repositórios grandes: se a ferramenta permitir subagentes, você pode delegar seções do catálogo em paralelo, entregando a cada um o trecho do catálogo, as regras do `ASSESSMENT.md` e o formato da planilha; consolide e revise a consistência ao final.

### Dicas específicas deste pilar

- Divergência entre o aviso de privacidade e o comportamento observado no código é sempre achado de severidade do item ou maior — cite o trecho do aviso e o arquivo:linha que o contradiz.
- Cite o fundamento legal (artigo/resolução) de cada achado — ele já está no catálogo.
- Documento jurídico sem revisão formal não reprova itens técnicos, mas registre a limitação em "Metodologia e limitações".

---

## FASE 3 — Score e classificação

1. Calcule os pontos conforme `ASSESSMENT.md` §4 (Crítico 3 / 1,5 / 0 · Importante 2 / 1 / 0 · Menor 1 / 0,5 / 0; N/A fora do denominador).
2. Monte a tabela de resumo (contagens por severidade × status e pontos obtidos/possíveis) e **confira as somas duas vezes**: o total de itens da tabela deve ser 126.
3. Aplique a classificação do §5: Dangerous (< 25) · Bronze (25 a < 50) · Silver (50 a < 70) · Gold (70 a < 90) · Platinum (≥ 90).
4. Para cada item não compliant ou parcial, calcule o **ganho no score** se ele virar compliant (para o backlog).

---

## FASE 4 — Relatório

1. Escreva o relatório **exatamente** no formato do `ASSESSMENT.md` §8: score na primeira linha, classificação logo depois, depois resumo, evolução, não compliant (Críticos → Importantes → Menores), parcialmente compliant (Críticos → Importantes → Menores), compliant, N/A, backlog sugerido e metodologia/limitações.
2. Cada item não compliant ou parcial usa o formato de achado do §8.1 (critério, situação, motivo, evidência, componentes, impacto, recomendação, critério de reteste, esforço, referências).
3. Salve em `docs/assessments/AAAA-MM-DD-privacy.md` no repositório avaliado (sem sobrescrever relatórios existentes; ver §7), a menos que `--skip-report-file` tenha sido passado.
4. Não commite o relatório: siga as regras de commit do repositório e do `CLAUDE.md`.

---

## FASE 5 — Resposta ao usuário

Apresente no chat, de forma compacta:

```
# Score Privacy (LGPD): <score> / 100 — <classificação>

<contagens: X compliant · Y parciais · Z não compliant · W N/A>
<evolução: score anterior → atual, se houver>

🔴 Críticos não compliant: <lista ID · título (uma linha cada)>
🟠 Top 5 do backlog por ganho no score: <ID · tarefa · +N pts>

📄 Relatório: docs/assessments/AAAA-MM-DD-privacy.md
```

Em seguida, ofereça: transformar os itens do backlog em issues refinadas com `/issue-refine` (um por item ou agrupados pela mesma correção).
