---
id: computing-software.cloud-infrastructure-engineering.rook.external-cluster-topology-replica1-pools
name: external-cluster-topology-replica1-pools
category: computing-software
field: cloud-infrastructure-engineering
product: rook
tags: [topology-pools, replica-1, ceph-rbd-topology, crush-rule, mon-allow-pool-size-one]
level: advanced
status: docs-checked
description: "Provision zone-pinned replica 1 RBD pools for apps like Kafka in external mode, using the topology flags and the ceph-rbd-topology storage class."
sources:
  - https://rook.io/docs/rook/latest-release/CRDs/Cluster/external-cluster/topology-for-external-mode/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Scenario: an application such as Kafka runs several instances, each claiming its own volume in a different zone. The application replicates data itself, so the data layer needs no redundancy. A storage class provisions from replica 1 Ceph pools, one in each zone.

Warning from the page: with replica 1, losing any OSD in a zone loses all data in that zone's pool, and the pool must be re-created manually.

Steps:
1. In Ceph, find the zone names in the CRUSH map and create a zone-specific CRUSH rule per pool with `ceph osd crush rule create-replicated <rule-name> <root> <failure-domain> <class>`.
2. Create a replica 1 pool from each rule, so each pool is restricted to OSDs in one zone. Silence the warning with `ceph config set global mon_allow_pool_size_one true`.
3. Label the Kubernetes nodes with the OSD topology labels matching each zone.
4. Add the flags to the export script:
- `--topology-pools`: comma-separated topology-constrained RBD pools
- `--topology-failure-domain-label`: the label such as zone, rack or host
- `--topology-failure-domain-values`: comma-separated values matching each pool

The import script then creates a storage class named `ceph-rbd-topology`.

## Checked

2026-11-03. Confirmed against the Topology for external mode page: the Kafka replica 1 scenario, the data-loss warning, the CRUSH rule and mon_allow_pool_size_one steps, and the --topology-pools, --topology-failure-domain-label and --topology-failure-domain-values flags. Removed: nothing.

Method: documentation only; no commands were run.
