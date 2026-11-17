---
id: computing-software.database-administration.cassandra.k8s-upgrades-and-scaling
name: k8s-upgrades-and-scaling
category: computing-software
field: database-administration
product: cassandra
tags: [cassandra, rolling-restart-k8s, scale-datacenter, operator-upgrade, nosql, wide-column, cql]
level: practitioner
status: draft
description: "Day-2 operations"
sources: ["https://cassandra.apache.org/doc/latest/", "https://docs.datastax.com/en/cql/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Scaling and upgrades on Kubernetes

Goal: scale and upgrade safely.
- Change `size` to scale; the operator decommissions nodes with data streaming.
- Version bumps trigger rolling restarts; keep PDB maxUnavailable=1.
- Back up first with Medusa or snapshots.
Verify: no stuck pods and schema agreement after changes.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
