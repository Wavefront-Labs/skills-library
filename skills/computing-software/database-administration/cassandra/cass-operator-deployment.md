---
id: computing-software.database-administration.cassandra.cass-operator-deployment
name: cass-operator-deployment
category: computing-software
field: database-administration
product: cassandra
tags: [cassandra, cass-operator, cassandradatacenter, k8ssandra-operator, k8ssandra, statefulset, nosql, wide-column, cql]
level: practitioner
status: draft
description: "Operator-based clusters"
sources: ["https://cassandra.apache.org/doc/latest/", "https://docs.datastax.com/en/cql/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Deploying with cass-operator

Goal: run Cassandra on Kubernetes.
- A `CassandraDatacenter` custom resource describes size, storage class, config and racks (`kubectl apply -f`).
- StatefulSets, PVCs with local or fast network storage; PodDisruptionBudgets.
- k8ssandra-operator adds Reaper, Medusa backups and Stargate (confirm current component set).
Verify: `nodetool status` shows all pods UN.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
