---
id: computing-software.cloud-infrastructure-engineering.openebs.choose-data-engine-by-node-and-workload
name: choose-data-engine-by-node-and-workload
category: computing-software
field: cloud-infrastructure-engineering
product: openebs
tags: [data-engine, selection, hyperconverged, disaggregated, local-storage, replicated-storage, capacity-planning]
level: practitioner
status: docs-checked
description: "Pick Local Storage or Replicated Storage from cluster size, ephemeral nodes, hyperconverged versus disaggregated layout, and whether the workload replicates itself."
sources:
  - https://openebs.io/docs/concepts/data-engines
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
OpenEBS bases engine choice on two things: node capabilities and what the stateful application already provides.

**Node capabilities.** The docs sketch small nodes (up to 4 cores, 16 GB RAM, gigabit Ethernet), medium (up to 16 cores, 32 GB, up to 10G) and large (over 16 cores, 256 GB or more, 10 to 25G). Storage may be ephemeral (lost when the node leaves the cluster), cloud or network volumes that can be re-attached, or direct-attached, and it may be slow (SAS HDD), medium (SAS SSD) or fast (NVMe).

The recommendation table for small to medium deployments:

| Layout | Engine |
|---|---|
| Single node, non-ephemeral | Local Storage |
| Multi-node hyperconverged, non-ephemeral | Local Storage and Replicated Storage |
| Multi-node disaggregated, ephemeral | Replicated Storage |

**Workload capabilities.** Distributed databases such as MongoDB replicas already handle node failure, so they mostly need performance and capacity from the engine: Local Storage. Standalone workloads depend on the engine for availability: Replicated Storage. Cassandra-style workloads can benefit from engine-level availability for faster node rebuilds, at the cost of extra storage. Workloads needing performance and availability point to Replicated Storage.

All engines support dynamic provisioning and strong consistency.

## Checked

Method: 2026-11-08 read the raw markdown of the cited data engines overview page in full; node sizes, both recommendation tables and the Cassandra and MongoDB examples match the page and are unchanged.
