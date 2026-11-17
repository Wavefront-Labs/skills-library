---
id: computing-software.systems-network-administration.virtualisation.vsan-ftt-and-raid-policies
name: vsan-ftt-and-raid-policies
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [vsan, vsan-ftt, failures-to-tolerate, raid-1, raid-5, raid-6, erasure-coding, stripe-width, object-space-reservation, spbm, vmware, vsphere]
level: advanced
status: draft
description: "Write vSAN storage policies: FTT 1/2/3 with RAID-1 vs RAID-5/6, minimum host counts, stripe width, space reservation, and the resync cost of changing a policy."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsan/vsan/8-0/vsan-administration/using-vsan-policies.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# vSAN FTT and RAID storage policies

**Goal:** each workload gets the resilience it needs at a known capacity cost, on a
cluster big enough to rebuild after a host loss.

## Host minimums
| Policy | Min hosts | Recommended (to self-heal after a host loss) | Capacity overhead |
|---|---|---|---|
| FTT=1 RAID-1 | 3 | 4 | 2x |
| FTT=1 RAID-5 (OSA 3+1) | 4 | 5 | 1.33x |
| FTT=1 RAID-5 (ESA, 2+1 on 3-5 hosts, 4+1 on 6+) | 3 | 4 / 7 | 1.5x / 1.25x |
| FTT=2 RAID-1 | 5 | 6 | 3x |
| FTT=2 RAID-6 (4+2) | 6 | 7 | 1.5x |
| FTT=3 RAID-1 | 7 | 8 | 4x |
"Recommended" adds one host so vSAN can rebuild components elsewhere instead of waiting
in a degraded state for the failed host.

## Other rules
- **Number of disk stripes per object** (OSA): >1 spreads I/O across devices; only helps
  specific workloads and costs component count. ESA ignores it largely.
- **Object space reservation**: 0% (thin) by default; 100% guarantees space (useful for
  critical DBs) but reduces usable capacity.
- **Force provisioning**: lets a VM be created even if the policy cannot be met; avoid in
  production except for recovery.
- **IOPS limit**, **checksum** (leave on), **site disaster tolerance** for stretched clusters.

## Changing policies
Applying a new policy rebuilds every object to the new layout; on large VMs this is hours
of resync traffic and temporary extra capacity (needs slack). Change in batches, watch
Monitor → vSAN → Resyncing Objects, and avoid during backups or maintenance.

## Gotchas
- Default vSAN policy is FTT=1 RAID-1; on ESA the cluster may auto-manage it
  ("auto-policy management") to RAID-5 when enough hosts exist. Know which is in force.
- A 3-node cluster with FTT=1 has no spare to rebuild into: a second failure during a
  host's maintenance means data unavailability. Use "Ensure accessibility" maintenance.
- Witness components count as a host for quorum but hold no data.

## Verify
VM → Monitor → vSAN → Physical disk placement shows components spread across hosts as
expected; policy compliance is green; capacity view "what if" for host failure is OK.
