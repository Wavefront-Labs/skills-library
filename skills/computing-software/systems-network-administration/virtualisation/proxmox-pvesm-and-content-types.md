---
id: computing-software.systems-network-administration.virtualisation.proxmox-pvesm-and-content-types
name: proxmox-pvesm-and-content-types
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [pvesm, content-types, storage-cfg, pve-storage, storage-id, volume-id, snippets, proxmox, proxmox-ve]
level: practitioner
status: docs-checked
description: "Manage Proxmox storage with pvesm and storage.cfg: storage IDs and volume IDs, content types, node restrictions, listing/allocating/freeing volumes, and orphaned disks."
sources:
  - https://github.com/proxmox/pve-docs/blob/master/pvesm.adoc
  - https://pve.proxmox.com/pve-docs/pve-admin-guide.html#chapter_storage
  - https://github.com/proxmox/pve-docs/blob/master/pve-storage-dir.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pvesm and storage content types

**Goal:** understand and script Proxmox storage definitions and find what is using space.

## storage.cfg
`/etc/pve/storage.cfg` is cluster-wide. Each entry: type, storage ID, options.
```
dir: local
        path /var/lib/vz
        content iso,vztmpl,backup,snippets

lvmthin: local-lvm
        thinpool data
        vgname pve
        content images,rootdir
        nodes pve1,pve2
```
`nodes` restricts the cluster nodes where the storage is usable. `disable` turns a storage
off without deleting it. `shared` only marks an already shared storage as such; it does not
make local storage accessible from other nodes. Avoid several entries pointing at the same
underlying storage (aliasing): two volume IDs can then address one disk image. Do not use
the same storage pool from different clusters (locking does not work between clusters).

## Volume IDs
`<storage-id>:<volume>`, e.g. `local-lvm:vm-101-disk-0`,
`local:iso/debian-13.iso`, `nas:backup/vzdump-qemu-101-2026_10_16-01_00_00.vma.zst`.
Guest configs reference disks by volume ID.

## pvesm commands
```sh
pvesm status                              # usage per storage on this node
pvesm list local-lvm                      # volumes
pvesm list local-lvm --vmid 101
pvesm alloc local-lvm 101 vm-101-disk-5 32G
pvesm free local-lvm:vm-101-disk-5
pvesm path local-lvm:vm-101-disk-0        # device path
pvesm set nas-vm --disable 1
```

## Content types
| Type | For |
|---|---|
| images | VM disks |
| rootdir | container volumes |
| iso | install media |
| vztmpl | container templates |
| backup | vzdump files |
| snippets | cloud-init custom configs, hookscripts |
| import | OVAs and VM disk images that can be imported from this storage |

## Orphaned disks
Disks of deleted VMs, or "unused" disks after detaching, consume space silently:
```sh
qm rescan            # adds unreferenced disks as unusedN entries to their VMID's config
```
Then review each VM's `unused` entries and delete deliberately. Volumes for VMIDs that no
longer exist show in `pvesm list` with no matching guest.

## Verify
`pvesm status` shows every storage active with expected usage; no unexplained volumes
remain after `qm rescan` review.

## Checked

Docs: Proxmox VE admin guide sources (proxmox/pve-docs, master, last commit 2026-10-17) and storage plugin sources (proxmox/pve-storage, master, last commit 2026-10-09).

Confirmed: `/etc/pve/storage.cfg` is cluster-wide and the default `local` entry; the content types listed (images, rootdir, vztmpl, backup, iso, snippets, import); the `nodes`, `shared` and `disable` properties and the aliasing and multi-cluster cautions; volume ID format and `pvesm status|list|alloc|free|path|set --disable`; `qm rescan` description in the qm source ("update disk sizes and unused disk images"). The "PVE 8.2+" gate for `import` was not confirmed and was removed.

Method: documentation only; no commands were run.
