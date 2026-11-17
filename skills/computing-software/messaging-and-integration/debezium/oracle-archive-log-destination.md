---
id: computing-software.messaging-and-integration.debezium.oracle-archive-log-destination
name: oracle-archive-log-destination
category: computing-software
field: messaging-and-integration
product: debezium
tags: [oracle, archive-log, destination, standby]
level: advanced
status: docs-checked
description: "Pin the Oracle archive log destination with archive.destination.name, including primary and standby lists."
sources:
  - https://debezium.io/documentation/reference/stable/connectors/oracle.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Oracle can have up to 31 archive log destinations. The connector uses only destinations whose status in `V$ARCHIVE_DEST_STATUS` is `VALID` and type is `LOCAL`. If more than one qualifies and you do not choose, the connector selects a destination path at random. Retention can differ per destination, so a random pick can point at a path where requested logs were already deleted.

Set the destination by its name, not its path:

```json
"archive.destination.name": "LOG_ARCHIVE_DEST_3"
```

Use the `DEST_NAME` value from `V$ARCHIVE_DEST_STATUS` for the row that matches your retention policy. Do not use the filesystem path.

For standbys whose destination name differs from the primary, give a comma-separated list ordered by preference:

```json
"archive.destination.name": "LOG_ARCHIVE_DEST_2,LOG_ARCHIVE_DEST_5"
```

After failover, Debezium prefers destination 2 and falls back to 5 to collect logs that existed before the standby was promoted. When both instances use the same name, a single value is enough.

The property is only required if either instance has more than one destination that is both `LOCAL` and `VALID`.

Check this query result before configuring:

```sql
SELECT dest_name, status, type FROM v$archive_dest_status;
```

Gotcha: the redo log size and number must be adequate; consult the DBA if the connector or database is slow.

## Checked

2026-11-08: read the Archive log destinations and Redo log sizing sections and the archive.destination.name property row of the Debezium Oracle connector reference (raw AsciiDoc source of the cited page, connectors/oracle.adoc). Confirmed the 31 destination limit, VALID and LOCAL criteria, random selection, DEST_NAME usage, the comma-separated standby list and when the property is required. Removed: the unsupported log-reads Check line.

Method: documentation only; no commands were run.
