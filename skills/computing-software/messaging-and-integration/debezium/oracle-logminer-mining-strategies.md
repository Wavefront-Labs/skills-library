---
id: computing-software.messaging-and-integration.debezium.oracle-logminer-mining-strategies
name: oracle-logminer-mining-strategies
category: computing-software
field: messaging-and-integration
product: debezium
tags: [oracle, logminer, mining-strategy, schema-changes]
level: sme
status: docs-checked
description: "Compare log.mining.strategy options online_catalog, hybrid and redo_log_catalog for schema change handling."
sources:
  - https://debezium.io/documentation/reference/stable/connectors/oracle.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Redo entries hold object identifiers, not names, so LogMiner needs a data dictionary to resolve them. `log.mining.strategy` controls this (default `online_catalog`).

- `online_catalog`: uses the current dictionary and never writes it to the redo logs. Cheapest, but it cannot parse schema changes interleaved with data changes, so events can fail. Telltale signs in redo logs are names like `OBJ# 123456` or `COL1`. For schema changes, do this: let the connector capture all pending DML, run the DDL and wait for it to be captured, then resume DML.
- `redo_log_catalog` (deprecated, scheduled for removal): flushes the dictionary to the redo logs after every log switch. Most reliable for interwoven DDL, but consumes archive log space. Do not run several connectors on one logical database in this mode.
- `hybrid`: starts in `online_catalog` mode. If LogMiner cannot reconstruct the SQL, the connector rebuilds it from the table schema history. It fails only when both fail. This is the suggested migration path from `redo_log_catalog`.

```json
"log.mining.strategy": "hybrid"
```

Restriction: `hybrid` cannot be used when `lob.enabled` is `true`. For CLOB, BLOB or XML capture only `online_catalog` or the deprecated `redo_log_catalog` are available.

Related: `log.mining.session.max.ms` (default `0`) caps how long a LogMiner session lives before a new one starts; by default a new session starts only on a log switch. Set it for low-volume systems where PGA use grows.

## Checked

2026-11-08: read the redo_log_catalog, online_catalog and hybrid strategy sections plus the log.mining.strategy and log.mining.session.max.ms property rows of the Debezium Oracle connector reference (raw AsciiDoc source of the cited page, connectors/oracle.adoc). Confirmed the strategy behaviours, the deprecation, the OBJ# and COL1 symptoms, the DDL procedure, the hybrid and lob.enabled restriction, and the session limit. Removed: the unsupported staging Check line.

Method: documentation only; no commands were run.
