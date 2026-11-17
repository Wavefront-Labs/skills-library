---
id: computing-software.digital-forensics-incident-response.incident-response-process.proving-data-exfiltration-to-removable-media
name: proving-data-exfiltration-to-removable-media
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [usb-exfiltration, insider-threat, data-exfiltration, usb-forensics, removable-media, dfir]
level: advanced
status: draft
description: "Prove or rule out copying of data to USB removable media in an insider case: device identity, connection times, file access on the device, and corroboration."
sources: ["https://www.sans.org/posters/windows-forensic-analysis/", "https://ericzimmerman.github.io/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Proving data exfiltration to removable media

**Goal:** show that a specific device was connected by a specific user at a specific time
and that specific files were copied or opened from it. Windows does not log "file copied to
USB" by default, so the case is built from corroborating artefacts.

## Steps
1. **Device identity**: SYSTEM hive `USBSTOR` and `USB` keys (vendor, product, serial),
   `MountedDevices` (drive letter and volume GUID), `Windows Portable Devices`, and the
   `Microsoft-Windows-Partition/Diagnostic` event log (Event 1006: serial, size, and raw
   partition table/VBR, which gives the **volume serial number**).
2. **Connection times**: `Properties\{83da6326...}` keys 0064 (first install), 0066 (last
   connected), 0067 (last removal); Kernel-PnP and DriverFrameworks events; setupapi.dev.log
   for first connection.
3. **User attribution**: `NTUSER.DAT\...\Explorer\MountPoints2\{volume GUID}` shows the
   user who had the volume mounted.
4. **Files on the device**: LNK files and jump lists with the device's **volume serial
   number** and drive type "removable"; shellbags for folders browsed on the drive; Office
   recent files pointing to `E:\`.
5. **Copy indicators**: source files' **last access** timestamps (if enabled) clustering at
   the connection time, `$UsnJrnl` showing no change to the source (copy reads only),
   Explorer copy dialogs are not logged; DLP/EDR file events (Defender `DeviceFileEvents`
   with `FolderPath` on removable media), Windows audit 4663 with Removable Storage auditing.
6. **The device itself** if recovered: image it, compare file hashes and $MFT creation times
   on the device with the source.

## Gotchas
- Last access updates are often disabled (`NtfsDisableLastAccessUpdate`), check the value.
- LNK files show a file was *opened from* the device, not that it was copied there.
- MTP phones do not appear as drive letters; check WPD keys and shellbags.

## Verify
Present a timeline: connection, user session active (4624/4800), files opened from the
device volume serial, disconnection. Each line cites its artefact.
