---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.mtp-devices-and-phones-on-windows
name: mtp-devices-and-phones-on-windows
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [mtp-devices, wpd, mobile-forensics, usb-forensics, shellbags, dfir]
level: advanced
status: draft
description: "Investigate MTP and portable devices (phones, cameras) connected to Windows: WPD registry keys, event logs, shellbags and LNK limits for evidence of file transfer."
sources: ["https://www.sans.org/posters/windows-forensic-analysis/", "https://learn.microsoft.com/en-us/windows-hardware/drivers/portable/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# MTP devices and phones on Windows

**Goal:** show a phone or other Media Transfer Protocol device was connected and what was
browsed or transferred, knowing MTP devices do not get drive letters.

## Artefacts
- `SYSTEM\ControlSet00N\Enum\USB\VID_xxxx&PID_yyyy\<serial>` (phone's USB identity, e.g.
  Apple VID 05AC, Samsung 04E8), with Properties times like USBSTOR devices.
- `SYSTEM\...\Enum\SWD\WPDBUSENUM\...` and `SOFTWARE\Microsoft\Windows Portable Devices\Devices\<id>`
  (`FriendlyName` such as "Jane's iPhone").
- Event logs: `Microsoft-Windows-WPD-MTPClassDriver/Operational`, Kernel-PnP Configuration
  400/410, DriverFrameworks-UserMode 2003/2100 (if enabled), Security 6416.
- **Shellbags** (UsrClass.dat): MTP folders appear as shell items under the device (e.g.
  `This PC\Jane's iPhone\Internal Storage\DCIM`), proving the user browsed them; SBECmd
  parses them.
- **LNK/jump lists**: opening a file directly from MTP usually copies it to a temp
  location first (`AppData\Local\Temp\WPDNSE\{GUID}\`), so LNK points to WPDNSE paths: a
  strong indicator of MTP file access.
- Photos app/Windows Photos import history and `Pictures` folder creation times for imports.

## Transfers to the phone
Copying files *to* an MTP device leaves weak evidence: shellbags of the destination folder,
Explorer's `WPDNSE` temp, and source-file access times; the phone itself (if seized) shows
file creation times on its storage.

## Gotchas
- Phones charging only (no MTP mode) appear in USB keys but not WPD; check friendly names.
- iPhones use Apple Mobile Device Support; iTunes/Apple Devices backups
  (`Users\<u>\AppData\Roaming\Apple Computer\MobileSync\Backup` or `Users\<u>\Apple\MobileSync`)
  are separate evidence.

## Verify
Device friendly name, USB serial and shellbag paths agree, and access times fall in the
user's session.
