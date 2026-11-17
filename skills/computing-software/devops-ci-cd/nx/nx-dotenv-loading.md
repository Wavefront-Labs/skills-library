---
id: computing-software.devops-ci-cd.nx.nx-dotenv-loading
name: nx-dotenv-loading
category: computing-software
field: devops-ci-cd
product: nx
tags: [nx, environment-variables, dotenv, env-files, configurations, batch-mode]
level: practitioner
status: docs-checked
description: "How Nx loads .env files per project, target and configuration, precedence and no-overwrite rules, atomized targets, batch mode and custom env files."
sources:
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/reference/environment-variables.mdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: predict which environment file wins when Nx runs a task.

Nx loads files in this order (30 candidates, missing ones skipped): project-root files first, then workspace-root files. Within each root, most specific first: `.env.[target].[config].local`, `.env.[target].[config]`, `.[target].[config].local.env`, `.[target].[config].env`, then the same four with only `[config]`, then only `[target]`, finally `.env.local`, `.local.env`, `.env`. Local files beat non-local.

Key rule: Nx never overwrites a variable already set. The first file to define it wins, so `apps/my-app/.env.local` beats `apps/my-app/.env`, and anything already in the process environment (shell, CI, `NODE_ENV`) beats every file. Package managers count: an npm `node-options` setting in `.npmrc` becomes `NODE_OPTIONS` under `npm run nx` / `npx nx` and beats `.env`; running `nx` directly uses `.env`.

Gotchas:
- Configuration files load only if that configuration is defined for the target. `nx build app --configuration development` uses `.env.build.development` only if the build target has `"configurations": { "development": {} }` (an empty object suffices); otherwise `.env.build`.
- Atomized targets (e.g. `e2e-ci--path/to/file`): Nx looks for the parent and non-atomized names (`.env.e2e-ci`, `.env.e2e`), not the full dynamic name.
- Batch mode tasks (Gradle and Maven by default) do not load task-specific files; they get the current environment plus root files such as `.env` and `.env.local`.
- Disable all file loading with `NX_LOAD_DOT_ENV_FILES=false`.
- Put app-specific files in the app directory; workspace-level files for workspace-wide settings like the Nx Cloud token.

Other file sources: `env-cmd -f .qa.env nx serve`, `dotenvx run --env-file=.qa.env -- nx serve`, or the run-commands `envFile` option.

Ad-hoc: Unix `NX_PUBLIC_API_URL=http://localhost:3333 nx build myapp`; cmd `set "VAR=x" && nx build myapp`; PowerShell `($env:VAR = "x") -and (nx build myapp)`.

## Checked

2026-11-07. Confirmed: the 30-file load order, no-overwrite rule, package manager and batch-mode notes, atomized targets, configurations, NX_LOAD_DOT_ENV_FILES and the cmd/PowerShell snippets against the Environment variables page. Removed: an invented Verify step.

Method: documentation only; no commands were run.
