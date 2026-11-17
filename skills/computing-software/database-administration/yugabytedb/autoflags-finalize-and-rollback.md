---
id: computing-software.database-administration.yugabytedb.autoflags-finalize-and-rollback
name: autoflags-finalize-and-rollback
category: computing-software
field: database-administration
product: yugabytedb
tags: [autoflags, promote-auto-flags, upgrade-ysql, finalize-upgrade, get-auto-flags-config, upgrade]
level: advanced
status: docs-checked
description: "Finalize an upgrade by promoting AutoFlags and upgrading the YSQL catalog, inspect AutoFlag state with yb-admin, and know what rollback is no longer possible."
sources: ["https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/manage/upgrade-deployment.md", "https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/admin/yb-admin.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# AutoFlags, finalize and rollback

AutoFlags let a new release ship behaviour changes switched off until every node runs the new version.

Check state:
```
yb-admin --master_addresses <masters> get_auto_flags_config
```

Finalize once you are satisfied (all nodes upgraded, workload healthy):
```
yb-admin --master_addresses <masters> promote_auto_flags
yb-admin --master_addresses <masters> upgrade_ysql
```
`promote_auto_flags` is cluster-level and enables the new behaviours. `upgrade_ysql` runs the YSQL catalog upgrade; if it times out on a large catalog, retry with `--timeout_ms 180000`.

After promotion:
- Rollback to the old version is impossible.

Before promotion, rollback means restarting tservers on the old version first and then masters.

Timeline guidance from the upgrade page: stay in the Monitor phase for as long as needed, up to about 2 days, running real workload and watching error rates and latency. Rollback support starts at v2.20.2. Delete snapshot schedules before the upgrade and recreate them after finalizing or rolling back.

For xCluster pairs, both universes must be finalized; in bidirectional setups finalize them near-simultaneously.

## Checked

2026-11-04. Confirmed against the upgrade deployment page and the yb-admin reference: get_auto_flags_config, promote_auto_flags and upgrade_ysql as cluster-level operations, the --timeout_ms 180000 retry for upgrade_ysql, the two-day recommended Monitor limit, rollback support from v2.20.2, no rollback after finalize, and the snapshot schedule advice. Removed an unsupported causal sentence.

Method: documentation only; no commands were run.
