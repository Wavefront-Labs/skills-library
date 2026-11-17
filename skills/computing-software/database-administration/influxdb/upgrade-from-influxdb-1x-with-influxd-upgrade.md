---
id: computing-software.database-administration.influxdb.upgrade-from-influxdb-1x-with-influxd-upgrade
name: upgrade-from-influxdb-1x-with-influxd-upgrade
category: computing-software
field: database-administration
product: influxdb
tags: [upgrade, v1-to-v2, influxd-upgrade, dbrp, continuous-queries]
level: advanced
status: docs-checked
description: "Run influxd upgrade to move 1.x data to 2.x: what it creates, what it does not migrate, and prerequisites."
sources:
  - https://docs.influxdata.com/influxdb/v2/install/upgrade/v1-to-v2/automatic-upgrade/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`influxd upgrade` reads the 1.x config and data and:

- Generates a 2.x config file at `~/.influxdbv2/config.toml` (or the path given with `--v2-config-path`) and upgrades metadata and engine paths to `~/.influxdbv2/meta` and `~/.influxdbv2/engine`.
- Writes existing data and WAL files into 2.x buckets.
- Creates DBRP mappings so InfluxQL and v1 clients keep working.
- Writes continuous queries to `~/continuous_queries.txt` by default; tasks replace them in 2.x.

Not migrated or changed:
- 1.x admin users and users with no privileges; create a read-only 1.x user first if a dashboard tool uses an admin account.
- Authentication is required in 2.x; `auth-enabled = false` is unsupported, and requests may be silently ignored if you upgrade that way. Enable auth in 1.x first.
- `inmem` index settings (`max-series-per-database`, `max-values-per-tag`) are ignored.
- The `_internal` database; use a scraper on `/metrics` instead.
- Alternate write protocols (CollectD, Graphite, OpenTSDB, Prometheus, UDP); route them through Telegraf.

Procedure: stop 1.x, back up the 1.x data directory, confirm `influxd version` is the 2.x binary, run `influxd upgrade` (add `--config-file <path>` if the 1.x config is not at the default location; run as the `influxdb` user for .deb installs) and answer the setup prompts. Output is also saved in `upgrade.log`. Afterwards check migrated users with `influx v1 auth list`.

InfluxDB must build a new TSI index on first start, which can take time for large datasets.

## Checked

Method: docs-checked 2026-11-09 against the Automatically upgrade from InfluxDB 1.x page, read in full from the overview to post-upgrade. Dropped the unconfirmed `--continuous-query-export-path` flag.
