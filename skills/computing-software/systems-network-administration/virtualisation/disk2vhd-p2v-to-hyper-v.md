---
id: computing-software.systems-network-administration.virtualisation.disk2vhd-p2v-to-hyper-v
name: disk2vhd-p2v-to-hyper-v
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [disk2vhd, p2v, hyper-v, sysinternals, vhdx]
level: practitioner
status: docs-checked
description: "Convert a physical Windows machine to Hyper-V with Sysinternals Disk2vhd: snapshot capture to VHD files, building the VM, avoiding duplicate identity and cleanup."
sources:
  - https://learn.microsoft.com/en-us/sysinternals/downloads/disk2vhd
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/plan/should-i-create-a-generation-1-or-2-virtual-machine-in-hyper-v
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Disk2vhd P2V to Hyper-V

**Goal:** a quick, free P2V of a Windows machine into a Hyper-V VM.

## Capture
Disk2vhd runs on the live system and uses the Windows volume snapshot capability for consistent point-in-time copies.
- Select every volume needed to boot (system/EFI partition, OS volume) plus any data volumes you want.
- It creates **one VHD per physical disk** that holds a selected volume; it keeps the partition layout but copies
  data only for the selected volumes.
- Writing the VHD to a different disk than the ones being converted performs better; writing to a converted volume
  is allowed.
- Command line: `disk2vhd <drive: [drive:]...| *> <vhdfile>`, for example `disk2vhd * <path>\snapshot.vhd`
  (`*` means all volumes). Check the tool's own UI for the choice of VHD versus VHDX output.

## Build the VM
- Add the captured disk(s) to a new VM. The Sysinternals page says to attach them as IDE disks, which is the
  Generation 1 layout.
- Generation 2 VMs use UEFI firmware and SCSI boot disks; use them only if the source booted in UEFI mode and the
  disk image is compatible with UEFI. Check Microsoft's generation guidance before choosing.
```powershell
New-VM -Name srv01 -Generation 1 -MemoryStartupBytes 8GB -VHDPath '<PATH>\srv01.vhd' -SwitchName vIsolated
Set-VMProcessor -VMName srv01 -Count 4
```
Copy the file to the target storage first rather than running it from a share.

## First boot
- Do not attach the VHD on the system that created it if you plan to boot from it: Windows assigns a new disk
  signature and the BCD then cannot find the boot disk.
- On first boot Windows detects the VM hardware and installs drivers present in the image; install Hyper-V
  integration components if drivers are missing.
- Connect the VM to an **isolated virtual switch** first, because the source may still be running with the same
  name, SID and IP.
- Re-enter the static IP on the new adapter, remove ghost NICs, then power down the physical server before
  connecting the VM to production.

## Gotchas
- Disk2vhd does not support volumes with BitLocker enabled: turn BitLocker off and wait for full decryption first.
- Licensing: the Sysinternals page says OEM-installed Windows XP, Vista and 7 may not be transferred to a virtual
  hard disk under Microsoft licensing terms. For current Windows versions check your licence terms before P2V.
- Virtual PC supports a maximum virtual disk size of 127 GB; this does not apply to Hyper-V.

## Verify
The VM boots, services start, and after cutover the source is powered off with no duplicate name or IP on the network.

## Checked

Date checked: 2026-10-27. Documentation: Sysinternals Disk2vhd page (v2.02, 2021-10-12) and the Hyper-V generation 1 versus 2 page.
Confirmed: snapshot-based online capture; one VHD per disk; command-line grammar; attach as IDE disks; do not boot the VHD on its source system; BitLocker unsupported until fully decrypted; OEM licence statement; Gen 2 uses UEFI and SCSI boot.

Method: documentation only; no commands were run.
