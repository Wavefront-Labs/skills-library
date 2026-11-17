---
id: computing-software.database-administration.cassandra.cassandra-stress-profile
name: cassandra-stress-profile
category: computing-software
field: database-administration
product: cassandra
tags: [cassandra, stress-yaml, write-benchmark, cassandra-stress-user, cassandra-stress, nosqlbench, load-testing, nosql, wide-column, cql]
level: practitioner
status: draft
description: "Workload profiles"
sources: ["https://cassandra.apache.org/doc/latest/", "https://docs.datastax.com/en/cql/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# cassandra-stress profiles

Goal: model your workload.
- `cassandra-stress user profile=ours.yaml 'ops(insert=1,read=3)' n=10000000 -rate threads=200`.
- Profile YAML defines schema, population and queries; default write tests are unrepresentative.
- Run from separate machines, warm up, record p99.
Verify: results stable across three runs.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
