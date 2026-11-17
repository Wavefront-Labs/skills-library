---
id: computing-software.collaboration-platform-administration.zulip.zulip-conf-postgresql-and-memcached
name: zulip-conf-postgresql-and-memcached
category: computing-software
field: collaboration-platform-administration
product: zulip
tags: [postgresql-backups, wal-g-backups, memcached-memory, ssl-mode]
level: advanced
status: docs-checked
description: "Configure the [postgresql] and [memcached] sections of zulip.conf: random_page_cost, listen_addresses, SSL mode, wal-g backup storage class, compression and memcached memory."
sources: ["https://zulip.readthedocs.io/en/latest/production/system-configuration.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# PostgreSQL and memcached keys in zulip.conf

PostgreSQL overrides:

- `random_page_cost`: Zulip defaults to 1.1 for SSDs; use PostgreSQL's 4.0 on spinning disks. Also `effective_io_concurrency` and `listen_addresses`.
- `ssl_ca_file`, `ssl_cert_file`, `ssl_key_file`: PEM paths securing client connections. `ssl_mode` defaults to PostgreSQL's `prefer`, which gives no security benefit; use `require` or better with certificate authentication.
- `missing_dictionaries`: true at initial database creation uses the standard `pg_catalog.english` search configuration instead of Zulip's stopwords; no effect later.
- `version`: do not set by hand; use the PostgreSQL upgrade tool.
- `replication_primary`, `replication_user`: warm standby settings.

Nightly `wal-g` backups run on all non-replicated hosts and warm standbys:

- `skip_backups`: set true to avoid duplicate backups when you have several standbys.
- `backups_directory`: local path owned by `postgres`, used if S3 secrets are absent. Not suitable for disaster recovery unless on a different disk, since backups die with the database.
- `backups_incremental`: delta backups between full ones; 0 for S3, 6 for local disk.
- `backups_storage_class`: `STANDARD` default, `STANDARD_IA` often cheaper, `REDUCED_REDUNDANCY` not suggested.
- `backups_compression_method`: `lz4` default; `lzma` best and slowest, `zstd` and `brotli` in between.
- `backups_disk_concurrency`: default 1; raise on SSD replicas.

Memcached (`[memcached]`): `memory` defaults to one eighth of RAM, `max_item_size` defaults to 1m and needs raising only above about 20k users in an organization, `size_reporting` enables size metrics at slight cost.

## Checked

2026-11-08. Checked: settings and defaults read against the Zulip system-configuration page (docs/production/system-configuration.md, read in full). Removed: nothing.

Method: documentation only; no commands were run.
