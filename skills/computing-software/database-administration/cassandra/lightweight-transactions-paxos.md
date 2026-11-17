---
id: computing-software.database-administration.cassandra.lightweight-transactions-paxos
name: lightweight-transactions-paxos
category: computing-software
field: database-administration
product: cassandra
tags: [cassandra, lwt, paxos, serial-consistency, nosql, wide-column, cql]
level: practitioner
status: docs-checked
description: "Compare-and-set with IF clauses"
sources: ["https://cassandra.apache.org/doc/latest/", "https://github.com/apache/cassandra/blob/trunk/conf/cassandra.yaml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lightweight transactions (Paxos)

Goal: use LWT correctly and sparingly.
- `INSERT ... IF NOT EXISTS` / `UPDATE ... IF col = ?` run a Paxos round (several round trips); the result row has `[applied]`.
- `SERIAL CONSISTENCY LOCAL_SERIAL` sets the serial consistency level in cqlsh.
- The docs call the Paxos cost non-negligible; prefer LWT sparingly.
- Accord transactions are documented separately (`accord.enabled` in cassandra.yaml, enabled per table).
Verify: `[applied]` is false on the second identical conditional insert.

## Checked

2026-11-02. Confirmed against Apache Cassandra trunk docs (doc/modules/cassandra/pages) and conf/cassandra.yaml, nodetool sources: IF NOT EXISTS and conditional UPDATE use Paxos with a non-negligible cost (dml), SERIAL CONSISTENCY LOCAL_SERIAL (cqlsh), Accord page and accord.enabled (cassandra.yaml).
Removed: the mixing warning, DC-local linearizability wording, CAS timeout and Accord status claims.
Method: documentation only; no commands were run.
