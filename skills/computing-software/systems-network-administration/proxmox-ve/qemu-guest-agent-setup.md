---
id: computing-software.systems-network-administration.proxmox-ve.qemu-guest-agent-setup
name: qemu-guest-agent-setup
category: computing-software
field: systems-network-administration
product: proxmox-ve
tags: [qemu-guest-agent, qga, fsfreeze, guest-trim, freeze-fs]
level: practitioner
status: docs-checked
description: "Install and enable the QEMU guest agent for correct shutdown, IP reporting, backups and TRIM in Proxmox VE."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-qm.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The guest agent is a service in the VM that gives the host a command channel. Proxmox uses it to show guest IP addresses, send clean shutdown commands and freeze filesystems around backups.

Setup needs both sides:
1. Install the agent in the guest; on most Linux distributions the package is `qemu-guest-agent`. On Windows install it from the VirtIO drivers package.
2. Enable communication with the agent in the VM Options panel (QEMU Guest Agent). The VM needs a fresh start for this to take effect.

If shutdown times out, the agent is probably not running, since Proxmox then sends power commands through it.

Freeze and thaw: with the agent enabled and available, Proxmox calls `guest-fsfreeze-freeze` and `guest-fsfreeze-thaw` for backups in snapshot mode, cloning a running VM, replicating a running VM, a snapshot without RAM, and importing a disk from a running guest. On Windows some applications (for example SQL Server) use VSS themselves and a freeze can break their backup chain, such as differential backups. Preferred fix is configuring the guest agent to use a different VSS variant. Alternatively disable the `freeze-fs` guest agent option (default 1), which can give backups with inconsistent filesystems.

Run guest-trim: with this option Proxmox issues a trim after moving a disk to another storage or live migrating a VM with local storage, freeing space on thin storage. On ext4 only the first trim covers everything until reboot, since the filesystem remembers trimmed areas in memory.

## Checked

2026-11-09. Compared with the QEMU Guest Agent section and the agent option of https://pve.proxmox.com/pve-docs/chapter-qm.html. Removed the qm set command, which the page does not show.

Method: documentation only; no commands were run.

