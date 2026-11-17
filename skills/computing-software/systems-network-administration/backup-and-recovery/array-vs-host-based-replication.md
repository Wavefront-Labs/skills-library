---
id: computing-software.systems-network-administration.backup-and-recovery.array-vs-host-based-replication
name: array-vs-host-based-replication
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [array-replication, host-based-replication, storage-replication, synchronous-replication, consistency-groups, dr-orchestration, rpo]
level: advanced
status: draft
description: "Choose array-based or host-based replication for DR: synchronous vs asynchronous RPO, granularity, consistency groups, resource cost, vendor lock-in and orchestration integration."
sources:
  - https://www.snia.org/education/dictionary
  - https://techdocs.broadcom.com/us/en/vmware-cis/live-recovery/live-site-recovery/9-0.html
  - https://learn.microsoft.com/en-us/windows-server/storage/storage-replica/storage-replica-overview
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Array-based vs host-based replication

**Goal:** pick the replication layer that meets RPO and consistency needs at an acceptable cost and complexity.

## Comparison
| Aspect | Array-based (SnapMirror, SRDF, Pure, ActiveCluster, Storage Replica at volume level) | Host/hypervisor-based (vSphere Replication, Zerto, Veeam, Hyper-V Replica) |
|---|---|---|
| Granularity | LUN/volume/datastore: everything on it | Per VM or per disk |
| RPO | Synchronous (zero) possible within distance limits; async seconds-minutes | Typically seconds (journal/CDP) to minutes; no synchronous in most |
| Consistency | Consistency groups across volumes | Per VM; multi-VM consistency only in some products (Zerto VPGs) |
| Resource use | Offloaded to arrays and SAN links | Host CPU/network; proxies |
| Vendor dependency | Same vendor/family on both sides | Storage-agnostic (different arrays or HCI at each site) |
| Cost | Array licences, matching hardware | Software licences per VM |
| Orchestration | SRAs for SRM, vendor tools | Built into product or SRM via vSphere Replication |

## Synchronous replication notes
- Every write waits for the remote acknowledgement: latency adds directly to application write latency; practical distances are limited (often tens of kilometres, a few ms RTT).
- Needs a witness/arbitrator for automatic failover (metro clusters, stretched clusters) to avoid split-brain.

## Decision rules
- Zero RPO between nearby sites for critical databases: synchronous array or stretched cluster.
- Mixed storage across sites, per-VM SLAs, many apps with differing RPOs: host-based.
- Very high change-rate workloads: array-based avoids host overhead.
- Ransomware: neither replication protects against encrypted data replicating; journals/point-in-time history (Zerto journal, snapshots on target) and backups are still needed.

## Verify
Measured RPO under peak load (replication lag metrics) meets targets, and test failovers prove multi-VM application consistency where required.
