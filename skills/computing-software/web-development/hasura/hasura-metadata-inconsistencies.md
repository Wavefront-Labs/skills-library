---
id: computing-software.web-development.hasura.hasura-metadata-inconsistencies
name: hasura-metadata-inconsistencies
category: computing-software
field: web-development
product: hasura
tags: [hasura, metadata, inconsistency, troubleshooting, cli]
level: practitioner
status: docs-checked
description: "Find and resolve Hasura metadata inconsistencies with the CLI inconsistency commands, reload, drop, and reset migrations from the live schema."
sources:
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/migrations-metadata-seeds/resolving-metadata-inconsistencies.mdx
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/migrations-metadata-seeds/resetting-migrations-metadata.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: fix metadata that is out of line with the database or Hasura configuration.

Causes listed on the page: schema changes made directly in the data source, manual edits to metadata files that do not match the database, failed migrations or incomplete operations, and conflicts in Remote Schemas.

CLI:
- `hasura metadata inconsistency status` logs `INFO metadata is consistent` when clean.
- `hasura metadata reload` is for changes made to the database outside the Console. It introspects the database again and does not modify or reset existing metadata configuration.
- `hasura metadata inconsistency list` prints NAME, TYPE, DESCRIPTION and REASON for each inconsistent object (for example a table that no longer exists in the source).
- Fix each object by hand or, if necessary, `hasura metadata inconsistency drop` removes all inconsistent objects from metadata.
- Resetting metadata (Console, or `clear_metadata` API) clears everything, including relationships and permissions, which you must then reconfigure.

The `reload_metadata` API accepts args `reload_remote_schemas`, `reload_sources` and `recreate_event_triggers`; it is an admin-only API (POST /v1/metadata).

Resetting a corrupted local migration state from the server:
1. `mv migrations migrations_backup`
2. `hasura migrate delete --all --server --database-name <DB>` (confirm with Y); leave out `--server` to also clean local files.
3. `hasura migrate create "init" --from-server --database-name <DB>` (Postgres only; exports only the public schema unless you add `--schema <name>`, repeatable).
4. `hasura migrate apply --version "<version>" --skip-execution --database-name <DB>` then `hasura metadata export`.
5. `hasura migrate status --database-name <DB>` should show the new migrations.

Gotcha: prefer reload, then manual fixes, before `drop` or a full reset, since reset clears all configuration.

## Checked
2026-11-07. Read in full both cited pages (resolving-metadata-inconsistencies.mdx, resetting-migrations-metadata.mdx; GitHub file view, no snippet files). The Console steps on the first page are images and were not visible in the fetched text.
Confirmed: every command, log line and API arg above.
Removed: the Console banner and "Settings -> Metadata Status" description, the `/healthz?strict=true` 500 claim, the claim that `drop` deletes dependent metadata, the invented Verify step (replaced by the page's `migrate status` step), "re-reads the database without changing metadata" (reworded to page text). Added causes, mark-applied and export steps and the `--schema` flag.
Method: documentation only; no commands were run.
