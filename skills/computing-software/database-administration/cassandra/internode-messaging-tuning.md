---
id: computing-software.database-administration.cassandra.internode-messaging-tuning
name: internode-messaging-tuning
category: computing-software
field: database-administration
product: cassandra
tags: [cassandra, internode-timeouts, messaging-service, native-protocol, internode-messaging, streaming, zero-copy-streaming, nosql, wide-column, cql]
level: practitioner
status: docs-checked
description: "Message verbs and timeouts"
sources: ["https://cassandra.apache.org/doc/latest/", "https://github.com/apache/cassandra/blob/trunk/conf/cassandra.yaml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Internode messaging and timeouts

Goal: understand coordinator-replica traffic.
- Coordinators send mutations and reads to replicas as messages with per-verb timeouts (`read_request_timeout`, `write_request_timeout`, `range_request_timeout`).
- Inbound/outbound queues have capacity limits; overload drops messages (see `nodetool tpstats`).
- Clients use the native protocol (CQL binary, port 9042).
Verify: raising a timeout is paired with a root-cause fix, not used alone.

## Checked

2026-11-02. Confirmed against Apache Cassandra trunk docs (doc/modules/cassandra/pages) and conf/cassandra.yaml, nodetool sources: read_request_timeout, write_request_timeout, range_request_timeout (cassandra.yaml), messaging architecture page, tpstats, native port 9042.
Removed: nothing.
Method: documentation only; no commands were run.
