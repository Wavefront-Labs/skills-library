---
id: computing-software.systems-network-administration.backup-and-recovery.pre-freeze-and-post-thaw-scripts
name: pre-freeze-and-post-thaw-scripts
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [pre-freeze-script, post-thaw-script, quiescing, fsfreeze-hook, vmware-tools, qemu-guest-agent, application-consistent]
level: advanced
status: docs-checked
description: "Make snapshot backups application-consistent on Linux guests with VMware Tools freeze/thaw scripts and QEMU guest agent fsfreeze hooks, keeping them failure-safe."
sources:
  - https://knowledge.broadcom.com/external/article?legacyId=1006671
  - https://www.qemu.org/docs/master/interop/qemu-ga.html
  - https://pve.proxmox.com/wiki/Qemu-guest-agent
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pre-freeze and post-thaw scripts

**Goal:** applications flush and pause just before the snapshot and resume right after, so the image-level backup is application-consistent.

## VMware Tools (Linux guests)
VMware Tools must be installed in the guest. Custom quiescing scripts go in `/etc/vmware-tools/backupScripts.d/`; the directory is not created automatically, so create it yourself.
- Before freezing: the legacy `/usr/sbin/pre-freeze-script` runs first, then every script in `backupScripts.d` in alphabetical order with `freeze` as the first argument.
- After thawing: scripts in `backupScripts.d` run in descending alphabetical order with `thaw` or `freezeFail` as the first argument, then the legacy `/usr/sbin/post-thaw-script`.
- The directory must contain only executable scripts; other files or non-executable scripts may make quiescing fail.
```bash
#!/bin/sh
# /etc/vmware-tools/backupScripts.d/10-app
case "$1" in
  freeze)         : ;;   # flush and pause the application
  thaw|freezeFail) : ;;  # resume the application
esac
```
On Windows guests the directory is `backupScripts.d` under the VMware Tools install directory (under Program Files by default).

## QEMU guest agent (Proxmox, KVM)
`qemu-ga` can run a script on freeze and thaw: enable it with `-F` / `--fsfreeze-hook` (or the `fsfreeze-hook` key in `qemu-ga.conf`); the script is called with `freeze` or `thaw`, and the default path is `etc/qemu/fsfreeze-hook`. With `-F PATH` do not put a space after `-F`. While filesystems are frozen, qemu-ga blocks all but a safe set of RPCs.

Proxmox VE: install `qemu-guest-agent` in the guest, enable it with `qm set VMID --agent 1` (or the GUI), and backups/snapshots call `guest-fsfreeze-freeze` and `guest-fsfreeze-thaw` (VSS on Windows). Test with `qm agent <vmid> ping`.

## Rules for scripts
- Never leave the app paused: the thaw and freezeFail paths must always resume it.
- Log with timestamps for troubleshooting.

## Verify
Check guest logs for freeze and thaw entries at each backup time, and restore a backup to confirm the application starts cleanly.

## Checked
2026-11-09. Read in full: Broadcom KB 313544 (legacyId 1006671, custom quiescing scripts), QEMU Guest Agent manual, Proxmox "Qemu-guest-agent" wiki. Confirmed script paths, order, arguments, executable-only warning, -F option and default hook path, qm commands. Removed as unstated: the `fsfreeze-hook.d` directory convention, OpenStack, freeze-window timing, root ownership, MySQL lock advice, the alternatives section, and the app-specific example commands.
Method: documentation only; no commands were run.
