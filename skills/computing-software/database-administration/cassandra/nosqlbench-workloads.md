---
id: computing-software.database-administration.cassandra.nosqlbench-workloads
name: nosqlbench-workloads
category: computing-software
field: database-administration
product: cassandra
tags: [cassandra, nosqlbench-workload, activity-driver, scenario, nosql, wide-column, cql]
level: practitioner
status: draft
description: "Driver-level testing"
sources: ["https://cassandra.apache.org/doc/latest/", "https://docs.datastax.com/en/cql/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# NoSQLBench workloads

Goal: benchmark with NoSQLBench.
- `nb5 cql-keyvalue rampup-cycles=1M main-cycles=10M host=<host>` runs bundled scenarios (confirm CLI).
- Custom workloads are YAML with bindings; metrics go to Prometheus and Grafana.
Verify: latency percentiles reported per op.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
