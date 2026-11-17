---
id: computing-software.systems-network-administration.virtualisation.vsphere-network-io-control
name: vsphere-network-io-control
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [network-io-control, nioc, distributed-switch, shares, bandwidth-reservation, network-resource-pool, vsphere-networking, converged-network, vmware, vsphere]
level: advanced
status: draft
description: "Use vDS Network I/O Control v3: system traffic shares, reservations and limits, VM network resource pools, and sane share values for converged 2x25 GbE hosts."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# vSphere Network I/O Control (NIOC v3)

**Goal:** on converged hosts (two fast NICs carrying everything) make sure vMotion or a
backup cannot starve vSAN, storage or management traffic.

## Concepts
- Applies per **physical uplink** of a vDS, only when that uplink is congested.
- **Shares** (low 25, normal 50, high 100, custom 1-100) divide bandwidth in contention.
- **Reservation** guarantees Mbps per uplink; total reservations across system traffic
  cannot exceed 75% of the slowest uplink. VM reservations also affect admission
  (a VM with a network reservation cannot power on where it cannot be honoured).
- **Limit** caps a traffic type even with no contention; rarely a good idea except to
  tame vMotion on thin links.

## Starting point for converged 2x25 GbE
| Traffic type | Shares | Reservation |
|---|---|---|
| Management | Normal (50) | 1 Gbps |
| vSAN / iSCSI / NFS | High (100) | 5-10 Gbps |
| Virtual machine | High (100) | — |
| vMotion | Low/Normal | — |
| vSphere Replication, backup (NFC) | Low (25) | — |
Adjust after watching real contention (vDS → Monitor → Resource Allocation).

## VM traffic
Create **network resource pools** under the virtual machine system reservation
(e.g. 2 Gbps for a "critical" pool), assign them to distributed port groups, then set
per-vNIC shares/reservation/limit in VM settings.

## Gotchas
- NIOC version 3 requires vDS 6.0+; enabling it on an upgraded vDS from v2 needs the
  upgrade wizard.
- Shares do nothing on a standard switch or when uplinks are not saturated, so testing
  needs real load (iperf between VMs plus a vMotion).
- Reserving too much blocks VM power-on with "insufficient network bandwidth".

## Verify
Run a large vMotion while generating storage I/O; storage latency and VM throughput
stay within targets, and vDS → Monitor → Resource Allocation shows shares in effect.
