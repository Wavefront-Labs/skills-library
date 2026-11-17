---
id: computing-software.systems-network-administration.immich.database-queries
name: database-queries
category: computing-software
field: systems-network-administration
product: immich
tags: [sql, asset-table, psql, checksum, duplicates]
level: advanced
status: docs-checked
description: "Connect to Immich's Postgres with psql and run read queries: find assets by name, path, ID or checksum, spot duplicates, list missing thumbnails."
sources:
  - https://docs.immich.app/guides/database-queries
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: investigate Immich data directly. The docs warn that editing the database directly can cause damage; prefer reads and keep a current backup.

Connect through the container:

```bash
docker exec -it immich_postgres psql --dbname=<DB_DATABASE_NAME> --username=<DB_USERNAME>
```

Use the values from your `.env`.

Find assets (note the quoted camelCase column names):

```sql
SELECT * FROM "asset" WHERE "originalFileName" LIKE 'PXL_%';
SELECT * FROM "asset" WHERE "originalPath" LIKE 'upload/library/admin/2023/%';
SELECT * FROM "asset" WHERE "id"::text LIKE '%ab431d3a%';
```

By checksum (SHA-1; compute with `sha1sum <filename>`):

```sql
SELECT * FROM "asset" WHERE "checksum" = decode('69de19c87658c4c15d9cacb9967b8e033bf74dd1', 'hex');
```

Counts by type:

```sql
SELECT "asset"."type", COUNT(*) FROM "asset" GROUP BY "asset"."type";
```

Assets without a thumbnail or preview file:

```sql
SELECT * FROM "asset"
WHERE (NOT EXISTS (SELECT 1 FROM "asset_file" WHERE "asset"."id" = "asset_file"."assetId" AND "asset_file"."type" = 'thumbnail')
   OR NOT EXISTS (SELECT 1 FROM "asset_file" WHERE "asset"."id" = "asset_file"."assetId" AND "asset_file"."type" = 'preview'))
AND "asset"."visibility" = 'timeline';
```

Other useful tables: `"user"`, `"tag"`, `"tag_asset"`, `"person"`, `"asset_exif"` and `"move_history"` (failed file movements). Custom settings are stored in `"system_metadata"` where `"key" = 'system-config'`, used only when no config file is in use.

## Checked

2026-11-03. Confirmed against the Immich docs (https://docs.immich.app/) by reading: guides/database-queries (all sections).
Removed or reworded: nothing needed removal.
Method: documentation only; no commands were run.
