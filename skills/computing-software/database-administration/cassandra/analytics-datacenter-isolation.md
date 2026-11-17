---
id: computing-software.database-administration.cassandra.analytics-datacenter-isolation
name: analytics-datacenter-isolation
category: computing-software
field: database-administration
product: cassandra
tags: [cassandra, workload-isolation, analytics-dc, local-one-reads, nosql, wide-column, cql]
level: practitioner
status: docs-checked
description: "Protecting OLTP"
sources: ["https://cassandra.apache.org/doc/latest/cassandra/architecture/dynamo.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Isolating analytics workloads

Goal: keep analytics away from production traffic.
- Add a separate DC for analytics replicated from production; run scans with `LOCAL_ONE` there (the docs say `LOCAL_ONE` is faster than `ONE` but typically less available across several datacenters).
- Throttle the analytics client so it cannot saturate the analytics DC.
- Monitor production latency during jobs.
Verify: production p99 unchanged during scans.

## Checked

2026-11-03. Confirmed against the Apache Cassandra documentation: `LOCAL_ONE` behaviour (Architecture: Dynamo page). Removed: the `input.reads_per_sec` option, which belongs to a third-party Spark connector.

Method: documentation only; no commands were run.
