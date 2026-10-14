<p align="right"><b>🇺🇸 English</b> · <a href="README.pt-BR.md">🇧🇷 Português</a></p>

<div align="center">

# Your Claude, with a team's way of working

**ai-toolbox teaches Claude to work the way your team does: from idea to task, from task to code, from code to review. You ask in plain language. It delivers.**

<table>
<tr>
<td align="center" width="25%"><h3>10 skills</h3>ready to use<br><sub><a href="#skill-catalog">see catalog</a></sub></td>
<td align="center" width="25%"><h3>4 health checks</h3>security, speed, privacy (LGPD) and AI readiness<br><sub><a href="#system-health-check">see how it works</a></sub></td>
<td align="center" width="25%"><h3>512 criteria</h3>assessed in the full health check<br><sub><a href="#system-health-check">see details</a></sub></td>
<td align="center" width="25%"><h3>1 message</h3>to install, right in the chat<br><sub><a href="#how-to-install">see installation</a></sub></td>
</tr>
</table>

**[Value](#why-it-matters-for-the-business) · [Install](#how-to-install) · [Before and after](#before-and-after) · [Catalog](#skill-catalog) · [How to use](#how-to-use) · [Update](#how-to-update) · [FAQ](#faq) · [Privacy](#privacy)**

</div>

---

## Why it matters for the business

**Less rework, more predictable delivery, and risks found before they become incidents.** ai-toolbox turns your team's way of working into something Claude repeats every day, for everyone.

| The everyday problem | What ai-toolbox does | What changes for the business |
|---|---|---|
| Vague requests cause back-and-forth and rework | Turns loose ideas and conversations into complete tasks, with a goal, rules and a test script | Fewer questions halfway through and deliveries that are easier to estimate |
| Everyone works their own way | Everyone follows the same rules, the same steps and the same quality standard | Predictable quality and faster onboarding of new people |
| Coding, testing and reviewing eats the team's time | Claude implements, writes tests, reviews itself and delivers a ready pull request | The team spends energy on decisions, not repetitive tasks |
| Security, performance and privacy (LGPD) risks show up late | Health checks with a 0 to 100 score and a prioritized problem list | You see risks before they become incidents and get an action plan in a clear order |
| Team knowledge lives in a few people's heads | Rules are recorded and versioned, and everyone gets updates with one message | Less dependence on key people |

**Who it's for:** managers and leaders who want predictability, product people who want well-defined tasks, and development teams who want more time for what matters.

## Before and after

<table>
<tr>
<th width="50%">Without ai-toolbox</th>
<th width="50%">With ai-toolbox</th>
</tr>
<tr>
<td valign="top">

> "We need a way to download the invoice."

One loose sentence. Everyone reads it differently, the developer asks questions for days, and the result depends on who picked up the task.

</td>
<td valign="top">

> A complete task on GitHub: goal, rules, what to change, how to test. Code ready for review and a test script in hand.

Claude studies the system, asks only what's missing and delivers to the team's standard.

</td>
</tr>
</table>

<sub>Illustrative example of the kind of result each skill produces.</sub>

**Same idea. Organized delivery, to the team's standard.**

## How to install

You don't need to open a terminal. You need three things installed: the **Claude app** (**Code** tab), **Git** and **Node.js**. If something is missing, Claude tells you and guides you.

1. Open the Claude app and go to the **Code** tab.
2. Choose the folder where your projects live (the "parent folder").
3. Paste this message into the chat and send it:

   > Install ai-toolbox: clone https://github.com/CaioGiasson/ai-toolbox.git into the current folder, run `npm install` and `npm run sync` inside it, and tell me when it's done.

4. Wait for Claude to confirm and open a **new conversation**. The skills now show up in the list.

One message. That's it.

<sub>Prefer the terminal? See the <a href="docs/TECNICO.md#instalação-via-terminal">technical installation</a> (in Portuguese).</sub>

## How to update

When the team ships news, open a conversation in the **Code** tab and send:

> Update ai-toolbox: go into the ai-toolbox folder, run `git pull` and `npm run sync`.

New skills and improvements arrive right away.

## How to use

In any conversation in the **Code** tab, type `/` and pick the skill from the list. Then write what you need in plain language.

> `/issue-refine` I want customers to be able to download their invoice as a PDF on the payments screen.

Or just describe what you want. Claude also suggests the right skill.

> The skills are written for a Portuguese-speaking team, so they work and answer in Brazilian Portuguese by default.

## Skill catalog

Ten skills in three groups. Each one says what it does and what result you get.

| Group | What it's for | Skills |
|---|---|---|
| **[From idea to task](#from-idea-to-ready-task)** | Turn loose conversation into a clear task | `/issue-from-thread` · `/issue-refine` |
| **[From code to delivery](#from-code-to-delivery)** | Build, review and finish | `/issue-start` · `/issue-review` · `/issue-approve` |
| **[System health check](#system-health-check)** | Measure project health, changing nothing | `/eval-security` · `/eval-performance` · `/eval-privacy` · `/eval-ai-readiness` · `/full-assessment` |

**A task's full path:** `/issue-from-thread` or `/issue-refine` → `/issue-start` → `/issue-review` → you test → `/issue-approve`.

### From idea to ready task

| Skill | What it does | What you get |
|---|---|---|
| **`/issue-from-thread`** | Reads an informal conversation (Slack thread link, Discord link or a `.md` file), drops the noise and separates decisions from doubts and opinions. | An organized task on the GitHub board, with no jokes, slang or loose information. |
| **`/issue-refine`** | Takes an idea described in a few lines, studies the system, asks focused questions and details everything. | A complete task on GitHub (goal, rules, what to change and how to test), clear enough for anyone to carry out. When several systems are involved, it creates one sub-task for each. |

### From code to delivery

| Skill | What it does | What you get |
|---|---|---|
| **`/issue-start`** | Takes a task link, moves it on the board to "In progress", builds the solution, writes the tests and reviews its own work. | A ready *pull request* (a request for review), with the code in organized steps and a test script for you to check. |
| **`/issue-review`** | Reviews a *pull request*: checks that everything requested was done, runs the tests and analyzes code quality. | Review comments posted on the right spot in the code, after you choose what to post. It only fixes something if you ask. |
| **`/issue-approve`** | Steps in after your manual tests and does the final review before wrapping up. | If all is well: a final comment, a "Reviewed" label, the delivery completed (*merge*) and the working copies cleaned up. If it finds a serious problem, it only tells you and touches nothing. |

### System health check

**They only read and assess. They change nothing in your project.** Each health check delivers a report with a **score from 0 to 100**, a **rating** and a **list of problems by priority**, ready to become an action plan. The report is saved in the assessed project's `docs/assessments` folder.

| Skill | What it assesses | Criteria | What you get |
|---|---|---:|---|
| **`/eval-security`** | Security: login, data protection, known weaknesses, exposed secrets. Works as preparation for a penetration test. | 153 | A security score and weak points by severity. |
| **`/eval-performance`** | Speed, ability to grow, stability and infrastructure costs. | 163 | Where the system is slow or expensive and what to prioritize. |
| **`/eval-privacy`** | Compliance with Brazil's LGPD: consent, data subject rights, personal data retention. | 126 | Legal gaps, each tied to its article of the law. |
| **`/eval-ai-readiness`** | How ready the project is to be developed with AI help: documentation, tests, organization. | 70 | What to improve so AI works faster and makes fewer mistakes. |
| **`/full-assessment`** | All four health checks at once. | 512 | The four reports plus an overall one, with a single score, risks that cut across areas and one list of priorities. |

How to read the score:

| Score | Rating |
|---|---|
| 90 to 100 | 🏆 Platinum |
| 70 to 89 | 🥇 Gold |
| 50 to 69 | 🥈 Silver |
| 25 to 49 | 🥉 Bronze |
| 0 to 24 | 🚨 Dangerous |

## What a health-check result looks like

An example **with made-up data** of `/eval-security` run on a project called `loja-online`. This is the reply that appears in the chat; the full report is saved to a file. Reports are generated in Portuguese, the language the skills were written in.

```text
# Score Security: 56,1 / 100 — Silver

63 compliant · 28 parciais · 46 não compliant · 16 N/A (153 critérios)
Evolução: primeira execução

🔴 Críticos não compliant (14):
  SEC-2.04 · Brute force, credential stuffing e evasão de rate limit
  SEC-2.05 · MFA
  SEC-2.08 · Recovery
  SEC-3.02 · BOLA/IDOR
  SEC-5.06 · XSS
  … e mais 9 (lista completa no relatório)
🟠 Top 5 do backlog por ganho no score:
  SEC-3.02 · Validar dono do pedido em todas as rotas /orders · +1,0 pt
  SEC-2.04 · Rate limit por conta e por IP no login · +1,0 pt
  SEC-2.08 · Token de recuperação de uso único e com expiração · +1,0 pt
  SEC-2.05 · Oferecer MFA para contas administrativas · +1,0 pt
  SEC-5.06 · Sanitizar o campo de comentário do produto · +1,0 pt

📄 Relatório: docs/assessments/2026-10-14-security.md
```

In plain English: the project scored **56.1 out of 100 (Silver)**; 14 critical problems are open, and the list says which ones to fix first and how many points each fix is worth.

<details>
<summary><b>See an excerpt of the saved report</b></summary>


````markdown
# Score: 56,1 / 100
## Classificação: Silver

# Assessment de Security — loja-online

| Campo | Valor |
|---|---|
| Data | 2026-10-14 |
| Commit avaliado | `a3f9c21` (branch `main`) |
| Catálogo | application-assessment v3 — 153 itens (137 aplicáveis, 16 N/A) |
| Escopo | API Node.js + Next.js + MongoDB; app mobile e LLM fora do escopo (N/A) |
| Execução anterior | primeira execução |

## Resumo

| Severidade | Compliant | Parcial | Não compliant | N/A | Pontos obtidos / possíveis |
|---|---:|---:|---:|---:|---:|
| Crítico | 20 | 9 | 14 | 5 | 73,5 / 129 |
| Importante | 36 | 17 | 28 | 8 | 89 / 162 |
| Menor | 7 | 2 | 4 | 3 | 8 / 13 |
| **Total** | 63 | 28 | 46 | 16 | **170,5 / 304 = 56,1** |

Principais riscos: qualquer cliente logado consegue ver pedidos de outros clientes
trocando o número na URL; o login não limita tentativas, o que permite adivinhar
senhas; contas administrativas não exigem segundo fator.

## 1. Itens não compliant

### 1.1 Críticos

#### SEC-3.02 · BOLA/IDOR — Crítico · Não compliant

- **Critério:** toda rota que recebe o identificador de um objeto confirma, no servidor, que o usuário autenticado tem direito a ele.
- **Situação encontrada:** as rotas de pedidos buscam o registro só pelo `id`, sem comparar com o usuário logado.
- **Motivo do status:** o controle não existe e não há teste negativo (ASSESSMENT §2 e §3).
- **Evidência:** `src/modules/orders/orders.controller.ts:58` — `orders.findById(req.params.id)` sem filtro por `userId`; busca `rg "findById\(req.params" src/` → 6 ocorrências, 5 sem verificação de dono.
- **Componentes afetados:** `GET /orders/:id`, `PATCH /orders/:id`, `GET /orders/:id/invoice` e outras 3 rotas.
- **Impacto / risco:** um cliente autenticado percorre ids sequenciais e lê nome, endereço e itens de pedidos de terceiros (vazamento de dados pessoais, com impacto na LGPD).
- **Recomendação:** buscar sempre por `{ id, userId }` na camada de repositório e responder 404 quando não encontrar. Adicionar teste em que o usuário A tenta ler o pedido do usuário B e recebe 404.
- **Critério de reteste:** teste negativo de acesso cruzado existe e passa no CI para todas as rotas listadas.
- **Esforço estimado:** P (≤ 1 dia)
- **Referências:** SEC-3.02 · OWASP API Security Top 10 (API1 — BOLA)

## 5. Backlog sugerido

| Prioridade | ID | Título da tarefa | Severidade | Esforço | Ganho no score |
|---:|---|---|---|---|---:|
| 1 | SEC-3.02 | Validar dono do pedido em todas as rotas `/orders` | Crítico | P | +1,0 |
| 2 | SEC-2.04 | Rate limit por conta e por IP no login | Crítico | P | +1,0 |
| 3 | SEC-2.08 | Token de recuperação de uso único e com expiração | Crítico | P | +1,0 |
| 4 | SEC-2.05 | Oferecer MFA para contas administrativas | Crítico | M | +1,0 |

*(…demais seções omitidas neste exemplo)*
````

</details>

After the report, Claude offers to turn the backlog items into tasks with `/issue-refine`.

## Before using the task skills

The `/issue-*` skills talk to GitHub. Claude uses the GitHub connection you already have and, if there is none, warns you and uses the GitHub CLI (`gh`). If something asks for access, just approve it when Claude asks.

## FAQ

**Do I need to know how to code?** Not to install it or to use task refinement and the health checks.

**Do the skills change my project without telling me?** The health checks never change anything. The others show what they will do and ask for confirmation on important decisions.

**The skill didn't show up in the list.** Open a new conversation after installing or updating.

**I want to create or edit skills, or understand the folder structure.** See the [technical documentation](docs/TECNICO.md) (in Portuguese).

## Privacy

- ai-toolbox is just a set of text files. Installing it **copies** those files to the `.claude` folder on your computer and sends nothing out.
- The skills run inside your Claude, with your account and your permissions.
- The `/issue-*` skills read and write on GitHub because that is their job, always with your account.

---

<div align="center">

**One team, one way of working. Everyone with their own Claude.**

<sub>
<a href="docs/TECNICO.md">Technical documentation (PT)</a> ·
<a href="https://github.com/CaioGiasson/ai-toolbox/issues">Issues</a>
</sub>

</div>
