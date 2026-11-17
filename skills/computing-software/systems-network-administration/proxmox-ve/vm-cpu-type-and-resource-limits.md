---
id: computing-software.systems-network-administration.proxmox-ve.vm-cpu-type-and-resource-limits
name: vm-cpu-type-and-resource-limits
category: computing-software
field: systems-network-administration
product: proxmox-ve
tags: [cpu-type, cpulimit, cpuunits, affinity, x86-64-v2-aes]
level: practitioner
status: docs-checked
description: "Pick a VM CPU type for live migration and apply cpulimit, cpuunits and affinity limits in Proxmox VE."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-qm.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Sockets versus cores matters little for performance, but set sockets to match licensing. Overcommitting vCPUs across VMs is fine, but Proxmox refuses to start a VM with more vCPUs than physical cores.

CPU type decides which CPU flags the guest sees:
- `host` gives exactly the host flags: best performance, fine for a homogeneous cluster with identical CPUs and microcode.
- For live migration with only Intel or only AMD hosts, choose the lowest CPU generation in the cluster.
- For mixed clusters choose the lowest compatible QEMU virtual type. Migration between Intel and AMD hosts is never guaranteed.
- The backend default is `kvm64`; the UI default for new VMs is `x86-64-v2-AES` (Westmere or newer on Intel, 4th generation Opteron or newer on AMD).

Limits:

```
qm set 100 --cpulimit 4
qm set 100 --cpuunits 200
qm set 100 --affinity 0-1,8-11
```

`cpulimit` is host CPU time (1.0 equals 100%); with 8 vCPUs and `cpulimit 4`, all 8 vCPUs together get at most 400%. Extra QEMU threads can push usage above the vCPU count, so set cpulimit equal to the core count for a hard ceiling. `cpuunits` is a relative weight (default 100, or 1024 on cgroup v1): 200 gets twice the CPU of 100 under contention. `affinity` pins vCPUs to host cores via taskset and is not a security feature; it complicates migration to nodes with fewer cores.

## Checked

2026-11-03. Commands, option names, defaults, limits and behaviour claims were compared with the official Proxmox VE documentation pages: https://pve.proxmox.com/pve-docs/chapter-qm.html (plus the chapter-qm, qm.1, pct, pvecm, pvesm, vzdump, pvesr and sysadmin pages). Items shown as placeholder or example values (file names, VM IDs, device names) are illustrative. Figures that the pages did not state were removed or reworded.

Method: documentation only; no commands were run.
