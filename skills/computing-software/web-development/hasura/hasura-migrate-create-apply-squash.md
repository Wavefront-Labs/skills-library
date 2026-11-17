---
id: computing-software.web-development.hasura.hasura-migrate-create-apply-squash
name: hasura-migrate-create-apply-squash
category: computing-software
field: web-development
product: hasura
tags: [hasura, cli, migrations, squash, postgres]
level: advanced
status: docs-checked
description: "Create, apply, inspect and squash Hasura migrations with the CLI, including up and down counts, dry runs and marking squashed versions as applied."
sources:
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/migrations-metadata-seeds/manage-migrations.mdx
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/hasura-cli/commands/hasura_migrate_apply.mdx
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/hasura-cli/commands/hasura_migrate_squash.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: manage database schema changes as versioned SQL.

Migrations are Unix nanosecond timestamped directories (for example `migrations/default/1654698227514_create_table_public_address/`) holding `up.sql` and `down.sql`. Only changes made in the Console served by the Hasura CLI are tracked; the Console served by the server at /console is not tracked. SQL run from the Console SQL tab gets no `down.sql` statements, so write them by hand if needed.

Commands:
- `hasura migrate create "init" --from-server` creates an `up.sql` with the full current schema (Postgres only; other databases need hand-written migration files).
- `hasura migrate create <name> --database-name <DB>` bootstraps empty up and down files for hand-written SQL.
- `hasura migrate apply --database-name <DB>` applies pending migrations. Options on the CLI page: `--up N|all`, `--down N|all`, `--goto`, `--version`, `--type up|down` (default up), `--skip-execution`, `--dry-run` (prints the names of migrations that would be applied), `--all-databases`, `--no-transaction`, `--per-migration-transaction`, plus inherited `--endpoint` and `--admin-secret`.
- Roll back: `hasura migrate apply --version <V> --type down` or `hasura migrate apply --down 2`; rollbacks only work where down migrations exist.
- `hasura migrate status` lists each version with SOURCE STATUS and DATABASE STATUS (Present or Not Present).
- `hasura migrate delete --all --server --database-name <DB>` removes only the server's applied-record; leave out `--server` to also remove local files. It does not change the schema.

Squash (marked PREVIEW; correctness not guaranteed):

```bash
hasura migrate squash --name "<name>" --from <VERSION> --database-name <DB>
```
Other options: `--to` (default -1, meaning up to the latest) and `--delete-source` (deletes source files without confirmation). Because the squashed migration's changes already happened on the server, mark it applied without running it:

```bash
hasura migrate apply --version "<SQUASHED_VERSION>" --skip-execution --database-name <DB>
```
Gotcha: `--skip-execution` is what avoids errors and conflicts from re-executing statements already applied.

## Checked
2026-11-07. Read in full all three cited pages (manage-migrations.mdx, hasura_migrate_apply.mdx, hasura_migrate_squash.mdx; GitHub file view, no snippet files).
Confirmed: every command and flag above.
Removed: `--endpoint` as an apply-specific option (it is inherited), the invented Verify step including the "copy of the database" advice, and the claim that skipping the mark step reruns the SQL (reworded to what the page says). Added the manual create command, rollback commands and the delete semantics from the page.
Method: documentation only; no commands were run.
