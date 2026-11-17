---
id: computing-software.systems-network-administration.virtualisation.proxmox-unlock-and-stop-hung-vm
name: proxmox-unlock-and-stop-hung-vm
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [qm-unlock, qm, proxmox-vm, hung-vm, vm-lock, proxmox]
level: practitioner
status: docs-checked
description: "Recover a Proxmox VM stuck 'locked (backup/migrate/snapshot)' or not responding to shutdown: identify the lock source, qm unlock, qm stop with skiplock, and kill as last resort."
sources:
  - https://pve.proxmox.com/pve-docs/qm.1.html
  - https://pve.proxmox.com/pve-docs/chapter-qm.html#_locks
  - https://pve.proxmox.com/pve-docs/chapter-ha-manager.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Unlocking and stopping a hung Proxmox VM

## Locks
Config line `lock: <type>` in `/etc/pve/qemu-server/<vmid>.conf` blocks other operations.
Types: `backup`, `clone`, `create`, `migrate`, `rollback`, `snapshot`, `snapshot-delete`, `suspended`, `suspending`. Online migrations, snapshots and backups set a lock to prevent incompatible concurrent actions; a stale lock can remain, for example after a power failure.

## Before unlocking: is the task still running?
```sh
qm config 101 | grep lock
```
Check the node's Tasks panel (or the task list) for a running backup, migration, clone or snapshot of this VM. Only unlock if you are sure the action which set the lock is no longer running; stop a still-running task first.

```sh
qm unlock 101
```
For `snapshot-delete` locks, also check `qm listsnapshot 101` for a half-deleted snapshot; `qm delsnapshot --force` removes the snapshot from the config file even if removing the disk snapshots fails.

## VM not responding to shutdown
```sh
qm shutdown 101 --timeout 120       # ACPI event, or via the guest agent if enabled; add --forceStop 1 to make sure it stops
qm stop 101                         # the qemu process exits immediately, like pulling the power plug
qm stop 101 --skiplock 1            # ignore locks (only root may use it)
qm stop 101 --overrule-shutdown 1   # abort active qmshutdown tasks before stopping
```
If `qm stop` hangs (QEMU stuck in uninterruptible I/O, e.g. dead NFS), find the QEMU process of the VM and check its state with `ps -o pid,stat,cmd -p <pid>`; `D` state means it is waiting on storage, so fix the storage path or reboot the node.

## Gotchas
- HA-managed VMs: request the stopped state with `ha-manager set vm:101 --state stopped`, otherwise the HA stack restarts a VM you stopped by hand.
- A process in `D` state cannot be killed until its I/O returns; restoring the storage path or rebooting the node clears it. Migrate other VMs off first.
- After a node crash that left a backup lock, check the backup storage for a partial archive.

## Verify
`qm status 101` shows stopped/running as intended, no `lock:` line, next backup succeeds.

## Checked

2026-10-26 against the Proxmox VE admin guide sources (github.com/proxmox/pve-docs master, last commit 2026-10-17: qm.adoc Locks section, generated qm.conf.5-opts.adoc lock values, qm.1-synopsis.adoc stop, shutdown, unlock and delsnapshot options, ha-manager.adoc) and confirmed the lock types, qm unlock caution, the qm stop and shutdown options (--skiplock root only, --timeout, --forceStop, --overrule-shutdown) and the ha-manager --state stopped request. Removed the wrong statement that unlocking during a running vzdump is harmless, and the unconfirmed task-list and pid file paths.

Method: documentation only; no commands were run.
