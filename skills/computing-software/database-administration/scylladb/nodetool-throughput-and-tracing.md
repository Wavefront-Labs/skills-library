---
id: computing-software.database-administration.scylladb.nodetool-throughput-and-tracing
name: nodetool-throughput-and-tracing
category: computing-software
field: database-administration
product: scylladb
tags: [nodetool, setcompactionthroughput, setstreamthroughput, settraceprobability, tracing]
level: practitioner
status: docs-checked
description: "Runtime throttling and tracing with nodetool: setcompactionthroughput, setstreamthroughput (0 disables the cap) and settraceprobability with its system_traces cost."
sources: ["https://github.com/scylladb/scylladb/blob/master/docs/operating-scylla/nodetool-commands/setcompactionthroughput.rst", "https://github.com/scylladb/scylladb/blob/master/docs/operating-scylla/nodetool-commands/setstreamthroughput.rst", "https://github.com/scylladb/scylladb/blob/master/docs/operating-scylla/nodetool-commands/settraceprobability.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Compaction/stream throughput caps and trace probability

**Compaction throughput cap**:
```
nodetool setcompactionthroughput <value_in_mib>
nodetool getcompactionthroughput
```
**Streaming throughput cap** (SSTable streaming):
```
nodetool setstreamthroughput <value_in_mb>
nodetool getstreamthroughput
```
For both, a value of `0` disables capping. The two pages disagree on units (`value_in_mib` for compaction, `value_in_mb` for streaming) and both describe the set commands as "Print the throughput cap", apparently a copy error since the syntax takes a value.

**Tracing**: `nodetool settraceprobability <value>` sets the probability, between 0 and 1, that a request is traced. `0` never traces and `1` traces everything; 60% is `0.6`. It helps find the queries behind intermittent slowness.

```
nodetool settraceprobability 0.1
nodetool gettraceprobability
```

Trace data is written to the `system_traces` keyspace. Use caution with a high value: system-wide tracing has a performance impact on an active system.

## Checked

2026-11-04. Confirmed against setcompactionthroughput.rst, setstreamthroughput.rst and settraceprobability.rst: syntax, zero disables capping, probability semantics, system_traces keyspace, performance caution. The pages conflict on units (MiB versus MB) and describe the set commands as printing the cap; this is noted in the skill. Removed the runtime-lever advice and streaming scope list.

Method: documentation only; no commands were run.
