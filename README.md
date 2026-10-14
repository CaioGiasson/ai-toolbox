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

**[Install](#how-to-install) · [Before and after](#before-and-after) · [Catalog](#skill-catalog) · [How to use](#how-to-use) · [Update](#how-to-update) · [FAQ](#faq) · [Privacy](#privacy)**

</div>

---

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
