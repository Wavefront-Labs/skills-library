---
id: computing-software.database-administration.cassandra.timeuuid-uuid-timestamps
name: timeuuid-uuid-timestamps
category: computing-software
field: database-administration
product: cassandra
tags: [cassandra, timeuuid, date-time-types, mintimeuuid, cql-types, counter, nosql, wide-column, cql]
level: practitioner
status: docs-checked
description: "Choosing identifiers and time types"
sources: ["https://cassandra.apache.org/doc/latest/", "https://github.com/apache/cassandra/blob/trunk/conf/cassandra.yaml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# uuid, timeuuid and time types

Goal: select the right key types.
- `timeuuid` sorts by time: `now()`, `min_timeuuid()`/`max_timeuuid()` for range slices.
- `timestamp` is millisecond precision; `date`, `time`, `duration` exist for calendar values.
Verify: `SELECT to_timestamp(id)` returns the expected time.

## Checked

2026-11-02. Confirmed against Apache Cassandra trunk docs (doc/modules/cassandra/pages) and conf/cassandra.yaml, nodetool sources: now(), min_timeuuid/max_timeuuid, to_timestamp(timeuuid), timestamp millisecond precision, date/time/duration types (functions and types pages).
Removed: varint/decimal key advice, UTC advice, camelCase function names.
Method: documentation only; no commands were run.
