---
id: computing-software.ai-ml-engineering.mastra.platform-deploy-environments
name: platform-deploy-environments
category: computing-software
field: ai-ml-engineering
product: mastra
tags: [mastra, platform, deploy, environments, mastra-deploy, preflight, regions, ci]
level: practitioner
status: docs-checked
description: "Deploy to the Mastra platform with mastra deploy: preflight checks, managed databases, environments, regions, variables, private npm packages, CI and migration."
sources:
  - https://mastra.ai/docs/mastra-platform/deploy
  - https://mastra.ai/docs/mastra-platform/environments
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: release a Mastra app with the single `mastra deploy` command and manage per-environment URLs, variables and databases.

## First deploy
```bash
mastra deploy
```
It builds, validates, creates the platform project (named from `package.json`) and the `production` environment on first run (prompts; `--yes` accepts defaults), deploys, streams build logs and prints the public URL once the new version serves traffic (typically 30 s to a few minutes). Log in is prompted if needed. A `.env` is optional; stored platform variables and managed database variables are used as-is; `--env-file` layers local values. It writes `.mastra-project.json` linking the directory to the project: commit it. Confirm by requesting `<url>/api/agents` (JSON list). Set up authentication before exposing endpoints publicly.

The older `mastra server deploy` / `mastra studio deploy` still work but are deprecated.

## Preflight
Runs before every deploy; only flags your own code.
- Local storage path (e.g. `file:./mastra.db`) is a hard block because the filesystem is ephemeral. The CLI offers to create and attach a managed database (`mastra env db create production --kind turso`); in non-interactive shells or `--yes` it prints that command. Localhost database URLs get a warning and the same offer (Neon vs Postgres prompt when both are available). A hard-coded path (`Build contains a host-local storage URL`) cannot be auto-fixed; guard it:
```typescript
new LibSQLStore({
  id: 'mastra-storage',
  url: process.env.TURSO_DATABASE_URL ?? 'file:./mastra.db',
  authToken: process.env.TURSO_AUTH_TOKEN,
})
```
- Missing environment variables: warning for variables your code reads but no source provides.
- `--skip-preflight` is an escape hatch. Dry run: `mastra lint --preflight` (sees only local env files, so it may report errors a real deploy would pass).

Background tasks: if the build finds `backgroundTasks.enabled: true`, a dedicated worker service needs a usable `REDIS_URL`; otherwise they run in-process. `--workers dedicated|in-process` skips the choice (`dedicated` fails without `REDIS_URL`). Removing `backgroundTasks` later removes the worker service. Dedicated workers are rolling out gradually; without access they run in-process.

Deploys replace the running process, which can interrupt streaming agent turns; do not rely on a raised `server.drainTimeout`. Use durable agents with persistent storage and cache or handle interrupted streams in the client.

## Environments
An environment has its own URL, variables, deploy history and optionally its own database. `production` is created by the first deploy; one per project.
```bash
mastra deploy --env staging            # creates after confirmation if missing
mastra env create eu-preview --type preview --region eu   # default type staging
mastra env list [--json]
mastra env deploys [staging]
mastra env delete staging              # removes its deploys and stored variables
```
Region (`us`/`eu`, e.g. `mastra deploy --env production --region eu`) is fixed at creation; databases are placed nearby and observability goes to the matching ingest region. Number of environments depends on plan. Deploy statuses: queued, (building for GitHub deploys), uploading, starting, deploying, running (shown only when serving traffic).

## Variables
Sources: managed (injected by platform/databases, not editable), stored (per environment in dashboard: Environments, env, Variables), local env files (`--env-file`, ambient `.env`, `.env.local`). A deploy of one environment uses only that environment's variables. Apply changes to a running service without redeploy: `mastra env restart staging`. Pull a view: `mastra env vars pull staging --output .env.staging` (managed values appear as name-only comments). Env vars do not override managed database variables; attach an environment-scoped database instead.

## Databases
Hosted databases are environment-scoped by default: `mastra env db create production --kind turso --name my-project-production-db`. `--shared` shares one across environments (`mastra env db create --kind turso --shared`); one database per provider per environment, and an existing shared one conflicts with a scoped one. `mastra env db delete` destroys the shared provider database and data; export first.

## Private npm packages
Store a read-only `NPM_TOKEN` on the project or environment; commit a token-free `.npmrc` keeping `${NPM_TOKEN}` literal (e.g. `@your-org:registry=https://npm.pkg.github.com` and `//npm.pkg.github.com/:_authToken=${NPM_TOKEN}`). Logs redact it; it is also injected at runtime as a normal env var. In a monorepo the project `.npmrc` wins over the root one. If `.npmrc` references it and it is unset, install fails.

## Project resolution and CI
Order: `MASTRA_PROJECT_ID`, `--project <name|slug|id>`, `.mastra-project.json`. `mastra env` commands resolve the same way (flag, env var, file). CI: set `MASTRA_PROJECT_ID` and `MASTRA_API_TOKEN`, run `mastra deploy --env production --yes`.

## Migrating from server/studio deploys
Legacy if the deploy log shows a Deprecated banner, last deploy used `@mastra/core` older than 1.44, or the org is not opted in. Steps: `npm install @mastra/core@latest` (needs `>= 1.44`; failure code `MASTRA_CORE_TOO_OLD`); replace both legacy commands with `mastra deploy` (builds once, deploys server and Studio shell); deploy once (auto-adopted, `production` created); move project-level variables to the right environment. Rollback: redeploy a prior successful artifact from the dashboard. The legacy commands will be removed in the next major version.

## Checked

Date: 2026-11-07

Every cited page was read against the skill's claims. No claims removed. Large pages (agents/processors, workflows control-flow) were read only in the sections the skill covers; sections not covered by the skill were not read in full.

Method: documentation only; no commands were run.
