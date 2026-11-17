---
id: computing-software.database-administration.scylladb.nodetool-toppartitions
name: nodetool-toppartitions
category: computing-software
field: database-administration
product: scylladb
tags: [nodetool, toppartitions, hot-partitions, sampling, diagnostics]
level: practitioner
status: docs-checked
description: "Find hot partitions with nodetool toppartitions: syntax, duration in ms, ks and cf filters, capacity and samplers options, and how to read the WRITES and READS output."
sources: ["https://github.com/scylladb/scylladb/blob/master/docs/operating-scylla/nodetool-commands/toppartitions.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# nodetool toppartitions

Samples reads and writes and reports the most active partitions of a table over a time window. Run it while reads and writes are happening.

```
nodetool toppartitions <keyspace> <table> <duration-ms>
nodetool toppartitions nba team_roster 5000
```

Flag form: `toppartitions [--ks-filters ks] [--cf-filters tables] [-d duration] [-s|--capacity capacity] [-a|--samplers samplers]`.
- `-d`: duration in milliseconds (needs the `-d` prefix).
- `--ks-filters`: list of keyspaces.
- `--cf-filters`: list of `keyspace:table` entries.
- `--capacity`: sampler capacity; larger is more accurate but uses more memory (default 256 keys).
- `--samplers`: `WRITES`, `READS`, or both (default).

Examples:
- All tables, all keyspaces: `nodetool toppartitions`
- Last second: `nodetool toppartitions -d 1000`
- Specific tables: `nodetool toppartitions --cf-filters ks:t,system:status`
- Keyspaces: `nodetool toppartitions --ks-filters ks,system`

Output has one block per sampler (`WRITES Sampler`, `READS Sampler`) with the approximate cardinality, the capacity, and a "Top 10 partitions" table of partition key, `Count` and `+/-` (estimation error). If `+/-` approaches `Count`, the measurement is inaccurate; raise `--capacity`. `nodetool getendpoints` shows which node holds a partition key.

## Checked

2026-11-04: syntax, parameters, defaults, examples and output columns confirmed against the ScyllaDB nodetool toppartitions documentation page. Replaced the unsupported hot-partition advice with the page's accuracy note.

Method: documentation only; no commands were run.
