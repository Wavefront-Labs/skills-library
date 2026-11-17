---
id: computing-software.systems-network-administration.virtualisation.vmfs-locked-file-owner-identification
name: vmfs-locked-file-owner-identification
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [vmfs-lock, vmkfstools-lock, vsphere-troubleshooting, vmfs, hung-vm, vmware, vsphere]
level: advanced
status: draft
description: "Resolve 'file is locked' and 'cannot power on, failed to lock the file' on VMFS: find the lock owner host with vmkfstools -D, release it by killing the holder, never by deleting."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-storage-8-0.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Locked files on VMFS

VMFS uses on-disk locks so one host owns a running VM's files. Errors like
"Unable to access file ... since it is locked" or "Failed to lock the file" at power-on
or consolidation mean some host (or process) still holds it.

## 1. Find the owner
On any host that sees the datastore:
```sh
cd /vmfs/volumes/DS01/app01
vmkfstools -D app01-flat.vmdk           # 'mode 1' = exclusive lock
# output: "owner 5f2c1a3e-8b1d2c4e-1234-001122334455" -> last 12 hex = MAC of owning host's mgmt NIC
```
Mode values: 0 no lock, 1 exclusive, 2 read-only, 3 multi-writer. Owner all zeros = no
host lock (check NFS `.lck-*` files on NFS datastores instead).
Match the MAC: `esxcli network ip interface list` / `esxcfg-nics -l` on each host.
vmkfstools on VMFS6 also shows `RO Owner` and `MAC address` lines directly.

## 2. Find the holding process on that host
```sh
lsof | grep app01                        # which world holds the file
esxcli vm process list                   # is the VM still running there?
```
Typical holders: the VM itself still running (ghost after HA event), a backup proxy
with the disk hot-added, a stuck `vmkfstools`/clone task, an `hostd` worker.

## 3. Release
- VM running on another host: power it off there (or `esxcli vm process kill -t soft -w <wid>`).
- Backup proxy hot-add: remove the disk from the proxy VM (don't delete it!), then
  consolidate the original VM.
- Stuck task: restart management agents on the owner (`/etc/init.d/hostd restart`) as a
  last resort before rebooting it.
- Host down but lock remains: locks of a dead host expire once its VMFS heartbeat stops
  being renewed; if the owning host is alive but disconnected, fix or reboot it.

## Never
Delete or rename `.lck`/flat files to "break" locks, or copy the disk while locked; you
risk two writers corrupting the VMDK.

## Verify
`vmkfstools -D` shows mode 0 or the intended owner; VM powers on; consolidation succeeds.
