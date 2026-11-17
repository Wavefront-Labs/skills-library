---
id: computing-software.systems-network-administration.virtualisation.proxmox-windows-guests-virtio
name: proxmox-windows-guests-virtio
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [virtio-win, windows-guest-proxmox, virtio-drivers, balloon-driver, qemu-guest-agent, windows-11, vtpm, proxmox-vm, proxmox, proxmox-ve]
level: practitioner
status: docs-checked
description: "Install Windows on Proxmox VE with VirtIO: load vioscsi/NetKVM during setup, guest tools installer, ballooning service, Windows 11 TPM/Secure Boot, and machine version pinning."
sources:
  - https://pve.proxmox.com/wiki/Windows_VirtIO_Drivers
  - https://pve.proxmox.com/wiki/Windows_2022_guest_best_practices
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Windows guests on Proxmox VE with VirtIO

**Goal:** Windows VMs using paravirtual disk and network drivers (fast) with the guest
agent and balloon service working.

## Build
- Settings: OS type `win11`/`win10`, machine **q35**, BIOS **OVMF** with EFI disk
  (pre-enrolled keys for Secure Boot), **TPM v2.0** state disk for Windows 11,
  a suitable CPU type, disk on **VirtIO SCSI single** with `discard=on`, NIC
  **VirtIO**.
- Attach two CD drives: Windows ISO and the **virtio-win ISO** (see the Windows VirtIO
  Drivers wiki page for downloads).

## During setup
At "Where do you want to install Windows?" → Load driver → browse the virtio-win CD:
`vioscsi\<os>\amd64` for the disk. Optionally also load `NetKVM\<os>\amd64` for
networking now.

## After setup
Run `virtio-win-guest-tools.exe` from the ISO: installs the VirtIO drivers and the **QEMU guest agent**. Enable the agent in VM Options (`qm set <id> --agent 1`), then fully stop and
start the VM.

## Settings worth knowing
- Pin the machine version (e.g. `pc-q35-9.0`) so QEMU upgrades don't change virtual
  hardware and trigger Windows re-activation or NIC re-detection (see the machine version setting in the admin guide).
- Ballooning: the Windows balloon driver must be installed manually and can slow the guest; set a sensible minimum or
  disable ballooning for SQL/Exchange.
- Time: Windows uses RTC local time; PVE sets `localtime=1` for Windows OS types.

## Gotchas
- Switching the boot disk to VirtIO needs the driver installed first; see the Windows VirtIO Drivers wiki page.

## Verify
Device Manager shows no unknown devices; `qm agent <id> ping` succeeds; PVE summary shows
the guest IP; Memory in PVE reflects balloon reporting.

## Checked

2026-10-28

Confirmed: Windows VirtIO Drivers and Windows 2022 best-practices wiki, admin guide qm options: vioscsi and NetKVM driver folders, virtio-win-guest-tools, q35, OVMF, machine version format, localtime default for Windows, balloon driver note.

Removed or corrected: Fedora virtio-win sourcing, CPU type and Server 2025 TPM specifics, driver list of the guest tools, 8.1 pinning claim, Hyper-V enlightenment claim, three unsupported gotchas.

Method: documentation only; no commands were run.
