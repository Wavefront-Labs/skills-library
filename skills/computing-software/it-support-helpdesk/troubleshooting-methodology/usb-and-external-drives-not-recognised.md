---
id: computing-software.it-support-helpdesk.troubleshooting-methodology.usb-and-external-drives-not-recognised
name: usb-and-external-drives-not-recognised
category: computing-software
field: it-support-helpdesk
product: troubleshooting-methodology
tags: [it-support-helpdesk, troubleshooting-methodology, usb-not-recognized, external-drive, usb-troubleshooting, disk-management, device-manager]
level: practitioner
status: draft
description: "Fix USB devices and external drives that aren't recognised: power, ports and cables, Device Manager errors, selective suspend, drive letters, and file system or policy blocks."
sources:
  - "https://support.microsoft.com/en-us/windows/fix-usb-c-problems-in-windows-f4e0e529-74f5-cdae-3194-43743f30eed2"
  - "https://learn.microsoft.com/en-us/windows-server/storage/disk-management/troubleshooting-disk-management"
  - "https://learn.microsoft.com/en-us/defender-endpoint/device-control-overview"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# usb-and-external-drives-not-recognised

## Work from the outside in
1. **Another port and cable**: front-panel and hub ports are often underpowered; use a
   rear motherboard port or the laptop's own port. USB-C cables vary (charge-only
   cables carry no data).
2. **Another computer**: if it fails everywhere, it's the device.
3. **Power**: 2.5" drives draw from the port; 3.5" drives need their adapter. Hubs need
   their own power for drives.

## Windows: "USB device not recognized"
- Device Manager > Universal Serial Bus controllers / Other devices: Unknown device with
  code 43 ("Windows has stopped this device because it has reported problems") means
  the device failed to enumerate: try another cable/port, power-drain the PC (shut
  down, unplug, hold power 15 s).
- Uninstall the device (and USB Root Hub entries) and scan for hardware changes.
- Disable USB selective suspend for troubleshooting: Power Options > Advanced > USB
  settings; and in Device Manager > USB Root Hub > Power Management.
- Chipset and USB controller drivers from the vendor; BIOS update for USB-C/TB issues.
- Event Viewer: Microsoft-Windows-Kernel-PnP > Configuration log.

## External drive detected but not in Explorer
- Open Disk Management (`diskmgmt.msc`):
  | Shows as | Fix |
  |---|---|
  | Online, healthy, no drive letter | Change Drive Letter and Paths > Add |
  | Unallocated | New Simple Volume (destroys nothing if truly empty; check first) |
  | RAW | File system damaged or unsupported (e.g. ext4/APFS); don't format if data needed |
  | Not initialized | New disk, or partition table lost; for existing data use recovery tools |
  | Offline | Right-click > Online (policy SAN or signature collision) |
- macOS drives (APFS/HFS+) aren't readable on Windows natively; exFAT works on both.
- Drive letter conflicts with mapped network drives: assign a letter outside the
  mapped range.

## Policy blocks
- Device control / removable storage policies (Intune, GPO, Defender) may allow read-only
  or block entirely; the user sees "access denied" or nothing. Check before replacing
  hardware; exceptions go through security.
- BitLocker To Go encrypted drives prompt for a password; policy may require encrypting
  before writing.

## Verify
The device appears in Device Manager without errors and the drive opens with its data;
if it failed on several machines it's replaced and the data question resolved.
