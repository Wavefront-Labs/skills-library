---
id: computing-software.database-administration.cassandra.change-data-capture
name: change-data-capture
category: computing-software
field: database-administration
product: cassandra
tags: [cassandra, cdc-raw, cdc-enabled, commitlog-cdc, nosql, wide-column, cql]
level: practitioner
status: docs-checked
description: "CDC logs"
sources: ["https://cassandra.apache.org/doc/latest/cassandra/managing/operating/cdc.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Change data capture

Goal: stream changes.
- Enable node-wide with `cdc_enabled: true` (default false) and per table with `cdc=true` (`CREATE TABLE ... WITH cdc=true` or `ALTER TABLE foo WITH cdc=true`).
- Commit log segments are moved to `cdc_raw_directory` once their memtables are flushed; a `_cdc.idx` file records how much of each segment is durable, so parse only up to that offset.
- `cdc_total_space` (default: min of 4096MiB and 1/8th of the volume) caps CDC disk use; once full, writes to CDC-enabled tables are rejected until a consumer parses and removes files.
- Do not enable CDC without a consumption process in place.
Verify: segments appear in `cdc_raw_directory` after a flush and are consumed.

## Checked

2026-11-02. Checked against the Change Data Capture page (cdc table property, cdc_enabled, cdc_raw_directory, cdc_total_space default, _cdc.idx, rejection of writes, warning). Removed: the Debezium claim (not on the page).

Method: documentation only; no commands were run.
