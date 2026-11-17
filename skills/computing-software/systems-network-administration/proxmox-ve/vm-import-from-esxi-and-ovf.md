---
id: computing-software.systems-network-administration.proxmox-ve.vm-import-from-esxi-and-ovf
name: vm-import-from-esxi-and-ovf
category: computing-software
field: systems-network-administration
product: proxmox-ve
tags: [esxi-import, ova, ovf, import-wizard, qm-importovf]
level: practitioner
status: docs-checked
description: "Import virtual machines from ESXi or OVA and OVF files into Proxmox VE using the import wizard or qm."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-qm.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Three common routes to bring in a VM: the native import wizard (uses the `import` content type, as provided by the special ESXi storage), backup on the source and restore on the target (best when the source is another Proxmox VE), or the OVF-specific import command of `qm`.

Import wizard: added in Proxmox VE 8.2 and still tech preview, though stable in practice. Add a storage for the import source under Datacenter, Storage, Add. Select it in the resource tree, open the Virtual Guests content tab, select a guest and click Import (or double-click). It has been tested with ESXi 6.5 through 8.0. Guests using vSAN must have their disks moved to another storage first. Using vCenter as the source works but is 5 to 10 times slower.

OVA or OVF files: first have a file-based storage with the `import` content type. That storage gets an `import` folder where you put OVA files, or OVF files together with their images, in a flat structure. Then they appear for import in the GUI. The CLI form is `qm importovf <vmid> <manifest> <storage>`.

After import, adapt the guest to the new hypervisor: install the QEMU guest agent and VirtIO drivers, and remember vmxnet3 NICs are only meant for imported VMs.

## Checked

2026-11-09. Confirmed against the Proxmox VE docs chapter Qemu/KVM Virtual Machines (chapter-qm), Importing Virtual Machines section: import wizard added in 8.2 and in tech preview, tested ESXi 6.5 to 8.0, vSAN caveat, vCenter 5 to 10 times slower, import content type and flat import folder, qm importovf, vmxnet3 note.

Method: documentation only; no commands were run.
