---
id: computing-software.database-administration.cassandra.counters
name: counters
category: computing-software
field: database-administration
product: cassandra
tags: [cassandra, counter-column, counter-table, counter-update, nosql, wide-column, cql]
level: practitioner
status: docs-checked
description: "Counter table rules"
sources: ["https://cassandra.apache.org/doc/latest/cassandra/developing/cql/types.html", "https://cassandra.apache.org/doc/latest/cassandra/developing/cql/counter-column.html", "https://cassandra.apache.org/doc/latest/cassandra/developing/cql/dml.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Counter columns

Goal: use counters safely.
- A table with a counter column can contain only counters outside the primary key; counters cannot be in the primary key. `UPDATE` increments (`c = c + 1`); `INSERT` does not support counters.
- A counter does not exist until first incremented; the first change starts from 0.
- Updates are not idempotent: after a timeout the client cannot know whether it applied, so replaying may over-count.
- Counters do not support expiration; `USING TTL` or `USING TIMESTAMP` on a counter update is rejected. Use the `COUNTER` batch option for batched updates.
- Deleting is only guaranteed to work the first time; do not re-update a deleted counter.
Verify: concurrent increments from several clients sum correctly in a test.

## Checked

2026-11-02. Checked against CQL data types (Counters and limitations), Using a counter, and DML (INSERT does not support counters, counter batches). Removed: the 'counter batches cannot mix non-counter statements' claim (not stated).

Method: documentation only; no commands were run.
