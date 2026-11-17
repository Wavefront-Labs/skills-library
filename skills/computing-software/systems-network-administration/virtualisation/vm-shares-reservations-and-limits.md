---
id: computing-software.systems-network-administration.virtualisation.vm-shares-reservations-and-limits
name: vm-shares-reservations-and-limits
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [shares-reservations-limits, cpu-reservation, memory-reservation, memory-limit, cpu-limit, latency-sensitivity, vswp, resource-management, drs, vmware, vsphere, latency-sensitivity-high]
level: practitioner
status: docs-checked
description: "Set VM CPU/memory shares, reservations and limits on vSphere: when to reserve memory, why limits cause ready time and ballooning, latency sensitivity and swap file sizing."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-resource-management-8-0/configuring-resource-allocation-settings.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# VM shares, reservations and limits

**Goal:** guarantee resources for the VMs that must have them, and avoid hidden caps that
make a VM slow on an idle host.

## Semantics
| Setting | Effect | Applies |
|---|---|---|
| Shares | Relative priority under contention | Only when contended |
| Reservation | Guaranteed minimum; affects admission (power-on fails if it cannot be met) | Always |
| Limit | Hard maximum, even if the host is idle | Always |

## Memory
- A memory **reservation** shrinks the VM's swap file and protects against
  ballooning/swapping. Reserve all memory for
  latency-sensitive DBs, VMs with passthrough devices (required), and VMs with
  huge pages tuned inside.
- A memory **limit below configured RAM** is a trap: the guest thinks it has 16 GB, the
  host gives 4 GB, the rest comes from balloon and host swap. Often left over from a
  template; audit for limits below configured RAM.

## CPU
- CPU reservations (MHz) rarely help; they guarantee cycles but not scheduling latency.
- CPU **limits** create CPU ready and max-limited time even on an idle host. Remove
  unless deliberately throttling a noisy tenant.
- **Latency sensitivity = High** (with full CPU and memory reservation) favours exclusive
  pCPUs for real-time-ish workloads (telco, trading). It reduces consolidation.

## Shares
Default share values scale with configured resources. Raising one VM's shares only
matters under contention and only against its siblings in the same pool.

## Gotchas
- Reservations count against HA admission control (slot policy) and can make a cluster
  look full.
- VMware Tools/balloon drivers missing means the host goes straight to compression and
  swap under pressure.

## Verify
Report shows no unintended limits; esxtop shows no max-limited time for any VM; VMs with
full memory reservation have no meaningful swap file on the datastore.

## Checked
2026-10-31: Shares/reservation/limit semantics and their behaviour under contention confirmed on the Configuring Resource Allocation Settings page of the vSphere Resource Management guide; the latency-sensitivity VM setting confirmed in the govc usage reference. Removed unconfirmed figures: the `.vswp` sizing formula, `%MLMTD`, the 1000-per-vCPU/10-per-MB share defaults and the PowerCLI audit command.
Method: documentation only; no commands were run.
