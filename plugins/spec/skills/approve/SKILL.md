---
name: approve
description: "Called by the user after the manual tests. Assumes the human tests were done and approved, and submits the change to a final layer of review. If there are blocking or important items, it only informs the user and takes no other action; if there are none, on GitHub it comments the result, applies the Reviewed label, merges the PR, moves the board item to Done and cleans up the branches; without GitHub it merges the branch locally (Git) or closes the record (no version control)."
---

# Skill: approve

You are a senior software engineer responsible for the **last layer of review** before the merge. The user invokes this skill **after running and approving the manual tests** of the task's test script — do not ask them to redo them.

Possible outcomes, and only one of them:

- **There are blockers or important items** → inform the user and **stop**. No other action (no fixes, no comments on the PR, no label, no push, no merge).
- **There are no blockers or important items** → complete the integration for the project's delivery mode (below) and clean up.

## Input

The user invoked this skill with the following text:
`$ARGUMENTS`

Accepts a **PR URL or number** (GitHub), a **branch name** (Git without GitHub) or the **path of a changelog file** (no version control). If empty, use the PR of the current branch (`gh pr view --json url`); without a PR, the current branch. If nothing identifiable exists, **stop** and ask for the reference.

## Shared rules

Before anything else, read `${CLAUDE_PLUGIN_ROOT}/references/WORKFLOW.md` and apply it (language, project context, tracker, mandatory documentation record, delivery modes, tooling). Write everything for people in the language of the user's request (English when it cannot be determined).

---

## PHASE 0 — Reading the guides

Read, before any other action:

1. `${CLAUDE_PLUGIN_ROOT}/references/PR_REVIEW_GUIDE.md`
2. The project's own conventions and context (`WORKFLOW.md` §2): `AGENTS.md`/`CLAUDE.md`/`CONTRIBUTING.md`, lint/format configuration, `tasks/lessons.md`, PR template, and any review rules (e.g., `docs/issue-workflow.md`, `.cursor/rules/`). **The project's rules win.** If the user has personal guidelines (e.g., `~/.claude/guidelines/`), read the applicable ones.

---

## PHASE 1 — Reading the change and preconditions

Decide the delivery mode (`WORKFLOW.md` §5).

**Mode A (PR):**

1. Identify `owner`, `repo` and the PR number. Fetch the title, description, source and base branches, changed files, commits, existing comments/reviews, labels and state (`OPEN`, `MERGED`, `CLOSED`).
   - If the PR is **not open**: inform and finish.
   - If it is a **draft**: inform and finish.

2. Read the **linked task** (`Closes #N` in the description): acceptance criteria, edge cases, order of commits and test script. If there is no linked task **and the project uses a board**, that is a **blocker** ("Change without a linked task"). Without a board, look for the refinement document instead; its absence (when the user did not ask not to document) is a **🟡 important** item.

3. Check CI and mergeability:
   ```bash
   gh pr checks <number>
   gh pr view <number> --json mergeable,mergeStateStatus,reviewDecision
   ```
   - A **failing** (or pending) CI check is a **blocker** — the PR cannot be merged. If it is pending, inform and finish without taking any other action.
   - Conflicts with the base (`mergeable: CONFLICTING`): **blocker**.

**Modes B–C:** the change is the branch against the base; read the refinement document and the commits. There is no CI to query unless the project documents a local equivalent (run it in Phase 2).

**Mode D:** the change is the changelog file plus the refinement document next to it.

---

## PHASE 2 — Checkout, build and tests

1. Confirm that the working tree is clean (`git status --porcelain`); if it is not, **abort** without switching branches. (Mode D: skip.)
2. Record `ORIGINAL_BRANCH`, update refs when there is a remote (`git fetch origin`) and switch to the change's branch (creating it with `--track` if it exists only on the remote; `git pull --ff-only` if it exists locally).
3. Install the dependencies and run the build and tests with the project's own tooling (`npm ci`/`npm install`, `npm run build`, `npm test`, plus lint and typecheck when they exist; or the equivalents for the stack). A failing build, lint, typecheck or test is a **blocker**.
4. Check whether the change has corresponding tests (absence on a critical flow is a blocker; on a secondary flow it is important).

---

## PHASE 3 — Review

Analyze all the changed files against the guides from Phase 0 and against the task (acceptance criteria, edge cases, out-of-scope items), including:

- Naming, clean code, typing (escape hatches such as `any`), functions (single responsibility, few parameters)
- Layering and structure per the project's rules; persistence only where the project allows it; transactions, soft delete, pagination
- Errors (the project's error types), validation at boundaries, security (authn/authz, secrets, sensitive data in logs)
- API contract: updated for every new/changed endpoint when the project keeps one (OpenAPI, request collections, inventory)
- Translations in all languages, when there is a UI
- Documentation: the refinement saved in the docs folder, README/docs/context files updated when applicable
- **Versioning:** at most **one** version bump in the change (more than one is important; no bump when the project versions itself is also important)
- Commits: follow the task's "Order of commits"; one subject per commit; messages in the project's commit convention
- Acceptance criteria met; nothing out of scope

Classify each finding as in `PR_REVIEW_GUIDE.md`:

- **🔴 Blocking** — bug, regression, vulnerability, serious layering violation, broken acceptance criterion, red CI, endpoint without a contract, missing critical test
- **🟡 Important** — real edge case, API/UI inconsistency, performance, maintainability, missing acceptance docs, insufficient tests
- **🟢 Suggestion / nit** — readability and non-critical refactors (they block nothing)

For each 🔴 and 🟡 prepare the **How to fix** block (where, what and why, step by step, before/after example, how to validate, suggested commit), detailed enough for a junior developer to fix — same format as the `/spec:review` skill.

---

## PHASE 4 — Decision

### Path A — there is at least one 🔴 or 🟡

1. Return to the original branch without changing anything:
   ```bash
   git restore .        # only tracked files changed by install/build/tests
   git switch "$ORIGINAL_BRANCH"
   ```
2. Inform the user, **in the chat only**:
   ```
   ⛔ Change not approved for merge — <N> blocking, <M> important

   🔴 [1] file.ts:42 — <short title>
       <description>
       How to fix: <complete block>

   🟡 [2] ...

   🟢 Suggestions (do not block): <short list>

   🔨 Build: ✅/❌  🧪 Tests: ✅/❌  🚦 CI: ✅/❌

   No other action was taken: no comments on the PR, no label, no push and no merge.
   Fix the items (or ask me to fix them) and run /spec:approve again.
   ```
3. **Stop.** Do not fix, do not comment, do not apply a label, do not merge.

### Path B — there is no 🔴 or 🟡

Go to Phase 5.

---

## PHASE 5 — Integration and cleanup (Path B only)

First restore the working tree and return to the original branch (as in Path A, step 1). Then, by delivery mode:

### Mode A — GitHub

1. **Comment on the PR** with the review result: what was reviewed, build/tests/CI, "no blocking or important items" and the 🟢 suggestions (if any) as an optional follow-up.

2. **`Reviewed` label:** apply it to the PR. If the label does not exist in the repository, create it (`gh label create Reviewed`) and then apply it.

3. **Merge** (only if the CI check is green and the PR is mergeable):
   ```bash
   gh pr merge <number> --squash --delete-branch
   ```
   - Use `--squash` unless the repository defines another standard (check the project's rules and the repository's merge settings).
   - If the merge fails (branch protection, conflict, pending check): **do not force**; report the reason and stop.

4. **Board:** if the project has a board (`WORKFLOW.md` §3), move the task to **Done** (`WORKFLOW.md` §3.1). If the board does not do it automatically and it cannot be done, say so in the summary.

5. **Branch cleanup:**
   - Find the base branch (`main`/`master`) and the PR's branch (`PR_BRANCH`). **Never** delete `main`, `master`, `homolog` or the base branch.
   - Update the local base:
     ```bash
     git switch "$BASE_BRANCH"
     git pull --ff-only origin "$BASE_BRANCH"
     ```
   - Delete the **local** branch: `git branch -d "$PR_BRANCH"`. Since a squash does not preserve history, `-d` may fail; in that case, confirm that the PR is `MERGED` (`gh pr view <number> --json state`) and only then use `git branch -D "$PR_BRANCH"`.
   - Delete the **remote** branch if it still exists (`--delete-branch` usually removes it already):
     ```bash
     git ls-remote --exit-code --heads origin "$PR_BRANCH" >/dev/null 2>&1 && git push origin --delete "$PR_BRANCH"
     git fetch --prune origin
     ```

6. Display the summary:
   ```
   ✅ PR approved and merged

   🔀 PR #<number>: <title>
   🏷 Label: Reviewed
   🔍 Review: no blocking/important items — <N> 🟢 suggestion(s)
   📌 Board: Done                       (or "no board")
   🌿 Branches removed: local ✔  remote ✔
   📍 Current branch: <BASE_BRANCH> (updated)
   ```

### Mode B/C — Git without GitHub, or another VCS

1. Merge the branch into the base **locally**, using the project's convention (squash or merge commit as documented; otherwise `--no-ff`), only if the build and tests are green:
   ```bash
   git switch "$BASE_BRANCH"
   git merge --no-ff "$PR_BRANCH"      # or: git merge --squash "$PR_BRANCH" && git commit
   ```
   If the merge conflicts or fails: **do not force**; abort the merge (`git merge --abort`), report and stop.
2. Delete the **local** branch once merged (`git branch -d "$PR_BRANCH"`; use `-D` only after confirming the merge result contains its changes).
3. If there is a remote: **do not push** on your own. Tell the user the base branch is ahead of the remote and ask whether to push, and whether to delete the remote branch.
4. Display the summary with the merge result, the branches removed and the current branch. For mode C, use that system's equivalents.

### Mode D — No version control

There is nothing to merge. Append a closing entry to the changelog file (`approved`, date, and the review result) and display:
```
✅ Change approved — record closed in <changelog path>
```
