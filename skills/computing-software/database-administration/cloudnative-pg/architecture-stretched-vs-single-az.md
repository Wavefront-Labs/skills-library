---
id: computing-software.database-administration.cloudnative-pg.architecture-stretched-vs-single-az
name: architecture-stretched-vs-single-az
category: computing-software
field: database-administration
product: cloudnative-pg
tags: [architecture, availability-zones, high-availability, disaster-recovery, shared-nothing, stretched-cluster]
level: practitioner
status: docs-checked
description: "Choose a CloudNativePG deployment shape: 3+ zones in one cluster, a single zone, or two data centers with manual cross-cluster promotion."
sources:
  - https://github.com/cloudnative-pg/cloudnative-pg/blob/main/docs/src/architecture.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
CloudNativePG uses **application-level** replication (PostgreSQL physical replication via WAL shipping), and the project recommends against storage-level replication even though it is possible.

**3+ availability zones in one Kubernetes cluster** is the recommended shape (the control plane needs three zones anyway). The operator treats every zone as active and handles scheduling by affinity, tolerations and node selectors, automated failover, self-healing and updates across zones.

**Single zone** (typical on-premises) still gives HA and DR with the zone as the single point of failure; instances must sit on different worker nodes and must not share storage.

**Only two data centers** cannot form a multi-zone Kubernetes cluster, so run two Kubernetes clusters in active/passive, the second being a DR replica cluster. Promotion of the second cluster is manual.

Key limits:

- Each operator deployment only manages its own Kubernetes cluster. Cross-cluster controlled switchover or unexpected failover must be coordinated manually (GitOps, for example) or by a higher-level tool.
- Automated failover across Kubernetes clusters is not in scope; the operator provides the primitives and probes for such tools.
- A controlled switchover between data centers demotes the primary cluster first, then promotes the replica cluster, with no re-clone of the former primary.

The Architecture page suggests a third physical location may be cheaper overall than carrying the two-site complexity at application level.

## Checked

2026-11-08. Read in full: docs/src/architecture.md. Zone recommendations, two-data-center guidance and the limit of one operator per Kubernetes cluster confirmed on the Architecture page.

Method: documentation only; no commands were run.
