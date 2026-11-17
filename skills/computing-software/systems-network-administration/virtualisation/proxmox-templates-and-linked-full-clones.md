---
id: computing-software.systems-network-administration.virtualisation.proxmox-templates-and-linked-full-clones
name: proxmox-templates-and-linked-full-clones
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [qm-clone, linked-clone, vm-templates, proxmox, qemu]
level: practitioner
status: docs-checked
description: "Turn Proxmox VE VMs into templates and create linked or full clones with qm clone, including storage support, target nodes and dependency gotchas."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-qm.html
  - https://pve.proxmox.com/pve-docs/qm.1.html
  - https://github.com/proxmox/pve-docs/blob/master/qm-cloud-init.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Templates, linked clones and full clones

**Goal:** fast, consistent VM provisioning from golden images.

## Make a template
```bash
qm shutdown 9000 && qm template 9000
```
A template is read-only and cannot be started, because starting would modify the disk images; to change it, create a linked clone and modify that.

## Clone
```bash
qm clone 9000 201 --name web01                      # for a template, a linked clone is tried by default
qm clone 9000 202 --name db01 --full 1 --storage ceph-rbd   # full, independent copy on another storage
qm clone 9000 203 --name web03 --target pve2        # create on another node (the VM must be on shared storage available on the target)
```

## Linked vs full
| | Linked | Full |
|---|---|---|
| Speed/space | Nearly instantaneous, no extra space initially (copy-on-write) | Reads and copies all VM image data, usually much slower |
| Dependency | Refers to the read-only original; target storage cannot be changed | Independent, no shared storage resources; target storage and format can be chosen |
| Storage | Needs a storage driver with linked clone support (storage internal feature) | Any |

## Gotchas
- You cannot delete an original template while linked clones exist.
- Linked clones need the original to be read-only, which is why a VM is first converted to a template; check the Clones column of the storage table for your storage type.
- Cloning a running VM issues a guest-agent freeze if the agent is enabled; `--snapname` clones a specific snapshot, and the copy never includes the original's other snapshots.
- Clone operations randomise network interface MAC addresses and generate a new smbios1 UUID.
- Pair templates with cloud-init (`qm set 9000 --ide2 <storage>:cloudinit`) to give each clone its own hostname, SSH key and IP (`--sshkey`, `--ipconfig0`).

## Verify
`qm config 201` shows the clone's own disk volumes and a new MAC address; the clone boots with its own identity.

## Checked

2026-10-26 against the Proxmox VE admin guide sources (github.com/proxmox/pve-docs master, last commit 2026-10-17: qm.adoc Copies and Clones and Virtual Machine Templates, generated qm.1-synopsis.adoc clone options, qm-cloud-init.adoc, pvesm.adoc storage table) and confirmed the clone option names (--full, --name, --snapname, --storage, --target), the default linked-clone behaviour for templates, the template read-only rule, the template deletion restriction and the MAC and UUID randomisation. Removed the unconfirmed base-disk naming, per-storage linked-clone matrix, machine-id command and move-disk conversion claims.

Method: documentation only; no commands were run.
