---
id: computing-software.database-administration.cassandra.batches-logged-unlogged
name: batches-logged-unlogged
category: computing-software
field: database-administration
product: cassandra
tags: [cassandra, batch, logged-batch, unlogged-batch, nosql, wide-column, cql]
level: practitioner
status: docs-checked
description: "BEGIN BATCH semantics"
sources: ["https://cassandra.apache.org/doc/latest/cassandra/developing/cql/dml.html", "https://cassandra.apache.org/doc/latest/cassandra/managing/configuration/configuration.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Batches: logged, unlogged, counter

Goal: use batches for atomicity, not speed.
- Batches are LOGGED by default: the batch log ensures all mutations eventually complete (or none will), but a multi-partition LOGGED batch is not truly atomic and there can be a window where only some operations are visible.
- There is a performance penalty for batch atomicity across partitions; `UNLOGGED` skips the batch log and a failed batch can be left partly applied.
- A LOGGED batch to a single partition is converted to UNLOGGED; updates to one partition key in a batch are performed in isolation.
- Use the `COUNTER` option for batched counter updates; counter updates are not idempotent.
- `batch_size_warn_threshold` and `batch_size_fail_threshold` (renamed from the `_in_kb` settings, in KiB) guard batch size; look up their defaults in `cassandra.yaml`.
- Batches are not a full analogue of SQL transactions.
Verify: no batch-size warnings in the logs.

## Checked

2026-11-02. Checked against the CQL DML page (BATCH, UNLOGGED batches, COUNTER batches, BATCH vs Transactions) and the configuration page (batch_size_warn_threshold and batch_size_fail_threshold in KiB). Real error fixed: the draft said a LOGGED batch gives multi-partition atomicity; the docs say multi-partition LOGGED batches are not truly atomic. Removed: the 5 KB and 50 KB default figures and the single-partition efficiency claim (not stated), and the system.log check.

Method: documentation only; no commands were run.
