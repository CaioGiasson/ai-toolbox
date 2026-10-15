# Criteria catalog — AI Readiness

> Derived from the *Senior checklist for application assessment — v3* (October 2026). This file is maintained directly in this repository. Item IDs, severities and criteria are the basis of the score and must stay stable between runs: changing an ID or a severity breaks score comparison across runs, so record any such change in the pull request.

**Severity (fixed per item):** `[B]` Blocking → **Critical** (weight 3) · `[A]` High → **Important** (weight 2) · `[M]` Medium and `[R]` Recommended → **Minor** (weight 1).

**Conditional items** (*If: …*): when the condition does not apply, mark **N/A with justification and evidence** (e.g., a code search with no hits). N/A without evidence counts as Non-compliant.

**Total items:** 70 — Critical: 6 · Important: 30 · Minor: 34. Maximum score (all applicable): 112.

## Pillar goal

> **Pillar goal:** the repository lets AI agents (Claude Code, Codex, Copilot, Cursor and similar) find context fast, spend few tokens, produce code that compiles, passes the tests, respects the architecture, performs well and does not introduce vulnerabilities — and **agent mistakes are caught by machines before they reach humans**.
>
> **Golden rule:** anything you would have to tell a new engineer more than once must live (a) in a short context file, (b) in a skill loaded on demand, or (c) — preferably — encoded as a test, lint rule or type that fails automatically. Prose instructions are the weakest layer; an executable invariant is the strongest.
>
> **Scope:** this pillar assesses the **repository and the engineering flow**. AI features of the application itself (chatbot, RAG, agents for users) are assessed in SEC-10, PERF-11 and PRIV-14.

## AIR-1. Context files and instructions

**How to verify:** Read `AGENTS.md`, `CLAUDE.md`, `.cursor/rules`, `.github/copilot-instructions.md`, `GEMINI.md`: size, content (map, stack, commands, constraints), duplication/contradiction, CODEOWNERS over these files, automatic verification in CI.

#### AIR-1.01 · Single, short entry point
**Critical** (weight 3, origin `[B]`)  
an `AGENTS.md` exists at the root (open standard maintained by the Agentic AI Foundation/Linux Foundation) with: the system's purpose in a few lines, a directory map, stack and versions, essential commands (install, run, test, lint, build), non-negotiable constraints and links to the source of truth. It is short (market reference: up to ~150 lines at the root) — not an encyclopedia.

#### AIR-1.02 · Compatibility across tools
**Minor** (weight 1, origin `[M]`)  
tools that read their own files (e.g., `CLAUDE.md`, `.github/copilot-instructions.md`, `.cursor/rules`, `GEMINI.md`) point to `AGENTS.md` (import, symlink or reference) instead of keeping diverging copies.

#### AIR-1.03 · Instructions at the right scope
**Important** (weight 2, origin `[A]`)  
global, per-stack, per-package and per-file-pattern rules are kept separate; nested `AGENTS.md` (e.g., `frontend/AGENTS.md`, `infra/AGENTS.md`) or glob-scoped rules are used when needed. Instructions neither duplicate nor contradict each other.

#### AIR-1.04 · Verified instructions
**Important** (weight 2, origin `[A]`)  
commands, paths and versions cited in the context files are tested automatically in CI (e.g., a script that runs the documented commands and checks that the paths exist). A context file that describes a structure that no longer exists is worse than none.

#### AIR-1.05 · Actionable, specific instructions
**Minor** (weight 1, origin `[M]`)  
rules say **what to do** and **how to verify** (“use `pnpm test --filter <package>`; never run the whole suite locally”), with good/bad code examples from the repository itself; no generic sentences (“write clean code”). Each rule has a short reason, so the agent generalizes correctly.

#### AIR-1.06 · Protection of context files
**Important** (weight 2, origin `[A]`)  
`AGENTS.md`, skills, rules and agent-tool configuration are under CODEOWNERS and require human review, since changing them changes the behavior of every agent (an attack and degradation vector).

## AIR-2. Skills, commands and tools for agents

**How to verify:** Look for skills (`.claude/skills`, `skills/`), generators (`plop`, scaffold scripts), MCP config (`.mcp.json`), hooks (`.claude/settings.json`, Husky/lint-staged) and documentation of dependencies at the version in use.

#### AIR-2.01 · Skills for recurring procedures
**Important** (weight 2, origin `[A]`)  
repetitive tasks with specific steps (create an endpoint, create a safe migration, add a feature flag, create a component with tests, investigate a performance regression, update a dependency) are packaged as skills (`SKILL.md` + scripts/references, Agent Skills standard) loaded on demand, instead of inflating the global context file.

#### AIR-2.02 · Deterministic generators and scaffolding
**Minor** (weight 1, origin `[M]`)  
standardized structures (module, endpoint, test, migration) are created by a generator/script in the repository, not “from memory” by the agent, ensuring conformity with conventions.

#### AIR-2.03 · MCP servers and tools with least privilege
**Important** (weight 2, origin `[A]`) · Conditional — *If: agents use MCP/external tools*  
MCP servers configured in the repository are inventoried, from a trusted source, version-pinned, minimally scoped (read-only by default, non-production environment) and use their own low-privilege credentials.

#### AIR-2.04 · Library documentation at the right version
**Minor** (weight 1, origin `[M]`)  
the agent has access to the documentation of the versions **actually used** of the main dependencies (versioned documentation in the repository, version-pinned links or an up-to-date documentation tool), reducing code based on obsolete APIs learned during training.

#### AIR-2.05 · Automatic hooks
**Minor** (weight 1, origin `[M]`)  
hooks of the agent tool and/or Git run formatting, lint and quick checks after edits and before commit, so the agent gets feedback without having to remember to run it.

## AIR-3. Business knowledge and documentation

**How to verify:** Look for the README, architecture, ADRs, glossary, business context, authorization matrix and non-functional requirements, documented and easy to find.

#### AIR-3.01 · Business context
**Important** (weight 2, origin `[A]`)  
the repository describes personas, business invariants, rules, permissions (authorization matrix — see SEC-3.01), events, states and integrations. Domain terms are consistent across code, docs, API and database (glossary).

#### AIR-3.02 · Architecture documentation
**Important** (weight 2, origin `[A]`)  
there are a `README`, an `ARCHITECTURE` document (components, boundaries, data flows, main decisions), recorded decisions (ADRs), contracts, the data schema and critical flows, versioned alongside the code.

#### AIR-3.03 · Documentation optimized for retrieval
**Minor** (weight 1, origin `[M]`)  
documents are clean Markdown, with descriptive headings, short self-contained sections, frontmatter/metadata (owner, review date, status), relative links and an index; this favors both the agent's search and internal semantic indexing.

#### AIR-3.04 · Explicit non-functional requirements
**Important** (weight 2, origin `[A]`)  
performance budgets and the security and privacy requirements relevant to the code (what is personal data, what must not be logged, default timeouts, payload limits) are documented so that the agent finds them when changing the corresponding area.

## AIR-4. Code readable by agents

**How to verify:** Assess the folder structure, import/architecture rules (`eslint-plugin-boundaries`, `dependency-cruiser`), file sizes (list the largest), isolated generated code, dead code, canonical examples cited in the instructions.

#### AIR-4.01 · Architecture with verifiable boundaries
**Important** (weight 2, origin `[A]`)  
modules have clear responsibilities, directional dependencies, explicit interfaces and predictable extension points. Layers and boundaries are verified by lint/structural tests (e.g., import rules, architecture tests). There are no circular imports or opaque abstractions.

#### AIR-4.02 · Findability
**Minor** (weight 1, origin `[M]`)  
names of files, functions and symbols are descriptive and consistent, allowing the code to be found by text search; a business rule has an identifiable owner; the same logic is not duplicated in several places.

#### AIR-4.03 · Size of files and functions
**Minor** (weight 1, origin `[M]`)  
very large files and functions are avoided (limits defined by lint), since they force the agent to read a lot of context for small changes and increase conflicts.

#### AIR-4.04 · Generated and vendored code isolated
**Minor** (weight 1, origin `[M]`)  
generated, vendored and minified code and large snapshots live in marked directories, are not edited by hand (“generated — do not edit” header) and can be regenerated by a documented command.

#### AIR-4.05 · Dead code and legacy paths removed
**Minor** (weight 1, origin `[M]`)  
dead code, expired flags and old parallel implementations are removed; if they coexist, they are marked obsolete with the replacement indicated — otherwise the agent copies the wrong pattern.

#### AIR-4.06 · Reference patterns
**Minor** (weight 1, origin `[M]`)  
for each common kind of artifact (endpoint, query, component, job, test), a canonical example is pointed to in the instructions (“follow `src/orders/` as a reference”).

## AIR-5. Contracts and types at the boundary

**How to verify:** Check `strict` in `tsconfig`, typecheck in CI, rules against `any`/`@ts-ignore`, boundary validation and contract synchronization (generated/verified OpenAPI), contract tests.

#### AIR-5.01 · Contracts and types at the boundary
**Important** (weight 2, origin `[A]`)  
inputs from HTTP, events, queues, files, the database and third parties are parsed/validated at the boundary; schemas, types, OpenAPI/GraphQL, migrations and examples are in sync (generated from a single source or verified in CI). Errors, nullability, units, timezone, idempotency and version compatibility are explicit.

#### AIR-5.02 · Strict typing
**Important** (weight 2, origin `[A]`)  
a type checker in strict mode (or the language's equivalent) runs in CI; use of escapes (`any`, `# type: ignore`, `@ts-ignore`, unchecked casts) is limited by lint and requires justification.

#### AIR-5.03 · Contract tests
**Minor** (weight 1, origin `[M]`)  
contracts between services and with the frontend are verified by tests (consumer-driven or schema diff), so the agent detects a compatibility break when changing an API.

## AIR-6. Executable feedback

**How to verify:** Run (when safe) the documented commands: install, lint, typecheck, test, build. Check whether there is a single verification command, per-file/package execution, a reproducible environment (Docker Compose/dev container) and pinned versions.

#### AIR-6.01 · Short, deterministic commands
**Critical** (weight 3, origin `[B]`)  
install, format, lint, test, build, run locally, seed data and validate work in a clean environment with one command each (e.g., `make check`, `pnpm verify`), documented in `AGENTS.md`. A single full local verification command exists.

#### AIR-6.02 · Targeted, fast checks
**Important** (weight 2, origin `[A]`)  
lint, types and tests of an isolated package/file can run in seconds; the agent does not have to run the whole suite on every change. Times are measured.

#### AIR-6.03 · Output readable by machines and agents
**Minor** (weight 1, origin `[M]`)  
lint, test and build failures show file, line, cause and the expected fix, without excessive noise (quiet/summary mode available), saving tokens when reading logs.

#### AIR-6.04 · Reproducible development environment
**Important** (weight 2, origin `[A]`)  
a dev container, Nix, Docker Compose or equivalent brings up the dependencies (database, cache, queue) with versioned sample data; no undocumented manual step is needed.

#### AIR-6.05 · Reproducibility and dependencies
**Important** (weight 2, origin `[A]`)  
runtime versions, package manager, lockfiles, toolchains, containers and local services are pinned or have an update policy. Builds are deterministic, fixtures and seeds are versioned, migrations are reversible. Dependencies and actions are pinned, scanned and updated by automation.

## AIR-7. Tests as specification

**How to verify:** Assess the test suite: types of tests present, mirroring, factories/fixtures, determinism (dates, network), mutation testing, a "test before fixing" rule in the instructions.

#### AIR-7.01 · Behavior coverage
**Important** (weight 2, origin `[A]`)  
there are unit, integration, contract, e2e and property tests for happy paths, errors, authorization, concurrency, limits and regressions; critical business rules have explicit coverage. Tests can be run per package/file and point (by name/description) to the rule they protect.

#### AIR-7.02 · Reliable tests
**Important** (weight 2, origin `[A]`)  
tests are deterministic (no dependence on time, external network or execution order), fast and free of known, unaddressed flakiness; a red test means a real problem — otherwise the agent learns to ignore failures.

#### AIR-7.03 · Test utilities
**Minor** (weight 1, origin `[M]`)  
data factories/builders, fixtures and role-based authentication helpers make it easier to write correct tests; there is an example test for each layer.

#### AIR-7.04 · Measured test quality
**Minor** (weight 1, origin `[R]`)  
beyond coverage, test effectiveness is evaluated (e.g., mutation testing on critical modules), avoiding generated tests that pass without verifying anything.

#### AIR-7.05 · Test before fixing
**Minor** (weight 1, origin `[M]`)  
the documented flow for bugs is: reproduce with a failing test → fix → the test passes. The agent's instructions require it.

## AIR-8. Quality, security and performance guardrails

**How to verify:** Read the CI and lint configs: SAST, secret scanning, SCA, architecture tests, budgets, rules for typical agent mistakes, new-dependency policy, protected areas in CODEOWNERS.

#### AIR-8.01 · Encoded invariants
**Critical** (weight 3, origin `[B]`)  
formatter, linter, type checker, dependency policy, SAST, secret scanning, SCA, security tests, performance budgets and architecture tests fail CI when invariants are violated. Lint messages indicate the expected fix. The principle is to encode invariants and allow local freedom.

#### AIR-8.02 · Rules for typical agent mistakes
**Important** (weight 2, origin `[A]`)  
there are lint/check rules for frequent mistakes in generated code in the project's context: network call without a timeout (PERF-4.07), query without pagination/limit, `SELECT *`, SQL concatenation, logging whole objects (PII leak), use of an obsolete internal API, unapproved new dependencies, disabling TLS verification, secrets in code, `eval`/`innerHTML`.

#### AIR-8.03 · New-dependency policy
**Important** (weight 2, origin `[A]`)  
adding a dependency requires justification and goes through an automatic check (license, maintenance, vulnerabilities, bundle size, real existence of the package — protection against “hallucinated”/slopsquatted packages).

#### AIR-8.04 · Protected areas
**Important** (weight 2, origin `[A]`)  
changes to authentication, authorization, cryptography, destructive migrations, CI/CD, IaC, agent context files and dependencies require human review by a specific owner (CODEOWNERS) and additional checks.

#### AIR-8.05 · Performance gates on the PR
**Minor** (weight 1, origin `[M]`)  
bundle size, number of queries per endpoint, benchmark test time and image size are compared with the main branch on the PR (see PERF-8.12), making agent-generated regressions visible.

## AIR-9. Context and token economy

**How to verify:** Check the ignore files for agents (`.cursorignore`, `.claudeignore`, `.aiexclude`, permissions in `.claude/settings.json`), the combined size of the context files, the split of docs by domain.

#### AIR-9.01 · Progressive context
**Important** (weight 2, origin `[A]`)  
the agent starts from a few pages (context file + index) and follows references as the task requires; long documentation is split and loaded on demand (skills, docs per domain); the whole repository is not injected into the prompt.

#### AIR-9.02 · Noise exclusion
**Important** (weight 2, origin `[A]`)  
files irrelevant to reasoning (lockfiles, builds, `dist/`, `node_modules`, vendored and minified files, large fixtures and snapshots, datasets, binaries, logs) are excluded from the agent's indexing/reading through the ignore files the tools support.

#### AIR-9.03 · Navigable monorepo
**Minor** (weight 1, origin `[M]`) · Conditional — *If: monorepo*  
the package map shows each package's responsibility and owner; workspace tooling allows operating on a single package; per-package instructions keep the agent from reading the whole repository.

#### AIR-9.04 · Context artifact size monitored
**Minor** (weight 1, origin `[M]`)  
the combined size of the always-loaded context files is measured in CI with a limit; growth requires review (move to a skill or an on-demand doc).

#### AIR-9.05 · Lean tool responses
**Minor** (weight 1, origin `[R]`)  
scripts and commands used by the agent have a summary output mode (e.g., failures only, diff only), avoiding dumping thousands of lines into the context.

## AIR-10. Safety of agent use in the repository

**How to verify:** Check the permissions configured for agents (command allowlist), blocked reading of `.env`, documented guardrails (no push to main, no prod), review of plugins/MCP, traceability of generated commits (`Co-Authored-By` trailer), AI usage policy.

> Reference: OWASP Top 10 for Agentic Applications 2026 (applied to the development flow itself).

#### AIR-10.01 · Isolated execution and least privilege
**Critical** (weight 3, origin `[B]`)  
agents run in a sandbox (container, VM or ephemeral remote environment) or in an isolated worktree/branch, with no production secrets, no broad personal credentials, with explicit command permissions (allowlist) and with network access restricted to what is necessary (package registries, documentation).

#### AIR-10.02 · Actions that require a human
**Critical** (weight 3, origin `[B]`)  
push to a protected branch, merge, deploy, running migrations in shared environments, infrastructure changes, package publishing and destructive operations require human approval; the agent has no credentials to do them alone.

#### AIR-10.03 · Instruction injection via repository content
**Important** (weight 2, origin `[A]`)  
the flow assumes that issues, PR comments, documents, dependencies, web pages and tool outputs may contain malicious instructions for the agent; agents that process external content (e.g., automatic triage of public issues) run with minimal permissions and with no access to secrets or write access to protected branches.

#### AIR-10.04 · Secrets out of reach
**Important** (weight 2, origin `[A]`)  
`.env` and local credential files are blocked from being read by the agent (ignore/permission configuration); examples use `.env.example` with no real values; secret scanning runs on every generated commit.

#### AIR-10.05 · Agent supply chain
**Important** (weight 2, origin `[A]`)  
third-party extensions, plugins, skills and MCP servers are reviewed before use, pinned by version and treated as untrusted code.

#### AIR-10.06 · Traceability of generated changes
**Minor** (weight 1, origin `[M]`)  
commits/PRs generated or co-authored by agents are identifiable (trailer, label or author), allowing quality analysis and audit.

#### AIR-10.07 · AI usage policy in development
**Important** (weight 2, origin `[A]`)  
it is defined which tools and providers are approved, what data may be sent to them (proprietary code, personal data in fixtures, production logs), retention and use for training by the provider (preference for contracts that forbid training), aligned with PRIV-14.05.

## AIR-11. Observability and environment operable by the agent

**How to verify:** Check whether the app starts in isolation per worktree (configurable ports/databases), documented diagnostic commands and automated UI verification (e2e/browser).

#### AIR-11.01 · Environment isolated per task
**Important** (weight 2, origin `[A]`)  
the application starts in an isolated worktree/environment (independent ports and databases), allowing parallel agent work without conflict.

#### AIR-11.02 · Diagnostics by command
**Minor** (weight 1, origin `[M]`)  
logs, local metrics, traces, DOM snapshots, screenshots and diagnostics are reachable through documented commands. The agent can reproduce a bug, observe the cause, apply a change and validate the affected metric.

#### AIR-11.03 · UI verification
**Minor** (weight 1, origin `[R]`) · Conditional — *If: frontend*  
there is an automated way for the agent to open the application, navigate and verify the result (e2e tests, automated browser, visual comparison), instead of declaring “it should work”.

## AIR-12. Plans, memory and decisions

**How to verify:** Look for versioned plans/specs, ADRs, `tasks/lessons.md` or equivalent and a specification-before-code flow.

#### AIR-12.01 · Versioned plans for complex tasks
**Minor** (weight 1, origin `[M]`)  
complex tasks have a plan with goal, non-goals, assumptions, affected files, risks, acceptance criteria and tests; plans are small and updated during execution.

#### AIR-12.02 · Persistent memory outside the ephemeral context
**Minor** (weight 1, origin `[M]`)  
concluded decisions (ADRs), technical debt, incidents and “known pitfalls” are recorded in indexed files; the agent resumes work without repeating discovery.

#### AIR-12.03 · Specification before code
**Minor** (weight 1, origin `[M]`)  
relevant features start with a short specification with verifiable acceptance criteria (which become tests), reducing ambiguity for the agent.

## AIR-13. Workflow and review

**How to verify:** Check PR/issue templates, typical PR size (`gh pr list`), documented human + automated review and checkpoints/rollback.

#### AIR-13.01 · Agent-friendly workflows
**Important** (weight 2, origin `[A]`)  
the PR template requires intent, scope, risk, tests, performance/security/privacy impact and evidence; PRs and commits are small; CI publishes artifacts and failures in a readable way; ephemeral environments allow per-branch previews. The flow offers checkpoints and rollback.

#### AIR-13.02 · Result validation
**Critical** (weight 3, origin `[B]`)  
before merge/deploy, the agent and a human reviewer check the diff, dependencies, migrations, authorization, sensitive data, performance, compatibility and observability. There are negative tests and adversarial review (including automated review by a second, independent agent/tool) for generated code.

#### AIR-13.03 · Limited change size
**Minor** (weight 1, origin `[M]`)  
there is a guiding limit on PR size; large agent-generated changes are split, since human review of huge diffs is ineffective.

## AIR-14. Measurement and continuous improvement

**How to verify:** Look for agent effectiveness metrics, records of systemic improvements after recurring mistakes, and reference tasks for evaluation.

#### AIR-14.01 · Effectiveness metrics
**Important** (weight 2, origin `[A]`)  
the team tracks time to locate context, acceptance/revert rate of generated PRs, defects and vulnerabilities introduced, flakiness, token cost per task, CI duration and rework. The goal is to reduce uncertainty and context cost, keeping quality, security, performance, privacy and maintainability as exit criteria.

#### AIR-14.02 · Learning loop
**Important** (weight 2, origin `[A]`)  
each recurring agent mistake produces a systemic fix: a lint rule, test, type, skill or instruction adjustment — in this order of preference. A record of these improvements exists.

#### AIR-14.03 · Evaluation on reference tasks
**Minor** (weight 1, origin `[R]`)  
a small set of tasks representative of the repository (e.g., “add a field to endpoint X with a test and a migration”) is used periodically to evaluate whether changes to instructions, skills or tools improve or worsen the result and the token consumption.

## AIR-15. Documentation add-ons and repository hygiene

**How to verify:** Check directly the files cited in each item (`CONTRIBUTING.md`, `.env.example` × `process.env.*` in the code, script index, i18n catalogs, `.github/ISSUE_TEMPLATE`, `docs/checkups/`, folder structure).

> Items incorporated from an AI-readiness assessment, not explicitly covered by the previous sections.

#### AIR-15.01 · CONTRIBUTING
**Minor** (weight 1, origin `[M]`)  
`CONTRIBUTING.md` (or an equivalent section) describes how to install, set up the environment, run tests and lint, name branches, write commits and open a PR — for humans and agents.

#### AIR-15.02 · Complete `.env.example`
**Important** (weight 2, origin `[A]`)  
every environment variable read by the code (`process.env.*` or equivalent) is in `.env.example` with a purpose comment and dummy values; no variable in use is missing from the example and no real value is versioned.

#### AIR-15.03 · Index of operational scripts
**Minor** (weight 1, origin `[M]`)  
each script in `package.json` (or Makefile/equivalent) and each script in `scripts/` is listed in an index (`scripts/README.md` or a README section) with its effect, risks and whether it is destructive/safe in production.

#### AIR-15.04 · Centralized text catalogs
**Minor** (weight 1, origin `[M]`) · Conditional — *If: the product is multilingual or has a UI with text*  
user-visible text lives in centralized, typed catalogs (e.g., next-intl, i18next), with keys present in all languages; there are no hardcoded UI strings in components.

#### AIR-15.05 · Issue templates
**Minor** (weight 1, origin `[M]`)  
issue templates (bug, feature) exist that require a goal, acceptance criteria and scope, and recent issues follow that format instead of one-liners.

#### AIR-15.06 · Assessments and reports with stable codes
**Minor** (weight 1, origin `[M]`)  
assessments and reports (security, privacy, performance, AI readiness) are versioned in the repository with stable IDs per item, allowing agents to cite and update the status without rewriting prose.

#### AIR-15.07 · Separation of app × operations × docs
**Minor** (weight 1, origin `[M]`)  
application runtime code, operations/CLI scripts and documentation live in separate, declared directories; operator scripts are not imported by the application code.
