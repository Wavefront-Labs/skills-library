---
id: computing-software.systems-network-administration.immich.postgres-without-superuser
name: postgres-without-superuser
category: computing-software
field: systems-network-administration
product: immich
tags: [superuser, earthdistance, create-extension, vchord, reindex]
level: advanced
status: docs-checked
description: "Prepare a Postgres database for Immich without granting superuser: create the database, extensions, and update VectorChord manually with reindexing."
sources:
  - https://docs.immich.app/administration/postgres-standalone
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: let the Immich database user work without superuser privileges.

The docs mark this for advanced users only and say it often needs manual steps when Immich updates. Automated database backups still need superuser because they use `pg_dumpall`.

At a `psql` prompt as an administrator, prepare the database once:

```sql
CREATE DATABASE <immichdatabasename>;
\c <immichdatabasename>
BEGIN;
ALTER DATABASE <immichdatabasename> OWNER TO <immichdbusername>;
CREATE EXTENSION vchord CASCADE;
CREATE EXTENSION earthdistance CASCADE;
COMMIT;
```

VectorChord and pgvector must already be installed on the server, with `vchord.so` in `shared_preload_libraries`.

When you install a new VectorChord version you must update the extension yourself and rebuild the vector indexes. Connect to the Immich database and run:

```sql
ALTER EXTENSION vchord UPDATE;
REINDEX INDEX face_index;
REINDEX INDEX clip_index;
```

Then point Immich at the database with `DB_URL` in `.env` (see the pre-existing Postgres skill). The docs warn this method often requires manual intervention when updating Immich.

## Checked

2026-11-03. Confirmed against the Immich docs (https://docs.immich.app/) by reading: administration/postgres-standalone (Without superuser permission, Updating VectorChord).
Removed or reworded: the face_index/clip_index purpose and the new-extension-per-release claim.
Method: documentation only; no commands were run.
