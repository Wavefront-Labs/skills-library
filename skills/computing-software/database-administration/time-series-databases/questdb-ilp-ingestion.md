---
id: computing-software.database-administration.time-series-databases.questdb-ilp-ingestion
name: questdb-ilp-ingestion
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-questdb, questdb-ilp-ingestion, questdb]
level: practitioner
status: draft
description: "Ingest into QuestDB using ILP with the right transport."
sources:
  - https://questdb.io/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# InfluxDB line protocol ingestion

**Goal:** Ingest into QuestDB using ILP with the right transport.

## Steps
- Use the official clients (Python, Java, Go, Rust, C++) with the ILP over HTTP sender for acknowledged writes; TCP ILP is faster but gives no per-request errors.
- HTTP: `POST /write` with line protocol also works for Telegraf's influxdb output, pointed at port 9000.
- Tables and columns are created automatically on first write (disable in production via `line.auto.create.tables` options, confirm names).
- Mixed-type writes to the same column cause a type error; set types in advance.
- Batch lines and flush by size or interval; handle retry with the client's retry timeout.
- Check ingestion with `SELECT count() FROM readings;` and the web console on port 9000.

**Gotcha:** Auto-created columns inherit the type of the first value, so a first integer write makes the column LONG instead of DOUBLE.

## Verify
- New rows appear after flush.
- No type-mismatch errors in the server log.
