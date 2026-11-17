---
id: computing-software.systems-network-administration.proxmox-ve.vm-snapshots-and-hibernate
name: vm-snapshots-and-hibernate
category: computing-software
field: systems-network-administration
product: proxmox-ve
tags: [snapshot, rollback, vmstate, hibernate, delsnapshot]
level: practitioner
status: docs-checked
description: "Take, roll back and delete VM snapshots in Proxmox VE, optionally with RAM state, and hibernate to disk."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-qm.html
  - https://pve.proxmox.com/pve-docs/qm.1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```
qm snapshot <vmid> <snapname> --description "before upgrade"
qm snapshot <vmid> <snapname> --vmstate 1
qm rollback <vmid> <snapname> --start 1
qm delsnapshot <vmid> <snapname>
```

A snapshot stores the VM configuration of that moment as a separate section in the same config file, for example `[testsnapshot]` with `snaptime` (Unix epoch), plus a `parent` property recording the parent and child relationship between snapshots. `--vmstate 1` also saves the memory of a running VM. Rolling back a snapshot that includes RAM starts the VM automatically; otherwise it stays stopped unless you pass `--start`. The storage must support snapshots; on file-based storage that means qcow2. A snapshot is not a backup: it lives on the same storage as the VM.

Snapshots taken with RAM remember the machine version in `runningmachine`, which cannot be changed later.

If the guest agent is running, a snapshot without RAM freezes the filesystems first for consistency.

Hibernate saves memory to disk and stops the VM:

```
qm suspend ID --todisk
```

On the next start the memory is loaded and the VM continues. The target storage for the state, when not given, is the first of: `vmstatestorage` from the VM config, the first shared storage of any VM disk, the first non-shared storage of any VM disk, then the storage `local`.

Hook scripts for lifecycle phases can be attached with `qm set 100 --hookscript local:snippets/hookscript.pl`, with an example at `/usr/share/pve-docs/examples/guest-example-hookscript.pl`.

## Checked

2026-11-03. Commands, option names, defaults, limits and behaviour claims were compared with the official Proxmox VE documentation pages: https://pve.proxmox.com/pve-docs/chapter-qm.html, https://pve.proxmox.com/pve-docs/qm.1.html (plus the chapter-qm, qm.1, pct, pvecm, pvesm, vzdump, pvesr and sysadmin pages). Items shown as placeholder or example values (file names, VM IDs, device names) are illustrative. Figures that the pages did not state were removed or reworded.

Method: documentation only; no commands were run.
