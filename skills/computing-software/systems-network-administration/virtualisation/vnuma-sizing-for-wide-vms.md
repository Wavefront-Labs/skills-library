---
id: computing-software.systems-network-administration.virtualisation.vnuma-sizing-for-wide-vms
name: vnuma-sizing-for-wide-vms
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [vnuma-topology, numa, resource-management, cores-per-socket, wide-vm, vmware, vsphere]
level: advanced
status: docs-checked
description: "Size large VMs to the host NUMA topology: cores per socket, vNUMA exposure, ESXi 8 automatic topology, hot-add caveat, and checking NUMA locality in esxtop."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-resource-management/using-numa-systems-with-esxi/virtual-numa-controls.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# vNUMA sizing for wide VMs

A VM whose vCPUs or memory exceed one physical NUMA node ("wide VM") performs best when
the guest sees a matching virtual NUMA topology so the OS and databases place threads and
memory locally.

## Know the host
```sh
esxcli hardware memory get            # NUMA node count
esxcli hardware cpu global get        # packages, cores, threads
sched-stats -t numa-pnode             # memory per node
```
Example: 2 sockets × 24 cores, 768 GB → 2 nodes of 24 cores / 384 GB.

## Rules
- Fit inside one node when possible (≤ 24 vCPU and ≤ ~384 GB here).
- If wider, use vCPU counts divisible by the node count and keep memory balanced.
- vNUMA is exposed automatically when a VM has **> 8 vCPUs** (`numa.vcpu.min=9`).
- **ESXi 8 / hardware version 20**: automatic vTopology picks cores per socket and vNUMA
  for you at power-on; leave "Cores per socket" on **Assigned at power on** unless a
  licence or app needs a specific socket count.
- ESXi 6.5-7: vNUMA is derived from physical topology independent of cores per socket,
  but a cores-per-socket value that spans nodes (e.g. 1 socket × 32 cores on 24-core
  nodes) still misleads the guest's cache/scheduler view. Prefer sockets = NUMA nodes.

## CPU hot add disables vNUMA
With CPU hot add enabled the guest sees a single UMA node. Turn hot add **off** on wide VMs.

## Check locality
esxtop → `m` → `f` to add the NUMA fields (home node, migrations, % memory local).
A low local-memory percentage on a wide VM = topology problem or memory larger than one
node without vNUMA.

## Gotchas
- vMotion to a host with a different NUMA layout keeps the vNUMA picked at power-on;
  power-cycle to recompute.
- `numa.autosize.once` = TRUE (default) means the topology sticks until you change vCPU
  count; reset by setting FALSE or editing CPU count.
- Hyperthread packing (keeping a wide VM inside one node's threads) helps memory-bound
  apps and hurts CPU-bound ones.

## Verify
Guest: `coreinfo -n` (Windows) or `numactl --hardware` (Linux) shows expected nodes;
esxtop local-memory percentage high under load.

## Checked
2026-10-31: Confirmed `numa.vcpu.min` default 9 (vNUMA only for 9+ vCPUs), the ESXi 8.0
automatic coresPerSocket selection, `numa.vcpu.coresPerNode` for hardware version 20,
`numa.autosize.once` and the deactivation of virtual NUMA when CPU hot add is enabled
against the vSphere 8.0 "Virtual NUMA Controls" page, and the hot-add/vNUMA interaction
in the vCenter 8.0U2 release notes. Genericised the esxtop NUMA field names and removed
the unconfirmed numa.vcpu.preferHT parameter.
Method: documentation only; no commands were run.
