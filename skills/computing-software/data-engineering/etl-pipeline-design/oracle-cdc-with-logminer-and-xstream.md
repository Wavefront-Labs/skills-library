---
id: computing-software.data-engineering.etl-pipeline-design.oracle-cdc-with-logminer-and-xstream
name: oracle-cdc-with-logminer-and-xstream
category: computing-software
field: data-engineering
product: etl-pipeline-design
tags: [etl-pipeline-design, logminer, oracle-cdc, xstream, debezium]
level: sme
status: docs-checked
description: "Capture Oracle changes via LogMiner or XStream (Debezium, GoldenGate): supplemental logging, archive logs, SCN bookmarks, LOB and DDL handling, and DBA coordination."
sources:
  - https://debezium.io/documentation/reference/stable/connectors/oracle.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/sutil/oracle-logminer-utility.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/xstrm/introduction-to-xstream.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Oracle CDC (LogMiner / XStream)

**Goal:** stream inserts, updates and deletes from Oracle into the lake/warehouse with low latency and no triggers.

## Database prerequisites (DBA)
```sql
-- archive log mode
SELECT log_mode FROM v$database;               -- must be ARCHIVELOG
ALTER DATABASE ADD SUPPLEMENTAL LOG DATA;      -- minimal, database level
ALTER TABLE sales.orders ADD SUPPLEMENTAL LOG DATA (ALL) COLUMNS;   -- full row images for captured tables
```
- A dedicated capture user with LogMiner privileges (`LOGMINING`, `SELECT ANY TRANSACTION`, access to `V$` views); in CDB/PDB setups a common user (`c##dbzuser`).
- Archive log retention must exceed the longest possible connector outage plus catch-up.

## Methods
| Method | Notes |
|---|---|
| LogMiner (Debezium default adapter) | mines redo/archive logs; watch database CPU and redo volume at scale |
| XStream | commercial component of Oracle GoldenGate; enabled in Debezium with `database.connection.adapter=xstream` |
| GoldenGate | Oracle's commercial replication product |

## Debezium Oracle connector essentials
```json
{
  "connector.class": "io.debezium.connector.oracle.OracleConnector",
  "database.hostname": "ora.internal", "database.port": "1521",
  "database.dbname": "ORCLCDB", "database.pdb.name": "ORCLPDB1",
  "database.user": "c##dbzuser", "database.password": "${secrets:oracle/password}",
  "table.include.list": "SALES.ORDERS,SALES.ORDER_LINES",
  "log.mining.strategy": "online_catalog",
  "snapshot.mode": "initial",
  "schema.history.internal.kafka.topic": "schema-history.oracle"
}
```
Offsets are SCNs. `online_catalog` is the default `log.mining.strategy`. `redo_log_catalog` tracks schema changes at the cost of higher redo and archive log volume and is marked deprecated in the Debezium docs; the `hybrid` strategy cannot be used with `lob.enabled=true`.

## Hard parts
- **LOBs**: CLOB/BLOB need `lob.enabled=true` and are expensive; exclude if not needed.
- **Long transactions**: the miner buffers until commit; huge batch jobs cause memory pressure and lag.
- **DDL**: coordinate schema changes; Debezium needs the schema history topic intact.
- **Time zones and NUMBER precision**: map `NUMBER` without precision carefully (`decimal.handling.mode`).

## Verify
Lag metric (`MilliSecondsBehindSource`) stays low under peak; a test update shows before/after images; archive logs are not deleted before being mined.

## Checked

2026-10-28. Confirmed in the Debezium Oracle connector page: `ARCHIVELOG`, `LOGMINING` and `SELECT ANY TRANSACTION` grants with `c##dbzuser`, `online_catalog` as default and `redo_log_catalog` deprecated, `hybrid` and `lob.enabled`, XStream as a commercial GoldenGate component via `database.connection.adapter`, `MilliSecondsBehindSource`, `decimal.handling.mode`. Removed: LogMiner no-license claim, XStream latency claim, the managed-services row (not in the cited pages), and the claim that `online_catalog` is faster.

Method: documentation only; no commands were run.
