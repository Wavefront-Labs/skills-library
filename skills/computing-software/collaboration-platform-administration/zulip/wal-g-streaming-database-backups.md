---
id: computing-software.collaboration-platform-administration.zulip.wal-g-streaming-database-backups
name: wal-g-streaming-database-backups
category: computing-software
field: collaboration-platform-administration
product: zulip
tags: [wal-g-backups, point-in-time-recovery, s3-backups-bucket, backups-directory]
level: sme
status: docs-checked
description: "Configure continuous PostgreSQL backups in Zulip with wal-g: S3 secrets or backups_directory, daily 0200 UTC snapshots, WAL archiving, retention and monitoring."
sources: ["https://zulip.readthedocs.io/en/latest/production/export-and-import.html", "https://zulip.readthedocs.io/en/latest/production/system-configuration.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Streaming database backups with wal-g

For continuous point-in-time recovery, Zulip supports daily snapshots plus streaming write-ahead log (WAL) backups through wal-g, kept for 30 days by default. These are database only, not a full system backup. Daily full backups run at 0200 UTC and every WAL archive file is saved as PostgreSQL writes it (every 16 KiB of WAL), so quiet periods can delay uploads by minutes; PostgreSQL's `archive_timeout` bounds that. Monitor that backups run, for example with the Prometheus exporter shipped as `wal-g-exporter` in Zulip's Puppet files.

To S3 (recommended for resilience to disk failure): on the PostgreSQL server add to `/etc/zulip/zulip-secrets.conf`:

```
s3_region =
s3_backups_key =
s3_backups_secret_key =
s3_backups_bucket =
```

The region defaults to the EC2 host's; the key pair is optional when access is by role. Then run `~zulip/deployments/current/scripts/zulip-puppet-apply`. Expect possibly thousands of PutObject requests per day.

To local disk: under `[postgresql]` in `/etc/zulip/zulip.conf` set `backups_directory` to a path on a different disk than `/var/lib/postgresql/` and apply. This does not protect against losing the database host unless the path is a NAS mount or is copied elsewhere.

Tune concurrency, storage class and incremental backups with the `backups_*` keys documented for the `[postgresql]` section.

## Checked

Confirmed against the Database-only backup tools section of the export-and-import page (30-day retention, 0200 UTC daily backups, WAL archive every 16KiB, archive_timeout, wal-g-exporter, the S3 secrets, backups_directory, thousands of PutObject requests) and the zulip.conf postgresql keys on the system-configuration page (backups_disk_concurrency, backups_directory, backups_incremental, backups_storage_class). Nothing removed.

Method: docs-checked 2026-11-09 against docs/production/export-and-import.md and docs/production/system-configuration.md in the zulip/zulip repository (main), the sources of the cited pages.
