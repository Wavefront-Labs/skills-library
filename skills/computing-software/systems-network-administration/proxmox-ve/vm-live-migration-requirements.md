---
id: computing-software.systems-network-administration.proxmox-ve.vm-live-migration-requirements
name: vm-live-migration-requirements
category: computing-software
field: systems-network-administration
product: proxmox-ve
tags: [live-migration, qm-migrate, online-migration, conntrack, local-disks]
level: practitioner
status: docs-checked
description: "Live migrate VMs between Proxmox VE nodes with qm migrate and know what blocks migration."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-qm.html
  - https://pve.proxmox.com/pve-docs/qm.1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```
qm migrate <vmid> <target>
qm migrate <vmid> <target> --online
qm migrate <vmid> <target> --online --with-local-disks --targetstorage other-store
```

Live migration (`--online`; the GUI defaults to it for running VMs) starts a paused QEMU process on the target, sends memory while the guest runs, re-sends dirty pages in repeated passes, and finally pauses the source for milliseconds, sends the remainder and resumes on the target in well under a second. Disks must be shared or already copied before the runtime state moves.

Requirements: no unmigratable local resources (passed-through PCI or USB devices block live migration), both hosts in the same cluster with a reliable network, a target running the same or newer Proxmox VE packages, CPUs from the same vendor with similar capabilities (other combinations might work but must be tested), and the same CPU architecture (x86 versus arm64 is impossible). Local disks can be migrated by `--with-local-disks`.

`--with-conntrack-state 1` copies firewall conntrack entries of the VM to the target and flushes them on the source. It is best-effort and likely to fail with source NAT on the host. Without it, active connections may be dropped on arrival.

Offline migration works when the VM has local resources, if all disks are on storage defined on both hosts; passthrough settings may need adapting to the target's device locations. Use `--migration_network CIDR` and `--migration_type` to override cluster defaults, and `--bwlimit` in KiB/s to cap bandwidth.

## Checked

2026-11-03. Commands, option names, defaults, limits and behaviour claims were compared with the official Proxmox VE documentation pages: https://pve.proxmox.com/pve-docs/chapter-qm.html, https://pve.proxmox.com/pve-docs/qm.1.html (plus the chapter-qm, qm.1, pct, pvecm, pvesm, vzdump, pvesr and sysadmin pages). Items shown as placeholder or example values (file names, VM IDs, device names) are illustrative. Figures that the pages did not state were removed or reworded.

Method: documentation only; no commands were run.
