---
id: computing-software.database-administration.influxdb.upgrade-v2-and-downgrade
name: upgrade-v2-and-downgrade
category: computing-software
field: database-administration
product: influxdb
tags: [upgrade, downgrade, influxd-downgrade, bolt, sqlite]
level: practitioner
status: docs-checked
description: "Upgrade OSS 2.x in place and downgrade with influxd downgrade, avoiding the migration specification not found error."
sources:
  - https://docs.influxdata.com/influxdb/v2/install/upgrade/v2-to-v2/
  - https://docs.influxdata.com/influxdb/v2/install/upgrade/downgrade/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Upgrading 2.x to a newer 2.x: with Homebrew `brew upgrade influxdb`; otherwise download and install the newer version in place of the current one; for Docker update the image to the newer InfluxDB image tag. If you are on 2.0 beta-16 or earlier, upgrade to 2.0 first.

Downgrading: run the newer binary's downgrade command first, giving the version to downgrade to:

```sh
influxd downgrade 2.0
```

then install the earlier version and start it. InfluxDB does not guarantee backwards compatibility in its embedded metadata stores, so an older binary started on a BoltDB or SQLite file migrated by a newer version fails with an error like `migration specification not found`; do not skip the downgrade step.

From 2.9.0 API tokens are hashed on first startup and cannot be recovered afterward, so capture any plaintext tokens you still need before you upgrade.

## Checked

Method: docs-checked 2026-11-09 against the InfluxDB v2 pages "Upgrade InfluxDB" (v2-to-v2) and "Downgrade InfluxDB", article bodies read from the downloaded text; the token hashing note is the banner on both pages.

Removed: the "back up first" line (not stated on these pages).
