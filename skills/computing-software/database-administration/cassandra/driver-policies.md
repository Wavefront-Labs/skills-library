---
id: computing-software.database-administration.cassandra.driver-policies
name: driver-policies
category: computing-software
field: database-administration
product: cassandra
tags: [cassandra, token-aware-routing, retry-policy, execution-profile, nosql, wide-column, cql]
level: practitioner
status: draft
description: "Resilient clients"
sources: ["https://cassandra.apache.org/doc/latest/", "https://docs.datastax.com/en/cql/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Load balancing, retry and reconnection policies

Goal: configure driver policies.
- Token-aware plus DC-aware round robin, with `local_datacenter` set explicitly; retry only idempotent operations.
- Execution profiles group consistency, timeouts and policies per workload.
- A few contact points are enough.
Verify: requests land on local-DC replicas only.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
