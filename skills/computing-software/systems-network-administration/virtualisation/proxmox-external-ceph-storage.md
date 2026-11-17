---
id: computing-software.systems-network-administration.virtualisation.proxmox-external-ceph-storage
name: proxmox-external-ceph-storage
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [external-ceph, ceph, rbd, cephfs, pvesm, proxmox]
level: advanced
status: docs-checked
description: "Connect Proxmox VE to an external Ceph cluster for RBD and CephFS: create restricted client keys, copy keyrings, set monhost and choose krbd."
sources:
  - https://pve.proxmox.com/pve-docs/pve-admin-guide.html#ceph_rados_block_devices
  - https://docs.ceph.com/en/latest/rados/operations/user-management/
  - https://github.com/proxmox/pve-docs/blob/master/pve-storage-rbd.adoc
  - https://github.com/proxmox/pve-docs/blob/master/pve-storage-cephfs.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# External Ceph cluster as PVE storage

**Goal:** use an existing Ceph cluster (not managed by PVE) for VM and container disks.

## On the Ceph cluster
```bash
ceph osd pool create pve-rbd
rbd pool init pve-rbd
ceph auth get-or-create client.pve mon 'profile rbd' osd 'profile rbd pool=pve-rbd' mgr 'profile rbd pool=pve-rbd' \
  -o ceph.client.pve.keyring
```
For CephFS, create a dedicated identity as described in the Ceph user management documentation and keep only its secret key.

## On PVE (any node; files replicate via pmxcfs)
```bash
pvesm add rbd ext-rbd --monhost "10.20.0.11 10.20.0.12 10.20.0.13" --pool pve-rbd --username pve --content images --keyring /root/rbd.keyring
# CephFS: export the bare key and pass it as the keyring file
ssh root@<ceph-host> 'ceph auth get-key client.pvefs' > /root/cephfs.secret
pvesm add cephfs ext-fs --monhost "10.20.0.11 10.20.0.12 10.20.0.13" --fs-name cephfs --username pvefs --content backup --keyring /root/cephfs.secret
```
`monhost` marks the cluster as external, so PVE keeps a separate key copy for the storage. The stored keyring is `/etc/pve/priv/ceph/<STORAGE_ID>.keyring` (RBD) or `/etc/pve/priv/ceph/<STORAGE_ID>.secret` (CephFS, bare key without a `[client.<USER>]` section). Use the Ceph client ID without the `client.` prefix as `username` (default `admin`). After `pvesm add` succeeds delete the plain-text keyring or secret file you created. An optional `/etc/pve/priv/ceph/<STORAGE_ID>.conf` can hold client settings for that storage; do not change these lightly. CephFS storage supports content types vztmpl, iso, backup and snippets (no disk images).

## krbd or librbd
- `krbd` forces access through the kernel module; leave it off unless you need it.
- Containers always use `krbd`, regardless of the option value.

## Gotchas
- The CephFS plugin needs PVE's Ceph client packages: add the PVE Ceph repository, run `apt update` and `apt dist-upgrade`, and make sure no other Ceph repositories are configured.
- Create a dedicated identity with only the capabilities needed for the storage; never copy `client.admin` to PVE.
- If the external cluster rotates the identity, replace the stored keyring or secret.

## Verify
`pvesm status` shows both storages active; `rbd -p pve-rbd ls --id pve` from a node works; a test VM disk creates and snapshots.

## Checked

Docs: Proxmox VE admin guide sources (proxmox/pve-docs, master, last commit 2026-10-17) and storage plugin sources (proxmox/pve-storage, master, last commit 2026-10-09). Ceph documentation sources (ceph/ceph, doc/ directory, master).

Confirmed: `monhost` external-cluster semantics and separate key copy, `pool`, `username` (ID without `client.`, default admin), `krbd` and containers always using krbd, `--keyring` option and delete-the-file instruction, keyring and secret paths, `<STORAGE_ID>.conf` client settings, CephFS properties `fs-name`, `subdir`, `fuse`, CephFS content types, Ceph repository requirement; `profile rbd` exists in Ceph user management. Removed as unconfirmed: firewall port ranges, the Ceph client-version rule, librbd default and performance remarks, and `ceph fs authorize` usage. The `ceph osd pool create` and `rbd pool init` commands are standard Ceph usage and were not re-read for this review beyond the profile names.

Method: documentation only; no commands were run.
