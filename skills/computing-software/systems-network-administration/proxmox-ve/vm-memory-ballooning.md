---
id: computing-software.systems-network-administration.proxmox-ve.vm-memory-ballooning
name: vm-memory-ballooning
category: computing-software
field: systems-network-administration
product: proxmox-ve
tags: [ballooning, balloon, memory, shares, min-memory]
level: practitioner
status: docs-checked
description: "Configure fixed or ballooned VM memory in Proxmox VE, including minimum memory, shares and the 80 percent target."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-qm.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Fixed allocation: set `memory` and minimum memory (`balloon`) to the same value and Proxmox allocates exactly that. The balloon device is still added because it reports how much memory the guest really uses. Keep ballooning on in general; to disable it for debugging, untick Ballooning Device or set `balloon: 0` in the config.

Automatic allocation: set minimum memory below `memory`. Proxmox always guarantees the minimum, and when host RAM usage is below the target percentage it adds memory to the guest up to `memory`. The target defaults to 80% and is set in the node options. When the host runs low, the guest's balloon driver takes pages back; the guest may swap processes and, as a last resort, invoke the OOM killer.

```
qm set 100 --memory 8192 --balloon 2048
qm set 100 --shares 3000
```

`shares` (default 1000) weights how much of the free host memory each ballooned VM gets. Example from the docs: 32 GB host at 80% target using 16 GB leaves 32 * 80/100 - 16 = 9 GB. A database VM with shares 3000 beside three VMs at 1000 gets 9 * 3000 / 6000 = 4.5 GB extra and the others 1.5 GB each.

Linux distributions released after 2010 include the balloon driver. For Windows the driver must be installed manually and can slow the guest, so avoid it on critical systems.

Rule of thumb: always leave 1 GB of RAM for the host.

## Checked

2026-11-03. Commands, option names, defaults, limits and behaviour claims were compared with the official Proxmox VE documentation pages: https://pve.proxmox.com/pve-docs/chapter-qm.html (plus the chapter-qm, qm.1, pct, pvecm, pvesm, vzdump, pvesr and sysadmin pages). Items shown as placeholder or example values (file names, VM IDs, device names) are illustrative. Figures that the pages did not state were removed or reworded.

Method: documentation only; no commands were run.
