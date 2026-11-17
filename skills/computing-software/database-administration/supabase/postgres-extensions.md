---
id: computing-software.database-administration.supabase.postgres-extensions
name: postgres-extensions
category: computing-software
field: database-administration
product: supabase
tags: [extensions, extensions-schema, pgtap, database-dev, create-extension]
level: intro
status: docs-checked
description: "Enable and disable Postgres extensions on Supabase, choose the extensions schema, avoid namespace conflicts, and add pure SQL extensions."
sources:
  - https://supabase.com/docs/guides/database/extensions
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: turn on extensions without polluting the database.

Enable in the Dashboard (Database page, Extensions in the sidebar) or with SQL. `create extension` is the equivalent of enabling; disable with `drop extension`:

```sql
create extension pgtap
with
  schema extensions;

drop
  extension pgtap;
```

Rules:
- Most extensions install under the `extensions` schema, which `public` can access by default.
- Do not create other objects in `extensions`; that pollutes the namespace.
- To restrict user access to tables an extension manages, install it in its own separate schema.
- Some extensions must use a fixed schema. `postgis_tiger_geocoder` creates a schema named `tiger`, so confirm you have no conflicting schema before enabling it.

Availability: Supabase preconfigures over 50 extensions. More can be installed through the database.dev package manager. Pure SQL extensions, including plpgsql ones, can be installed directly through the SQL editor or any Postgres client.

Upgrades: a new extension version needs a software upgrade started from General Settings. Restarting the server from that page also triggers the upgrade.

## Checked

2026-11-04: Read the Postgres Extensions Overview in full, including the SQL tab from the Markdown source on GitHub. Confirmed the SQL example, schema advice, the `postgis_tiger_geocoder` note, the over-50 count, database.dev and the upgrade steps. Added the Dashboard path.
Method: documentation only; no commands were run.
