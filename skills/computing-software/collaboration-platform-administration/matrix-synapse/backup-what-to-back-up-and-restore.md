---
id: computing-software.collaboration-platform-administration.matrix-synapse.backup-what-to-back-up-and-restore
name: backup-what-to-back-up-and-restore
category: computing-software
field: collaboration-platform-administration
product: matrix-synapse
tags: [matrix, synapse, backup, restore, pg-dump, pg-restore, signing-key, media-store, one-time-keys, e2e-one-time-keys-json]
level: practitioner
status: docs-checked
description: "Back up Synapse: config and signing key, pg_dump -Fc excluding e2e_one_time_keys_json, safe pg_restore into a fresh database, and which media store directories matter."
sources:
  - https://element-hq.github.io/synapse/latest/usage/administration/backups.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Keep backups against hardware failure and against corruption from bugs or admin error. Four things need covering.

**Configuration.** `homeserver.yaml` and the auxiliary files it references, such as the `log_config` file and `app_service_config_files`. Keeping them all in one directory (the docs mention `/etc/synapse`) makes this easier.

**Signing key.** It signs events and outgoing federation requests. Easiest to back up with the config; the alternative is letting Synapse generate a new one on restore, in which case add the old public key to `old_signing_keys`.

**Database.** SQLite is for testing only, so assume PostgreSQL. Two Synapse-specific rules:

- Never restore into a database that already has tables; at best it errors, at worst you get subtle inconsistencies.
- Do not back up the `e2e_one_time_keys_json` table, or `TRUNCATE` it after restoring and before starting Synapse. Restoring an older backup can re-issue one-time keys that were already used, causing message decryption errors; clearing them makes clients upload new ones.

The easy method is `pg_dump` in custom format (smaller files). It takes a consistent snapshot, so neither Postgres nor Synapse needs stopping:

```shell
sudo -u postgres pg_dump -Fc --exclude-table-data e2e_one_time_keys_json synapse > synapse.dump
```

To restore, create the database as in the Postgres setup, then load it:

```shell
sudo -u postgres createdb --encoding=UTF8 --locale=C --template=template0 --owner=synapse_user synapse
sudo -u postgres pg_restore -d synapse < synapse.dump
```

**Media store.** Always back up `local_content`, which may hold the only copy of users' files. Back up `local_thumbnails` too unless `dynamic_thumbnails` is enabled (then they regenerate); without it there is no tooling to rebuild them. `remote_content` and the remote thumbnails directory, plus `url_cache` and `url_cache_thumbnails`, need no backup. The layout is described in the media repository skill.

## Checked

2026-11-04. Confirmed against the Synapse backups page: config files, signing key and old_signing_keys, database rules, e2e_one_time_keys_json, pg_dump and pg_restore commands, media store directories. Removed the signing_key_path name (not on the page).
Method: documentation only; no commands were run.
