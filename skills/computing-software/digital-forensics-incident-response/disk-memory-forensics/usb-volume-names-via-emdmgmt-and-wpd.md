---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.usb-volume-names-via-emdmgmt-and-wpd
name: usb-volume-names-via-emdmgmt-and-wpd
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [emdmgmt, usb-forensics, removable-media, volume-serial-number, dfir]
level: practitioner
status: draft
description: "Recover USB volume names and serials from EMDMgmt, Windows Portable Devices and VolumeInfoCache to link LNK targets and user activity to a specific device."
sources: ["https://www.sans.org/posters/windows-forensic-analysis/", "https://www.13cubed.com/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# USB volume names via EMDMgmt and WPD

**Goal:** USBSTOR identifies the physical device; LNK files and shellbags record a volume label
and volume serial number. These keys bridge the two.

## SOFTWARE hive keys
| Key | Content |
|---|---|
| `Microsoft\Windows NT\CurrentVersion\EMDMgmt` | ReadyBoost evaluation of non-SSD removable devices: subkey names include device serial, **volume name** and **volume serial number (decimal)**; key last-write time. Not present when the system drive is an SSD (ReadyBoost disabled) |
| `Microsoft\Windows Portable Devices\Devices` | Per device: `FriendlyName` = volume label at time of connection, device instance path containing serial |
| `Microsoft\Windows Search\VolumeInfoCache\<letter>:` | `VolumeLabel` last seen per drive letter |
| `SYSTEM\MountedDevices` | Drive letter and volume GUID mapping to device instance |

## Linking workflow
1. USBSTOR: vendor/product/serial `ABC123&0`.
2. WPD `FriendlyName` for the same serial: e.g. `PROJECTS`.
3. EMDMgmt subkey `..._ABC123_PROJECTS_1234567890` - convert decimal VSN to hex (`1234567890` = `499602D2`).
4. LNK/jump list entries with volume serial `499602D2` and label `PROJECTS` -> files opened from that device.
5. MountPoints2 (NTUSER) volume GUID -> which user mounted it.

## Gotchas
- Volume serial numbers change when the device is reformatted; labels are user-editable.
- EMDMgmt absent on SSD systems (common today); rely on WPD, partition diagnostic log (event 1006 contains VBR with VSN), and LNK data.
- Hex vs decimal VSN representations differ across tools.

## Verify
At least two independent artefacts tie the volume serial to the USBSTOR serial before attributing file access to a device.
