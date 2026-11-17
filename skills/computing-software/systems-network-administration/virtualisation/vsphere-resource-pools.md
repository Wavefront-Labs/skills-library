---
id: computing-software.systems-network-administration.virtualisation.vsphere-resource-pools
name: vsphere-resource-pools
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [resource-pools, resource-pool, resource-pool-pie-paradox, expandable-reservation, scalable-shares, drs, resource-management, vmware, vsphere]
level: practitioner
status: draft
description: "Use vSphere resource pools correctly: shares are per pool not per VM (the pie paradox), expandable reservations, scalable shares, and why pools are not folders."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-resource-management-8-0/managing-resource-pools.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# vSphere resource pools

**Goal:** divide cluster capacity between groups (prod vs test, tenants) under contention,
without accidentally starving the "high priority" group.

## The pie paradox
Shares divide resources **between sibling pools**, then among VMs inside each pool.
Example: Prod pool High shares (8000) with 80 VMs, Test pool Normal (4000) with 4 VMs.
Under contention Prod gets 2/3 of the cluster split 80 ways; each Test VM gets far more
than each Prod VM. Fixes:
- Enable **scalable shares** on the cluster/pool (7.0+): pool shares scale with VM
  count and size.
- Or set custom shares proportional to VM count and revisit them, or use reservations.

## Reservations and limits on pools
- **Reservation** guarantees MHz/MB to the pool. **Expandable reservation** lets child VMs
  borrow unreserved capacity from the parent for power-on admission.
- **Limits** on pools cap the whole group (e.g. test can never exceed 30% of the cluster);
  use them deliberately, limits cause ready time even when the host is idle.

## Pools are not folders
Using resource pools to organise VMs visually (one pool per team, default shares)
distorts entitlement and is the classic misuse. Use VM folders and tags for
organisation; create pools only for resource policy. Nested pools multiply the problem.

## Inspect
- Cluster → Monitor → Resource Allocation → CPU/Memory shows reservation, shares and
  worst-case allocation per VM.
- PowerCLI: `Get-ResourcePool | Select Name, CpuSharesLevel, NumCpuShares, CpuReservationMHz, MemReservationGB`.

## Gotchas
- DRS must be enabled for resource pools to exist; disabling DRS **deletes** them (vSphere
  7+ offers to save a snapshot of the tree you can restore).
- vApps behave like resource pools for shares.

## Verify
Worst-case allocation in the Resource Allocation view matches the intended priority
(Prod VMs get more than Test VMs under contention), and no pool exists purely as a folder.
