---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.shellbags-jumplists-and-usb-device-history
name: shellbags-jumplists-and-usb-device-history
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [shellbags, jump-lists, automaticdestinations, customdestinations, usb-forensics, mounteddevices, setupapi, sbecmd, jlecmd, eric-zimmerman-tools, folder-access-history, removable-media, usb-device-serial, dfir, windows-forensics]
level: advanced
status: draft
description: "Reconstruct which folders a user browsed, which files/apps they opened, and which USB devices connected and when, from Shellbags, Jump Lists and registry device keys."
sources: ["https://ericzimmerman.github.io/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Shellbags, jump lists and USB device history

**Goal:** answer "did the user browse this folder / open this file / plug in this
drive, and when" — a different question from the execution/persistence focus of
computing-software.digital-forensics-incident-response.disk-memory-forensics.super-timeline-with-plaso,
answered from artefacts that often outlive the thing they describe (a Shellbag entry
for a USB drive's folder survives after the drive is gone).

## 1. Shellbags
Windows Explorer remembers window position/view settings for every folder a user has
opened, including folders on **removed** drives, network shares, and deleted local
folders — the registry entry persists even after the folder is gone. Stored in
`UsrClass.dat` (Shell\BagMRU, Shell\Bags) per user.
```
SBECmd.exe -d <profile>\AppData\Local\Microsoft\Windows\UsrClass.dat --csv out\
```
Each entry carries a **first-interacted** and **last-interacted** timestamp (from the
embedded FILETIME in the shell item) plus the full path, even for a path that no
longer resolves. This is strong evidence a user *navigated into* a folder — it does
not by itself prove a specific file inside was opened or exfiltrated; pair with
LNK/Jump List evidence (below) or USN Journal entries for that.

## 2. Jump Lists
Two files per application ID (AppID, an 8-hex-char hash of the exe path) under
`AppData\Roaming\Microsoft\Windows\Recent\AutomaticDestinations\` and
`CustomDestinations\`:
- **AutomaticDestinations** (`.automaticDestinations-ms`) — auto-populated recent-file
  list, a structured-storage (OLE CFB) file containing embedded LNK streams. Each
  stream is a full LNK record with target path, volume serial number, MAC times of the
  target *at the time it was opened*, and sometimes a network share UNC path.
- **CustomDestinations** (`.customDestinations-ms`) — app-pinned items, less reliably
  timestamped.
```
JLECmd.exe -d <profile>\AppData\Roaming\Microsoft\Windows\Recent\AutomaticDestinations --csv out\
```
AppID-to-application mapping isn't always obvious; Eric Zimmerman's tools ship a
lookup list, but an unrecognised AppID means manually hashing candidate exe paths or
accepting it as unknown. A Jump List entry for a file on a volume with a **matching
USB device serial** (see below) is strong, specific evidence that a particular file on
a particular removable drive was opened by a particular application at a known time.

## 3. USB device history
No single key gives "device X connected at time Y" directly — build it from several:
- `SYSTEM\CurrentControlSet\Enum\USBSTOR` — device descriptor + serial number, with the
  key's **last-written time** approximating first-connection (not last).
- `SOFTWARE\Microsoft\Windows Portable Devices\Devices` and
  `SYSTEM\...\Enum\SWD\WPDBUSENUM` — richer for MTP/media devices (phones, cameras).
- `SYSTEM\MountedDevices` maps a volume serial number to a drive letter — this is what
  lets you correlate a Shellbag/LNK volume serial back to a specific physical USB
  device's USBSTOR entry.
- `<WINDIR>\inf\setupapi.dev.log` has a per-installation timestamped log entry for
  every PnP device Windows installed a driver for, including USB mass storage — the
  closest thing to a precise connection timestamp, when the log hasn't rolled over.
- Volume serial number inside an LNK/Jump List record is the join key tying "a file was
  opened from drive X" back to "drive X is USB device with serial Y."

## Verify
- Corroborate any single-artefact USB connection claim (e.g. USBSTOR key time) against
  setupapi.dev.log and MountedDevices before dating a connection event precisely.
- Confirm a Shellbag/Jump List target path's volume serial actually matches the USB
  device serial you're attributing it to — don't assume by drive letter alone, letters
  are reused across devices.
- When citing "user opened file X from drive Y," show the LNK target MAC times, the
  volume serial match, and the USBSTOR connection window together, not any one alone.

Unconfirmed: Jump List AppID hash algorithm coverage in public lookup tables is
incomplete for less common / custom apps — verify an unknown AppID empirically
(open the app, check what list it creates) before asserting what produced it.
