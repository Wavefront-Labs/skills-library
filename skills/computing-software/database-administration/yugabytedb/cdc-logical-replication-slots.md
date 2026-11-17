---
id: computing-software.database-administration.yugabytedb.cdc-logical-replication-slots
name: cdc-logical-replication-slots
category: computing-software
field: database-administration
product: yugabytedb
tags: [cdc, logical-replication, replication-slot, publication, yboutput, pgoutput, lsn, replica-identity, kafka]
level: advanced
status: docs-checked
description: "Operate YugabyteDB CDC with logical replication: slots, publications, output plugins, LSN types, replica identities, monitoring views, and slot design practices."
sources: ["https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/additional-features/change-data-capture/using-logical-replication/key-concepts.md", "https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/additional-features/change-data-capture/using-logical-replication/best-practices.md", "https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/additional-features/change-data-capture/using-logical-replication/monitor.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# CDC with logical replication

CDC follows the PostgreSQL publish-subscribe model. A **replication slot** is an ordered stream of changes for one database, and a **publication** selects tables (it lives in one database).

Output plugins: `yboutput` (YugabyteDB specific), `pgoutput`, `test_decoding` and `wal2json`. Replica identity CHANGE is not supported by pgoutput.

LSN types, chosen at slot creation:
- SEQUENCE (default): monotonic within the slot only; never compare LSNs across slots.
- HYBRID_TIME: the commit hybrid time.

Replica identity per table: CHANGE (default), DEFAULT, FULL or NOTHING. The default for new tables comes from `ysql_yb_default_replica_identity`.

Design practices:
- One slot per table for parallel consumption; each slot is independent.
- For fan-out to several applications, consume once and distribute downstream.
- Consumers may connect to any tserver, and reconnect to another after a failure. Spread different slots across different tservers.
- With Kafka Connect, deleting a connector does not clear its stored offsets. Do not drop and recreate a slot with the same name and reuse old topics: SEQUENCE LSNs are not comparable across slots, so records may be missed.

Monitor with the `pg_replication_slots`, `pg_publication` and `pg_publication_tables` views (fields such as `restart_lsn`, `confirmed_flush_lsn` and `yb_restart_commit_ht`), and CDC metrics `cdcsdk_sent_lag_micros`, `cdcsdk_flush_lag` and `cdcsdk_expiry_time_ms`.

## Checked

2026-11-04. Confirmed against the key concepts, best practices and monitor pages for logical replication: output plugins, SEQUENCE and HYBRID_TIME LSN types, replica identities and ysql_yb_default_replica_identity, the slot design practices, Kafka Connect offset behaviour, the monitoring views and cdcsdk metrics. Removed the bundled-plugins claim, the cheapest claim and the PITR statement, which the pages do not make.

Method: documentation only; no commands were run.
