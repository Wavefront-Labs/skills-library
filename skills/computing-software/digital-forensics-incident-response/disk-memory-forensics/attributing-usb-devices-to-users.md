---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.attributing-usb-devices-to-users
name: attributing-usb-devices-to-users
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [mountpoints2, volume-serial-number, usb-forensics, user-attribution, lnk, dfir]
level: practitioner
status: draft
description: "Attribute a USB device to a user account via MountPoints2 volume GUIDs and link files on the device using the volume serial number from LNK and jump lists."
sources: ["https://www.sans.org/posters/windows-forensic-analysis/", "https://ericzimmerman.github.io/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Attributing USB devices to users

**Goal:** connect a specific removable volume to a specific user profile, and show which
files that user opened from it.

## MountPoints2
`NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\Explorer\MountPoints2\{volume GUID}`
- Exists in a user's hive if that user was logged on when the volume was mounted (or
  accessed it). Key **last write time** approximates the last time that user had it mounted.
- Map the volume GUID to the device via `SYSTEM\MountedDevices`: value
  `\??\Volume{GUID}` whose data contains the USBSTOR device path with the serial.

## Volume serial number (VSN)
- A filesystem property set at format time (e.g. `A4F2-91C3`), different from the USB
  hardware serial.
- Get it from: Partition/Diagnostic Event 1006 VBR bytes, `EMDMgmt` key in SOFTWARE
  (`Microsoft\Windows NT\CurrentVersion\EMDMgmt`, ReadyBoost; older systems), or the device
  itself (`fsstat` on its image).
- LNK files and jump list entries store the **drive type** (removable) and **VSN** of the
  target's volume (LECmd/JLECmd output columns `DriveType`, `VolumeSerialNumber`).

## Workflow
1. USBSTOR serial -> MountedDevices volume GUID -> MountPoints2 in which user hive.
2. VSN of that volume -> filter LNK/jump list entries by VSN -> files opened from the
   device, with their times and paths.
3. Shellbags with the device's drive letter/volume for folders browsed.

## Gotchas
- Drive letters get reused; never match by letter alone.
- Reformatting changes the VSN; the hardware serial stays.

## Verify
At least two independent links (MountPoints2 and LNK with VSN) tie the device to the user,
and times fall inside that user's logon sessions.
