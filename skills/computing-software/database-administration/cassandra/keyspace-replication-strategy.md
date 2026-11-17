---
id: computing-software.database-administration.cassandra.keyspace-replication-strategy
name: keyspace-replication-strategy
category: computing-software
field: database-administration
product: cassandra
tags: [cassandra, create-keyspace, networktopologystrategy, replication-factor, cql-ddl, keyspace, create-table, nosql, wide-column, cql]
level: practitioner
status: docs-checked
description: "NetworkTopologyStrategy and RF"
sources: ["https://cassandra.apache.org/doc/latest/", "https://github.com/apache/cassandra/blob/trunk/conf/cassandra.yaml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Creating keyspaces and replication

Goal: create keyspaces safely.
- `CREATE KEYSPACE app WITH replication = {'class':'NetworkTopologyStrategy','dc1':3,'dc2':3} AND durable_writes = true;`.
- SimpleStrategy is documented as useful only for testing; use NetworkTopologyStrategy in production.
Verify: `DESCRIBE KEYSPACE app` shows the intended replication.

## Checked

2026-11-02. Confirmed against Apache Cassandra trunk docs (doc/modules/cassandra/pages) and conf/cassandra.yaml, nodetool sources: keyspace replication and durable_writes options, SimpleStrategy testing-only note (ddl and dynamo pages), DESCRIBE KEYSPACE (cqlsh).
Removed: DC-name matching, repair-after-RF-change and system_auth RF advice.
Method: documentation only; no commands were run.
