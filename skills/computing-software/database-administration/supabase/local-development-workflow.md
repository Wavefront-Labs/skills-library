---
id: computing-software.database-administration.supabase.local-development-workflow
name: local-development-workflow
category: computing-software
field: database-administration
product: supabase
tags: [local-development, cli, db-pull, db-push, db-reset]
level: intro
status: docs-checked
description: "The Supabase CLI local-first workflow: init, start, migrations, db diff, db pull and push, link, with pg-delta and migra notes and caveats."
sources:
  - https://supabase.com/docs/guides/local-development/database-migrations
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: develop locally, then promote to a linked hosted project.

Commands:

```bash
supabase init
supabase start
supabase migration new create_employees_table
supabase db reset
supabase db diff --schema public
supabase login
supabase link --project-ref <project-id>
supabase db pull --remote
supabase db push --remote
supabase functions deploy <function_name>
supabase seed buckets --remote
supabase stop
```

Flags: `--schema <name>` syncs or diffs one schema; `--remote` is used with `db pull`, `db push` and `seed buckets` after `link`; `--project-ref` identifies the project (the ID is in the dashboard project URL).

Files: `supabase/config.toml`, `supabase/migrations/<timestamp>_<name>.sql`, `supabase/seed.sql`. Keep migrations in version control. `db reset` rebuilds the local database from current migrations and seed data.

Rules:
- `pg-delta` is the default diff engine; the legacy `migra` is used only if `config.toml` has an `[experimental.pgdelta]` section with `enabled = false`, or `SUPABASE_EXPERIMENTAL_PGDELTA_ENABLED=false` is set in the shell or a project `.env`. On `pg-delta`, a plain `db pull --remote` also captures triggers and RLS policies on `auth` tables and on `storage.objects` and `storage.buckets`. On `migra`, older CLIs that print a message that the `auth` or `storage` schema was excluded need one explicit `db pull --schema auth --remote` (or `storage`).
- `db pull --remote` writes remote-only changes to a `<timestamp>_remote_schema.sql` migration; skip it for an empty remote project.
- If the local migrations directory is empty, `db pull --schema` ignores `--schema`; pull twice.
- Buckets defined in `config.toml` are created by `supabase start` and `db reset`.
- Hosted settings cannot be changed in the local Dashboard; use the config file, then `supabase stop` and `start` after auth changes.
- Local is not as feature-complete as the platform; keep the CLI current, since it sets the local Studio version.

## Checked

2026-11-04: Read the page (cited URL now redirects to the "Local database migrations" tutorial; its Markdown source on GitHub was read because the rendered text lost the top). Confirmed every command, flag, file path, the diff-engine switches, the empty-migrations `--schema` caveat, bucket config and the local limitations. Named the exact engine switches and the pull behaviour per engine. The page points to a separate Local development workflow guide for the full end-to-end flow, which this skill does not cover.
Method: documentation only; no commands were run.
