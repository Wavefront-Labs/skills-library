---
id: computing-software.database-administration.cassandra.triggers-and-their-risks
name: triggers-and-their-risks
category: computing-software
field: database-administration
product: cassandra
tags: [cassandra, create-trigger, trigger-class, trigger-risks, triggers, use-keyspace, cql-comments, nosql, wide-column, cql]
level: practitioner
status: docs-checked
description: "Server-side hooks"
sources: ["https://cassandra.apache.org/doc/latest/cassandra/developing/cql/triggers.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Triggers

Goal: know when not to use triggers.
- `CREATE TRIGGER myTrigger ON myTable USING 'org.apache.cassandra.triggers.InvertedIndex';`; the logic is written in any JVM language outside the database, placed in `lib/triggers` of the installation directory, loaded at startup and must exist on every node.
- The trigger fires before the DML statement on its table.
- `DROP TRIGGER` removes it.
Verify: write latency under load tests with the trigger.

## Checked

2026-11-02. Checked against the Triggers page (CREATE TRIGGER, lib/triggers location, startup load, every node, fires before DML, DROP TRIGGER). Removed: 'slow triggers reduce throughput', 'failures fail the write' and 'prefer CDC' (not on the page).

Method: documentation only; no commands were run.
