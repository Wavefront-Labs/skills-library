---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.placement-groups
name: placement-groups
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, compute-selection, placement-groups, cluster-placement, spread-placement, proximity-placement-groups, compact-placement, hpc-interconnect, efa]
level: advanced
status: docs-checked
description: "Use placement groups and policies (AWS cluster/spread/partition, Azure proximity, Google compact/spread) and EFA for latency, throughput or failure isolation."
sources: ["https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/placement-groups.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/placement-strategies.html", "https://learn.microsoft.com/azure/virtual-machines/co-location", "https://cloud.google.com/compute/docs/instances/placement-policies-overview", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/efa.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Placement groups and HPC interconnect

## Types
| Goal | AWS | Azure | Google Cloud |
|---|---|---|---|
| Lowest latency, highest throughput between nodes | Cluster placement group (one AZ, never multi-AZ) | Proximity placement group (one data center; cannot span zones) | Compact placement policy (best effort; optional maximum distance) |
| Separate hardware to limit correlated failure | Spread placement group (rack level; max 7 running instances per AZ per group) | Spread across availability zones (a proximity group cannot) | Spread placement policy (up to 8 availability domains; max 256 instances) |
| Large replicated systems that need rack awareness | Partition placement group (max 7 partitions per AZ; each partition has its own racks) | - | Spread policy across availability domains |

AWS partition groups expose which instance is in which partition, so topology-aware systems (HDFS, HBase, Cassandra) can place replicas sensibly.

## HPC networking
- AWS EFA (Elastic Fabric Adapter) bypasses the OS kernel via the Libfabric API. It supports NCCL, and Open MPI 4.1+ / Intel MPI 2019 Update 5+ for HPC. Only supported instance types work.
- Azure and Google: the pages checked state only that low latency comes from colocation. Azure recommends proximity groups plus accelerated networking for lowest latency.

## Steps
1. Decide the goal: tight coupling (MPI, distributed training) -> cluster/proximity/compact; resilience -> spread or partition.
2. AWS cluster groups: launch every instance in a single request and use one instance type. Adding instances later, or mixing types, raises the chance of an insufficient-capacity error.
3. AWS: reserve capacity with an On-Demand Capacity Reservation created in the cluster group. Zonal Reserved Instances cannot reserve capacity in a placement group, Capacity Blocks do not support placement groups, and Capacity Reservations do not reserve capacity in partition or spread groups.
4. Azure: specify all VM sizes up front (single template) or set the proximity group `intent` (needs API version 2021-11-01 or later), which picks a data center supporting all listed sizes but does not reserve capacity.
5. Benchmark to confirm the interconnect delivers what the job needs.

## Gotchas
- Cluster placement concentrates failure risk in one AZ.
- AWS capacity error in a group with running instances: stop and start all instances in the group and retry; they may move to hardware with room.
- Azure proximity groups are a colocation constraint, not pinning; deallocated VMs may fail to restart (AllocationFailure) and planned maintenance can leave a group Not aligned. Check with `az ppg show --include-colocation-status`, then deallocate and restart.
- AWS cluster group single-flow traffic is up to 10 Gbps (5 Gbps outside a group); internet and Direct Connect traffic is limited to 5 Gbps.
- Google compact policy with a maximum distance restricts machine series and instance counts; the placement policy is regional and one per resource.

## Verify
- [ ] Measured latency/bandwidth meet the job's requirement.

## Checked
2026-11-08
Method: documentation only; no commands were run.
Confirmed against the AWS EC2 placement strategies page, the AWS EFA page, the Azure proximity placement groups page and the Google Compute Engine placement policies overview. Removed unconfirmed claims: Azure availability-set and fault-domain rows, Azure HB/HC/ND InfiniBand, Google gVNIC/Tier_1/GPUDirect.
