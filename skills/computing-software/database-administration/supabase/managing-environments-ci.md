---
id: computing-software.database-administration.supabase.managing-environments-ci
name: managing-environments-ci
category: computing-software
field: database-administration
product: supabase
tags: [environments, staging, ci-cd, github-actions, db-diff]
level: practitioner
status: docs-checked
description: "Manage Supabase local, staging and production with the CLI and CI: db diff, strict coverage, db push, required secrets and branch triggers."
sources:
  - https://supabase.com/docs/guides/deployment/managing-environments
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: promote schema changes through environments safely.

Commands:

```bash
supabase init
supabase login
supabase link --project-ref $PROJECT_ID
supabase db pull --remote
supabase migration new new_employee
supabase db reset
supabase db diff -f new_employee
supabase db diff --strict-coverage
supabase gen types typescript > types.gen.ts
supabase db push --yes --remote
supabase migration list --remote
```

Flags: `-f <name>` writes the diff to a migration file (without it, output goes to stdout); `--use-migra` generates the diff with the legacy engine for a single run; `--strict-coverage` fails the job when `pg-delta` finds schema objects it does not track, instead of warning (no effect on `migra`). `--remote` and `--yes` appear on `db push` in the page's CI and troubleshooting examples. `supabase db pull --remote` writes `supabase/migrations/<timestamp>_remote_schema.sql`.

Rules:
- Each developer, branch or git worktree can have its own local database.
- `pg-delta` is the default diff engine. `migra` applies only with `[experimental.pgdelta]` `enabled = false` in `config.toml` or `SUPABASE_EXPERIMENTAL_PGDELTA_ENABLED=false`; drop the `--strict-coverage` step if you use it.
- Generated migrations may include `GRANT` and `REVOKE`; remove them if permissions are unchanged and roles already hold them.
- The staging project must be new, not one already modified to match production.
- Prefer CI/CD to deploying production from a laptop.

GitHub Actions needs `SUPABASE_ACCESS_TOKEN` (a personal access token scoped to the projects the workflow deploys to), `SUPABASE_DB_PASSWORD` and `SUPABASE_PROJECT_ID`; the page recommends storing them as encrypted secrets. The workflows run `supabase link`, so the token needs Read access to Project Settings, API Keys and API Key Secrets. The page's examples map secrets named `STAGING_PROJECT_ID`, `STAGING_DB_PASSWORD`, `PRODUCTION_PROJECT_ID` and `PRODUCTION_DB_PASSWORD` onto those variables.

Workflows: CI runs on `pull_request` and `workflow_dispatch`, starts the local stack with `supabase db start`, runs the strict-coverage diff, and regenerates `types.gen.ts`, failing if it differs from the committed file. Staging deploys on pushes to `develop`; production on pushes to `main`. Each deploy job runs `supabase link --project-ref $SUPABASE_PROJECT_ID` then `supabase db push --yes --remote`.

Rebasing: after `git pull`, create a new migration with `supabase migration new dev_A`, rename your old file to that new timestamp, and run `supabase db reset`. If `reset` fails, resolve conflicts by editing the renamed migration file.

## Checked

2026-11-04: Read the Managing Environments guide in full from its Markdown source on GitHub (the rendered fetch returned only the last lines). Confirmed commands, the diff-engine notes, GRANT/REVOKE advice, the new-staging-project warning, secrets, token permissions and workflow triggers. Removed the unstated gloss for `--remote` and `--yes`; added the CI steps, secret mapping and rebasing steps. The page's prose refers to a `PROJECT_ID` variable while its YAML uses `SUPABASE_PROJECT_ID`; the skill uses the YAML names.
Method: documentation only; no commands were run.
