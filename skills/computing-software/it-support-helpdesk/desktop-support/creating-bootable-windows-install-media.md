---
id: computing-software.it-support-helpdesk.desktop-support.creating-bootable-windows-install-media
name: creating-bootable-windows-install-media
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, windows-installation, bootable-usb, media-creation-tool, install-wim, fat32, dism, comptia-a-plus]
level: practitioner
status: docs-checked
description: "Build a Windows 10/11 install USB with the Media Creation Tool or by hand: FAT32 format, copying the ISO, the 4 GB install.wim limit and splitting it with DISM."
sources:
  - "https://www.microsoft.com/software-download/windows11"
  - "https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/install-windows-from-a-usb-flash-drive"
  - "https://www.comptia.org/certifications/a"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# creating-bootable-windows-install-media

Goal: a USB stick that boots the target PC and installs Windows, without
hitting the "file too large" surprise.

## Pick the method
| Situation | Use |
|---|---|
| Easy, automated, internet available | Microsoft Media Creation Tool (MCT) from the Download Windows 11 or 10 page |
| Need an ISO to keep or use in a VM | The disk image (ISO) download on the same page, or the MCT "ISO file" option |
| Manufacturer or locked-down build bench | Manual copy of the ISO contents to a FAT32 flash drive (below) |

## Media Creation Tool
- Run it as an administrator. The Windows 11 tool creates media for x64
  processors only; Arm-based PCs are not supported by it.
- Choose "USB flash drive" and attach a blank USB drive with at least 8 GB of
  space. Anything on the drive is deleted.
- The Windows 11 ISO download is a multi-edition ISO that uses the product key
  to unlock the correct edition.
- The page shows how to compute an ISO hash with PowerShell's `Get-FileHash`
  and lists published hash values per language.

## Manual build
Needs the installation ISO or DVD, a flash drive with at least 5 GB free
(it will be formatted), a technician PC and the target device.
1. Format the flash drive as FAT32 so it boots BIOS-based and UEFI-based PCs.
   In Disk Management right-click the partition, Format, FAT32.
2. Mark the partition active (Disk Management, or `diskpart` to select it and
   mark it active).
3. Copy the entire contents of the ISO or DVD to the drive with File Explorer.
   Optionally add an unattend file to automate setup.
4. Boot the target and press its boot-device menu key (for example
   Esc, F10 or F12), choose the flash drive, then follow Windows Setup.
   Consult the device maker if it will not boot from USB.

### If `install.wim` is over 4 GB
FAT32 has a 4 GB file size limit. With `D:` the mounted ISO and `E:` the
flash drive, as in Microsoft's example:
```
robocopy D: E: /s /max:3800000000
Dism /Split-Image /ImageFile:<ISO-drive>\sources\install.wim /SWMFile:<USB-drive>\sources\install.swm /FileSize:3800
```
Windows Setup installs from the split files automatically as long as the first
is named `install.swm`.

## Gotchas
- If the PC does not list the USB device as a boot option, open its firmware
  boot menu or boot order; Microsoft's download page also suggests asking the
  PC maker how to temporarily disable Secure Boot.
- An `autounattend.xml` or other unattend file on the stick drives the install;
  label such sticks clearly. See the autounattend skill for what it can do.
- Mounting the ISO and running `setup.exe` is an upgrade of the running OS,
  not a clean install from media.

## Verify
The target shows the stick in its boot menu, Windows Setup starts, and the
edition and disk shown are the expected ones.

## Checked

Date 2026-11-08. Pages: Download Windows 11 (Microsoft), Install Windows from a Flash Drive (Microsoft Learn); the CompTIA A+ page was read but covers no claim here. Confirmed: MCT administrator and x64 note, 8 GB USB, FAT32 and 4 GB limit, robocopy and DISM split commands, install.swm naming, 5 GB free space, boot menu keys, Secure Boot note, multi-edition ISO. Removed as not on the cited pages: Rufus and Ventoy guidance, the diskpart clean/convert gpt build, Intel VMD driver loading, `ei.cfg` edition selection, VLSC and admin centre ISO source, MBR/CSM install behaviour, MCT ESD size remark and the Verify dism commands.

Method: docs-only read of cited pages, 2026-11-08
