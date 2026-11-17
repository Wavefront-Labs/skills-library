---
id: computing-software.database-administration.cassandra.storage-compatibility-mode
name: storage-compatibility-mode
category: computing-software
field: database-administration
product: cassandra
tags: [cassandra, storage-compatibility-mode, sstable-format, client-protocol-version, nosql, wide-column, cql]
level: practitioner
status: docs-checked
description: "Mixed-version rules"
sources: ["https://cassandra.apache.org/doc/latest/", "https://github.com/apache/cassandra/blob/trunk/conf/cassandra.yaml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Compatibility and feature flags

Goal: avoid incompatible on-disk changes.
- 5.0 adds `storage_compatibility_mode` (`CASSANDRA_4`, `UPGRADING`, `NONE`; shipped default `NONE`) to gate new formats.
- Keep mixed-version windows short.
Verify: per cassandra.yaml, roll all nodes to `UPGRADING` first, then roll to `NONE`.

## Checked

2026-11-02. Confirmed against Apache Cassandra trunk docs (doc/modules/cassandra/pages) and conf/cassandra.yaml, nodetool sources: storage_compatibility_mode values, default NONE and upgrade sequence (cassandra.yaml comments).
Removed: the driver protocol pinning remark.
Method: documentation only; no commands were run.
