---
id: computing-software.devops-ci-cd.nx.nx-migrate-workflow
name: nx-migrate-workflow
category: computing-software
field: devops-ci-cd
product: nx
tags: [nx, nx-migrate, upgrade, migrations-json, dependencies, agentic]
level: practitioner
status: docs-checked
description: "Upgrade Nx with nx migrate: generate step, --include required/optional/all, --run-migrations, agentic flow, migrate defaults in nx.json, community plugins."
sources:
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/features/automate-updating-dependencies.mdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: update Nx, plugins, configs and source code in two reviewable phases.

Phase 1, generate:
```shell
nx migrate
```
Resolves the latest version, asks how far to jump when crossing several majors (one major at a time is safest), and which packages to include (the `--include` flag):
- `required`: the target package and packages it ships with (Nx and `@nx/*` plugins). Best default; keeps the PR small.
- `optional`: dependency updates those recommend (e.g. `vite` rather than `@nx/vite`); catch up later with `nx migrate --include=optional`.
- `all`: both.
Result: `package.json` updated and `migrations.json` written if migrations are pending. Nothing is installed and no other file touched. Review `package.json` for conflicting versions, edit, then install with your package manager (`npm install`, `yarn install`, `pnpm install`, `bun install`).

Phase 2, run:
```shell
nx migrate --run-migrations
```
Migrations run one at a time. Types: generator-based (deterministic), prompt-based (AI-aided), or hybrid. Generator-only ones run automatically and leave changes unstaged. If prompt/hybrid migrations are queued and a supported agent is installed (Claude Code, OpenAI Codex or OpenCode), Nx offers an agentic flow: one agent session, a commit per migration, and a final check that touched projects still lint, build and pass unit tests. Progress lives in `.nx/migrate-runs`; interrupted runs print a continue command. On the default branch pass `--create-commits` or `--no-create-commits`. In CI or with `--agentic=false`, prompt-based migrations are only listed.

Defaults in `nx.json`:
```json
{ "migrate": { "agentic": "claude-code", "createCommits": true, "commitPrefix": "chore(repo): apply nx migration " } }
```

Cleanup: delete `migrations.json` after committing, but keep it until all older branches merge so others can rerun it.
Community plugins: `nx migrate my-plugin`; list installed with `nx report`.
Keep `nx` and all `@nx/*` on one version; add plugins with `nx add <plugin>`, not manual edits.

## Checked

2026-11-07. Confirmed: the two phases, --include values, migrations.json, agentic flow, nx.json migrate defaults, cleanup and community plugin steps against the Automate updating dependencies page. Removed: an invented Verify step.

Method: documentation only; no commands were run.
