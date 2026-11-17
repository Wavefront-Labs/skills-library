---
id: computing-software.systems-network-administration.virtualisation.proxmox-storage-inactive-troubleshooting
name: proxmox-storage-inactive-troubleshooting
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [storage-inactive, pve-storage, pvesm, nfs, cifs, iscsi, proxmox]
level: practitioner
status: docs-checked
description: "Where Proxmox VE keeps storage settings and credentials, and the pvesm commands and properties (status, disable, nodes) to check when a storage is unusable on a node."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-pvesm.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Storage inactive or unavailable: what the storage chapter lets you check

**Scope:** the Proxmox VE storage chapter documents configuration, not a fault-finding
procedure. This skill lists the places and commands it does document; it gives no
diagnosis of why a particular server stops answering.

## Look at state and configuration
- `pvesm status` lists storage status.
- `pvesm list <STORAGE_ID> [--vmid <VMID>]` lists the storage contents.
- All storage configuration is in `/etc/pve/storage.cfg`, which sits in `/etc/pve` and is
  distributed to all cluster nodes, so every node shares the same storage configuration.

## Properties that make a storage unavailable on purpose
- `disable`: "disable the storage completely". Re-enable with `pvesm set <STORAGE_ID>
  --disable 0` (set `--disable 1` to disable).
- `nodes`: list of cluster node names where the storage is usable/accessible; use it to
  restrict access to a limited set of nodes (for example a storage only reachable from some
  nodes).
- `shared`: marks an already shared storage as single storage with the same contents on all
  nodes; it does not make local storage accessible to other nodes.

## Per-type facts the chapter documents
- NFS: mount point defaults to `/mnt/pve/<STORAGE_ID>/`; `options` are NFS mount options
  (see man nfs); the chapter's example uses `options vers=3,soft`.
- CIFS: the password is stored in `/etc/pve/priv/storage/<STORAGE-ID>.pw` (root only);
  mount point defaults to `/mnt/pve/<STORAGE_ID>/`; `smbversion` sets the SMB version; extra
  options go to mount.cifs, and Proxmox VE always sets `soft` and may set username,
  credentials, guest, domain and vers itself.
- Proxmox Backup Server: `fingerprint` is the API TLS certificate fingerprint, shown in the
  server's dashboard or by `proxmox-backup-manager cert info`; required for self-signed
  certificates. The password is stored in `/etc/pve/priv/storage/<STORAGE-ID>.pw`.
- iSCSI: low-level management is done with the `iscsiadm` tool.
- External Ceph RBD with cephx: the keyring is stored at
  `/etc/pve/priv/ceph/<STORAGE_ID>.keyring`; CephFS stores its secret at
  `/etc/pve/priv/ceph/<STORAGE_ID>.secret`.
- Directory-style mounts: for a BTRFS storage whose directory is not itself the mount point
  the chapter highly recommends the `is_mountpoint` option (example `is_mountpoint
  /mnt/data2`). Other mounts can be made via `/etc/fstab` and a directory storage defined
  on that path.
- `pvesm remove <STORAGE_ID>` only removes the configuration; it does not delete data or
  unmount anything.

## Checked
Date: 2026-11-07. Read the Proxmox VE storage chapter (`chapter-pvesm.html`) by search and
section reads (storage.cfg, common properties, pvesm command examples, NFS, CIFS, PBS,
iSCSI, Ceph RBD, CephFS and BTRFS sections). Removed as not on the page: the `journalctl
-u pvestatd` and `cat` first-look steps, the 10 second polling claim, grey-icon behaviour,
`showmount`, `rpcinfo`, firewall ports, `smbclient`, `iscsiadm -m session/discovery`,
initiator name file, LVM filter advice, `ceph -s`, the stale-NFS `umount -f -l` and
`systemctl restart pvestatd` recipe, `is_mountpoint` for plain directory storage (the page
only mentions it for BTRFS), the root-filesystem-fill gotcha and the Verify step.
Method: documentation only; no commands were run.
