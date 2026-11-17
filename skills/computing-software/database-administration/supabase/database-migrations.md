---
id: computing-software.database-administration.supabase.database-migrations
name: database-migrations
category: computing-software
field: database-administration
product: supabase
tags: [migrations, migration-new, migration-repair, declarative-schema, db-push]
level: practitioner
status: docs-checked
description: "Supabase migrations workflow: migration new and up, db diff, push with seed, history table, migration repair and declarative schemas."
sources:
  - https://supabase.com/docs/guides/deployment/database-migrations
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: version schema changes and apply them to remote projects.

```bash
supabase migration new create_employees_table
supabase migration up
supabase db reset
supabase db diff -f create_cities_table
supabase login
supabase link
supabase db push --remote
supabase db push --include-seed --remote
supabase migration list --remote
supabase db pull --remote
supabase db pull --schema auth --remote
supabase migration repair --status applied <migration-timestamp> --remote
supabase migration repair --status reverted <migration-timestamp> --remote
supabase db schema declarative sync
```

Files: `supabase migration new <name>` creates `supabase/migrations/<timestamp>_<name>.sql`; migrations apply in timestamp order. The seed script is `supabase/seed.sql`; `db push --include-seed` pushes it. Declarative schema files live in `supabase/schemas/` (see the pg-delta note below).

Workflow: write or diff a migration, test with `supabase db reset`, commit it (`git add supabase/migrations`), then `db push --remote`. Remote history is tracked in `supabase_migrations.schema_migrations`; use `migration repair` with `--status applied` or `reverted` to fix mismatches. `db pull --remote` writes a migration capturing the current remote schema; do this if someone changed the remote directly. On pg-delta it captures customisations in managed schemas such as a trigger on `auth.users` calling a `public` function or RLS policies on `storage.objects`; a trigger whose function lives inside `auth` or `storage` is excluded, so deliver it by migration. The page says older CLI versions excluded `auth` and `storage` entirely and printed a message; in that case run `db pull --schema auth --remote` and `db pull --schema storage --remote` once. `migration repair` only updates the tracking table; it does not apply or revert SQL.

The diff engine is pg-delta unless `[experimental.pgdelta]` has `enabled = false` in `config.toml` (legacy `migra`), or `SUPABASE_EXPERIMENTAL_PGDELTA_ENABLED=false` is set in your shell or a project `.env` file. On pg-delta, generate migrations from `supabase/schemas/` with `db schema declarative sync` and do not use `db diff` for that; on legacy migra `declarative sync` won't run and `db diff` reads `supabase/schemas/`.

Never change the remote schema directly (SQL editor or Table Editor): it bypasses migration history and `db push` then fails with sync errors. Only one person should run `db push` at a time; for automation the page suggests Branching or CI running `supabase db push --yes --remote`.

If a lock timeout error occurs, consider increasing `lock_timeout` in the migration file.

## Checked

2026-11-04: Read the Deploy database migrations guide in full and compared each command and rule. Confirmed the command list, file locations, history table, engine switch and repair behaviour. Corrected the over-broad "db pull captures auth and storage" claim and the lock_timeout wording to match the page.
Method: documentation only; no commands were run.
