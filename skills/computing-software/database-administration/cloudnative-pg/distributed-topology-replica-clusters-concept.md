---
id: computing-software.database-administration.cloudnative-pg.distributed-topology-replica-clusters-concept
name: distributed-topology-replica-clusters-concept
category: computing-software
field: database-administration
product: cloudnative-pg
tags: [replica-cluster, distributed-topology, designated-primary, disaster-recovery, rpo, rto, multi-region]
level: advanced
status: docs-checked
description: "How a distributed CloudNativePG topology works: replica clusters with a designated primary, fed by streaming or WAL archive, promoted manually."
sources:
  - https://github.com/cloudnative-pg/cloudnative-pg/blob/main/docs/src/architecture.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A distributed PostgreSQL topology spans Kubernetes clusters: one primary cluster and one or more **replica clusters**. Only one PostgreSQL instance can be primary at any time, so applications write inside a single Kubernetes cluster at once. The goals are lower global RPO (backups in several locations, regions or providers) and lower RTO (replication beyond the primary Kubernetes cluster).

A replica cluster is a separate `Cluster` resource in continuous recovery. It replicates by streaming from a primary or standby (cascading), by WAL shipping from an archive, or both. Instead of a primary it has a **designated primary**, a standby with any number of cascading standbys, so the architecture can mirror the primary cluster (symmetric). You may run fewer replicas in the replica cluster and scale up when it is promoted.

The designated primary receives WAL via streaming (`primary_conninfo`) and falls back to the object store via `restore_command`, for example `barman-cloud-wal-restore` from the Barman Cloud plugin. If the archive is its source, run a PostgreSQL version containing the fix described in the Replica Cluster page.

Promotion happens by:

- **Human decision**: demote the current primary first, then promote the designated primary through the CloudNativePG API, so the old primary follows without a re-clone.
- **Unexpected failure** of a whole Kubernetes cluster: promote the replica cluster, accepting possible data loss.

CloudNativePG cannot fail over across clusters automatically; that is delegated to manual action or a federation-aware authority. The topology is declarative, so GitOps can drive it.

## Checked

2026-11-08. Read in full: docs/src/architecture.md. Designated primary, symmetric architecture, human versus failure-driven promotion and the lack of cross-cluster automation confirmed on the Architecture page, section Deployments across Kubernetes clusters.

Method: documentation only; no commands were run.
