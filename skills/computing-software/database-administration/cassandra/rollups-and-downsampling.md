---
id: computing-software.database-administration.cassandra.rollups-and-downsampling
name: rollups-and-downsampling
category: computing-software
field: database-administration
product: cassandra
tags: [cassandra, rollup-aggregation, downsample, counter-rollups, nosql, wide-column, cql]
level: practitioner
status: draft
description: "Summary tables"
sources: ["https://cassandra.apache.org/doc/latest/", "https://docs.datastax.com/en/cql/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Rollups and downsampling

Goal: keep aggregates cheap.
- Write raw data plus pre-aggregated tables (per minute/hour) from stream processing.
- Do not aggregate across partitions in queries at read time.
- Use different TTLs per resolution.
Verify: dashboards read only summary tables.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
