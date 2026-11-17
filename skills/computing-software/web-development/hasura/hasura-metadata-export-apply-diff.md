---
id: computing-software.web-development.hasura.hasura-metadata-export-apply-diff
name: hasura-metadata-export-apply-diff
category: computing-software
field: web-development
product: hasura
tags: [hasura, cli, metadata, export, diff, apply]
level: practitioner
status: docs-checked
description: "Export, apply, reload, clear and diff Hasura metadata with the CLI and know the metadata directory layout stored in hdb_catalog.hdb_metadata."
sources:
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/migrations-metadata-seeds/manage-metadata.mdx
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/migrations-metadata-seeds/overview.mdx
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/hasura-cli/commands/hasura_metadata_diff.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: version-control the GraphQL configuration.

Commands (run in the project dir; `md` is an alias for `metadata`):
- `hasura metadata export` writes the server metadata as YAML files into `metadata/`. There is no partial export.
- `hasura metadata apply` applies local metadata and completely replaces the metadata on that instance.
- `hasura metadata reload` is for metadata out of sync with the database schema, for example a column added with psql. It may reveal inconsistent objects, which you resolve or delete and then reload again.
- `hasura metadata clear` is irreversible; export first as a backup.
- `hasura metadata diff [file1] [file2] [--type unified-json|unified-yaml|yaml|json]` (marked PREVIEW) with no arguments compares the server with the metadata in the project directory; with two folders it compares them.

Directory layout: `databases/databases.yaml`, `databases/<db>/tables/*.yaml` (including `tables.yaml`), `actions.graphql`, `actions.yaml`, `allow_list.yaml`, `api_limits.yaml`, `cron_triggers.yaml`, `graphql_schema_introspection.yaml`, `inherited_roles.yaml`, `network.yaml`, `query_collections.yaml`, `remote_schemas.yaml`, `rest_endpoints.yaml`, `version.yaml`.

The server stores metadata as a single JSON blob in the table `hdb_metadata` in schema `hdb_catalog` of the metadata database. The Console and API export and import that JSON; the CLI uses YAML files.

Metadata API equivalents (admin only, POST to `/v1/metadata`): `export_metadata`, `replace_metadata`, `reload_metadata`, `clear_metadata`.

Gotcha: `metadata apply` loses any metadata that existed before. Dependent tables, views and functions must already exist in the database, so apply migrations before metadata. To roll metadata back, check out an earlier snapshot from version control.

## Checked
2026-11-07. Read in full all three cited pages (manage-metadata.mdx, overview.mdx, hasura_metadata_diff.mdx; GitHub file view, no snippet files).
Confirmed: commands, layout, storage table, API names.
Removed: `get_inconsistent_metadata` and the bulk wrappers (`bulk`, `bulk_atomic`, `concurrent_bulk`, `bulk_keep_going`) as not on these pages, the "re-reads the database and refreshes dependent objects" description of reload, "compares ... two sources" (page says two folders), and the invented Verify step. Added `databases.yaml` to the layout.
Method: documentation only; no commands were run.
