---
id: computing-software.systems-network-administration.immich.vectorchord-migration
name: vectorchord-migration
category: computing-software
field: systems-network-administration
product: immich
tags: [pgvecto-rs, vectorchord, db-storage-type, docker-compose, migration]
level: advanced
status: docs-checked
description: "Migrate an Immich Docker Compose database from pgvecto.rs to VectorChord by swapping the Postgres image, with SSD or HDD storage type setting."
sources:
  - https://docs.immich.app/install/upgrading
  - https://docs.immich.app/administration/postgres-standalone
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: move off the deprecated pgvecto.rs extension to VectorChord.

If your compose file already uses `ghcr.io/immich-app/postgres` and you never set `DB_VECTOR_EXTENSION`, you are already on VectorChord. If you see a pgvecto.rs deprecation warning at startup, follow this.

Back up the database first. Then in `docker-compose.yml`, service `database`:

```diff
-   image: docker.io/tensorchord/pgvecto-rs:pg14-v0.2.0@sha256:...
+   image: ghcr.io/immich-app/postgres:14-vectorchord0.4.3-pgvectors0.2.0
```

Also remove the old `healthcheck` and the `command:` block (the new image includes them with extra tuning) and add `shm_size: 128mb`. If the database is not on SSD, add:

```
DB_STORAGE_TYPE: 'HDD'
```

If you used a non-default Postgres major version or pgvecto.rs version, adjust the image tag accordingly. Start Immich as usual; startup changes to the database can take seconds to minutes depending on hardware and library size.

Do not downgrade Immich below 1.133.0 after switching.

The new image contains pgvector and pgvecto.rs alongside VectorChord, so it can restore backups made with either. pgvecto.rs is only needed during migration or for restoring old backups.

For a shared standalone Postgres, follow the migration section of the standalone Postgres page instead; it covers installing both extensions, adding `vchord.so, vectors.so` to `shared_preload_libraries`, and waiting for the "Reindexed face_index" and "Reindexed clip_index" logs.

## Checked

2026-11-03. Confirmed against the Immich docs (https://docs.immich.app/) by reading: install/upgrading (Migrating to VectorChord, FAQ); administration/postgres-standalone (Migrating to VectorChord).
Removed or reworded: nothing needed removal.
Method: documentation only; no commands were run.
