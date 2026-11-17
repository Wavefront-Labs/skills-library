---
id: computing-software.systems-network-administration.virtualisation.proxmox-qemu-guest-agent-and-fsfreeze
name: proxmox-qemu-guest-agent-and-fsfreeze
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [qemu-guest-agent-freeze, qm-agent, qemu-guest-agent, fsfreeze, fs-freeze-hooks, consistent-backup, proxmox-vm, proxmox, proxmox-ve]
level: practitioner
status: docs-checked
description: "Use the QEMU guest agent on Proxmox: enable it, qm agent commands, fs-freeze/thaw during snapshots and backups, freeze hook scripts for databases, and when to disable freeze."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-qm.html#qm_qemu_agent
  - https://pve.proxmox.com/pve-docs/qm.conf.5.html
  - https://pve.proxmox.com/wiki/VM_Backup_Consistency
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# QEMU guest agent and filesystem freeze on Proxmox

**Goal:** clean shutdowns, accurate guest info, and filesystem-consistent snapshots and
backups.

## Enable
1. VM Options → QEMU Guest Agent → enabled (`qm set <id> --agent enabled=1`); a fresh start of the VM is necessary for the change to take effect.
2. Install in guest: the package is usually named `qemu-guest-agent` (for example `apt install qemu-guest-agent` / `dnf install qemu-guest-agent`) and the service must be running; for Windows see the Proxmox Windows VirtIO Drivers article.

## qm agent
```sh
qm agent 120 ping                    # alias for qm guest cmd
qm agent 120 network-get-interfaces
qm agent 120 get-osinfo
qm agent 120 fsfreeze-status
qm guest exec 120 -- systemctl is-active nginx
```
Once the agent is enabled, power commands such as shutdown are sent through the agent; if the agent is not running the shutdown runs into a timeout.

## Freeze during backup and snapshot
By default, when the agent is enabled in the VM config and available in the guest, PVE syncs the guest filesystems with `guest-fsfreeze-freeze` (and thaws afterwards) for: a backup in snapshot mode, cloning a running VM, replicating a running VM, a snapshot without RAM of a running VM, and importing a disk image from a running guest.
- **Windows:** the guest agent works with the VSS layer. Some applications handle consistent backups themselves through VSS, and a freeze can interfere with them; the docs give the example of SQL Server differential backup chains being broken by `guest-fsfreeze-freeze`.

## When freeze causes trouble
- With some Windows applications the freeze interferes with VSS. Preferred fix: configure the QEMU Guest Agent in the guest to use a VSS variant that does not interfere (see the Proxmox wiki page VM Backup Consistency).
- Alternative: disable the `freeze-fs` agent property (`qm set <id> --agent enabled=1,freeze-fs=0`, default 1); the docs warn this can produce backups with inconsistent filesystems.
- Agent enabled in PVE but not running in the guest means agent commands such as shutdown time out; keep the agent installed and running or disable the option.

## Verify
`qm agent <id> ping` responds; the backup task log shows the freeze and thaw steps without errors.

## Checked

2026-10-26 against the Proxmox VE admin guide sources (github.com/proxmox/pve-docs master, last commit 2026-10-17: qm.adoc QEMU Guest Agent, Filesystem Freeze and Thaw and Troubleshooting sections; generated qm.conf.5-opts.adoc agent option; qm.1-synopsis.adoc qm guest cmd) and confirmed the agent option properties (enabled, freeze-fs default 1, fstrim_cloned_disks, type), the list of operations that trigger a freeze, the shutdown-via-agent behaviour and the qm agent alias for qm guest cmd. Corrected the invented freeze-fs-on-backup property to freeze-fs; removed the unconfirmed 8.3 gate, fsfreeze-hook paths and database hook advice.

Method: documentation only; no commands were run.
