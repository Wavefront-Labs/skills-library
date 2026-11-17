---
id: computing-software.systems-network-administration.virtualisation.proxmox-import-disks-and-esxi-vms
name: proxmox-import-disks-and-esxi-vms
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [qm-importdisk, esxi-import-wizard, qm-importovf, vmware-to-proxmox, v2v, import-storage, proxmox-vm, proxmox, proxmox-ve]
level: practitioner
status: docs-checked
description: "Bring VMs into Proxmox: the ESXi import wizard, qm disk import for VMDK/qcow2/raw, qm importovf for OVF exports, and post-import driver and boot fixes."
sources:
  - https://pve.proxmox.com/wiki/Migrate_to_Proxmox_VE
  - https://pve.proxmox.com/pve-docs/qm.1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Importing disks and ESXi VMs into Proxmox VE

**Goal:** move existing VMs (especially from VMware) to Proxmox with minimal downtime and
no unbootable guests.

## ESXi import wizard
1. Datacenter → Storage → Add → **ESXi**: host or vCenter address and credentials.
2. Browse the storage, select a VM → Import: choose target storage, bridge, CPU type,
   disk bus (keep SATA/IDE for Windows first boot if VirtIO drivers are not installed).
3. **Live import** option starts the VM while disks copy in the background (reduces downtime; the PVE docs warn of possible hanging IO for
   live-imported guests, so test first).

## Manual import of disks
```sh
qm create 140 --name legacy01 --memory 4096 --cores 2 --net0 virtio,bridge=vmbr0 --scsihw virtio-scsi-single
qm disk import 140 /mnt/import/legacy01.vmdk local-lvm --format raw
qm set 140 --scsi0 local-lvm:vm-140-disk-0 --boot order=scsi0
# OVF exported from vSphere:
qm importovf 141 /mnt/import/app.ovf local-lvm
```
`qm disk import` (alias `qm importdisk`) accepts image formats supported by qemu-img. The disk appears as `unused0` until attached.

## Post-import fixes
- **Windows:** install VirtIO drivers *before* migration if possible (virtio-win ISO),
  otherwise boot on SATA, add a small VirtIO SCSI disk to load the driver, then switch
  the boot disk to SCSI. Remove VMware Tools after. Expect a new NIC (re-enter static IP).
- **Linux:** rebuild initramfs with virtio modules if missing (use the distribution's initramfs tool); NIC name changes (ens192 → ens18): fix netplan/ifcfg.
- Firmware must match: a UEFI VM in VMware needs `--bios ovmf` + EFI disk in PVE.
- Install `qemu-guest-agent`.

## Gotchas
- VMs with disks on VMware vSAN cannot be imported; move the disks to other storage first.
- Large estates: plan waves, test each OS type first.

## Verify
VM boots, gets its IP, guest agent responds (`qm agent 140 ping`), application smoke
test passes; source VM kept powered off until sign-off.

## Checked

2026-10-28

Confirmed: Migrate to Proxmox VE wiki and qm man page: vSAN limitation, live-import, qm disk import and its importdisk alias, qm importovf, qemu-img format support, --bios ovmf, qm agent.

Removed or corrected: the PVE 8.2 version gate, the ESXi-host-faster claim, thick VMDK size claim, encrypted-VM claim, dracut.

Method: documentation only; no commands were run.
