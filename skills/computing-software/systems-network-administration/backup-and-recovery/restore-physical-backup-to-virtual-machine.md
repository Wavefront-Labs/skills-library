---
id: computing-software.systems-network-administration.backup-and-recovery.restore-physical-backup-to-virtual-machine
name: restore-physical-backup-to-virtual-machine
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [restore-to-virtual, p2v-restore, disk2vhd, virtio-drivers]
level: advanced
status: docs-checked
description: "Bring a physical server back as a VM: Disk2vhd limits, firmware type, disk drivers in the initramfs, network and tool clean-up on first boot."
sources:
  - https://learn.microsoft.com/en-us/sysinternals/downloads/disk2vhd
  - https://pve.proxmox.com/wiki/Migration_of_servers_to_Proxmox_VE
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Restoring physical backups to a VM

**Goal:** a failed or retiring physical server runs as a VM on existing virtual infrastructure, faster than waiting for hardware.

## Disk2vhd (live P2V of a Windows machine)
- Creates one VHD per disk containing selected volumes; it keeps the partitioning of the disk but copies data only for selected volumes, so you can capture system volumes and skip data volumes.
- Scriptable: `disk2vhd <[drive: [drive:]...]|[*]> <vhdfile>`, where `*` selects all volumes.
- Do not attach the VHD on the system where you created it if you plan to boot from it: Windows assigns a new disk signature, the BCD references disks by signature, and the VM then fails to find its boot disk.
- Volumes with BitLocker are not supported; turn BitLocker off and wait for full decryption first.
- Virtual PC supports virtual disks only up to 127 GB.

## VM settings to match
- Firmware follows the source: legacy BIOS mode needs a BIOS VM (SeaBIOS in Proxmox); UEFI needs UEFI (OVMF). Some operating systems set only a custom UEFI boot path and not the default `/EFI/BOOT/BOOTX64.EFI`, so the VM will not boot until you add the boot entry in the UEFI setup; in Proxmox an EFI disk is needed to persist it.
- Disk controller: install and load VirtIO drivers in the guest (in the initramfs on Linux) before migrating. If a Linux VM no longer boots because it lacks a virtio SCSI driver, boot a rescue entry (its initramfs normally contains more drivers) or temporarily use IDE or SATA for the disk bus. Windows needs extra steps to switch the boot disk to VirtIO SCSI drivers.

## Before and after the move
- Remove guest tools specific to the old hypervisor before migrating; they can be hard to remove afterwards.
- Note the guest network configuration so you can restore it by hand.
- On Windows, consider removing static network settings first: the adapter changes and Windows warns if the same IP is set on another adapter.
- DHCP reservations: update them to the new MAC address, or set the MAC on the target VM NIC manually.
- Full-disk encryption with keys in a virtual TPM: the Proxmox page says vTPM state cannot be migrated from VMware; keep manual recovery keys.

## Verify
Application owner signs off after a functional test; record the time taken as the RTO for "hardware loss, restore as VM".

## Checked

2026-11-09. Confirmed against the Sysinternals Disk2vhd page (volumes, usage, disk signature warning, BitLocker, 127 GB Virtual PC limit) and the Proxmox "Migration of servers to Proxmox VE" page (VirtIO drivers and initramfs, rescue entry or IDE/SATA, BIOS/UEFI, preparation list). Partial read of the long Proxmox page (guest sections only). Removed: Veeam Agent, Windows Server Backup, Clonezilla and ReaR restore routes, `dracut` and `update-initramfs` commands, `/etc/fstab` and NIC naming advice, vendor agent and ghost NIC removal, licence reactivation, passthrough and hardware-dependency remarks (not on cited pages).

Method: documentation only; no commands were run.
