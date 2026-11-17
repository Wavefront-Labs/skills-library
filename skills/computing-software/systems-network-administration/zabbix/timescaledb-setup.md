---
id: computing-software.systems-network-administration.zabbix.timescaledb-setup
name: timescaledb-setup
category: computing-software
field: systems-network-administration
product: zabbix
tags: [timescaledb, postgresql, partitioning, schema-sql, history-trends]
level: advanced
status: docs-checked
description: "Enable TimescaleDB for history and trends on PostgreSQL, including the schema script and housekeeping prerequisites."
sources:
  - https://www.zabbix.com/documentation/current/en/manual/appendix/install/timescaledb
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
TimescaleDB partitions PostgreSQL data into time-based chunks for performance at scale. It is not supported on Zabbix proxy.

Prerequisites: a supported TimescaleDB extension version on the database server, and a supported PostgreSQL from the official repository installed first.

Steps from the docs:
1. Enable the extension on the Zabbix database as an administrator: CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE; run via psql against the zabbix database. For a non-public schema add SCHEMA yourschema.
2. Run postgresql/timescaledb/schema.sql after the regular PostgreSQL database has been created with its initial schema and data. For example: cat /usr/share/zabbix/sql-scripts/postgresql/timescaledb/schema.sql | sudo -u zabbix psql zabbix
3. Ignore the best-practices warnings printed on TimescaleDB 2.9.0 and higher; configuration still completes.

Migrating existing history, trends and audit log data can take a long time. Zabbix server and frontend must be down for that period.

The script sets the housekeeping parameters Override item history period and Override item trend period. Both must be enabled to use partitioned housekeeping for history and trends. For compression, both must also be enabled for the housekeeper to remove compressed data; otherwise it does not remove data from tables with compressed chunks and warnings appear in Housekeeping and System information. The script also sets Enable compression and Compress records older than 7 days (not less than 7 days); late data older than that is discarded.

When upgrading Zabbix to a version with new hypertables, the server does not configure them automatically: start the server to upgrade the database, stop it once the log shows the upgrade is complete, then run postgresql/timescaledb/schema.sql. Compression settings can be changed in Administration > Housekeeping.

## Checked

2026-11-09. Confirmed against the Zabbix manual page TimescaleDB setup (current): proxy not supported, prerequisites, CREATE EXTENSION and schema.sql steps, 2.9.0 warning note, migration downtime, housekeeping override parameters, compression defaults, hypertable upgrade steps. Rewrote the housekeeping and upgrade paragraphs to the page wording.

Method: documentation only; no commands were run.
