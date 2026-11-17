---
id: computing-software.database-administration.supabase.cli-config-api-and-db
name: cli-config-api-and-db
category: computing-software
field: database-administration
product: supabase
tags: [config-toml, cli-config, api, db-pooler, ports]
level: practitioner
status: docs-checked
description: "Supabase config.toml api and db sections with defaults: ports 54321 and 54322, schemas, max_rows, pooler, migrations and seed paths."
sources:
  - https://supabase.com/docs/guides/local-development/cli/config
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: configure the local stack's API and database in `supabase/config.toml`.

```toml
[api]
enabled = true
port = 54321
schemas = ["public", "storage", "graphql_public"]
extra_search_path = ["public", "extensions"]
max_rows = 1000

[db]
port = 54322
shadow_port = 54320
major_version = 15

[db.pooler]
enabled = false
port = 54329
pool_mode = "transaction"
default_pool_size = 20
max_client_conn = 100

[db.migrations]
schema_paths = []

[db.seed]
enabled = true
sql_paths = ["./seed.sql"]
```

Notes:
- `api.schemas`: schemas exposed in the API; `public` and `storage` are always included. `api.extra_search_path` adds schemas to every request's `search_path`; `public` is always included. `max_rows` is the maximum rows returned from a view, table or function.
- `db.shadow_port` is the port of the local shadow database.
- `db.major_version` is the Postgres major version (default 15) and has to match the remote database (check with `SHOW server_version;` there). `db.orioledb_version` has no default and requires `db.major_version` 15 or 17.
- The pooler (PgBouncer) is off by default; `pool_mode` defaults to `transaction` and accepts `transaction` or `session`. `default_pool_size` is server connections per user/database pair.
- `db.settings.*` (for example `work_mem`, `max_connections`, `statement_timeout`) has no default value; several, such as `max_connections`, need a database restart.
- `db.migrations.schema_paths` is an ordered list of declarative schema files, directories or globs relative to the `supabase` directory; only the legacy migra diff engine uses it.
- `[db.seed]` `enabled` runs seeds on start or reset; `sql_paths` is an array of files or glob patterns. Restart with `supabase stop` then `supabase start` after editing `config.toml`.

## Checked

2026-11-04: Read the Supabase CLI config reference (API and Database sections, with general notes) in full. Confirmed every default in the example block and the notes. Removed "used for diffing" and "caps rows per response", which the page words differently, and expanded notes with the page's wording.
Method: documentation only; no commands were run.
