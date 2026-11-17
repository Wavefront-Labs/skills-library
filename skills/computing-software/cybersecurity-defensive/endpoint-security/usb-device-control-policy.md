---
id: computing-software.cybersecurity-defensive.endpoint-security.usb-device-control-policy
name: usb-device-control-policy
category: computing-software
field: cybersecurity-defensive
product: endpoint-security
tags: [device-control, usb-device-control, removable-storage, defender-device-control, device-installation-restrictions, bitlocker-to-go, approved-usb-devices]
level: practitioner
status: draft
description: "Control USB and removable storage: block by default, allow approved encrypted devices by ID, read-only options, Defender device control policies and audit events."
sources: ["CIS Control 10.3 and 3.9 (disable autorun, encrypt data on removable media)", "Microsoft Learn - Device control in Microsoft Defender for Endpoint", "Microsoft Learn - Manage device installation with Group Policy"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# USB device control policy

**Goal:** removable media cannot be used to bring malware in or take data out, except approved
encrypted devices for users with a business need.

## Policy design
| Group | Removable storage |
|---|---|
| Default users | Deny write and execute; read allowed or denied per risk appetite |
| Approved users (business need) | Read/write only to approved corporate encrypted devices (by VID/PID/serial) |
| Kiosks, servers, OT | Deny all |
Allow other USB classes (keyboards, mice, headsets, smart cards) explicitly; block mass storage, MTP (phones), and optionally printers/CD.

## Windows implementation options
1. **Defender for Endpoint device control** (removable storage access control): groups by
   `VID_PID`, `SerialNumberId`, `InstancePathId`, `BusId`; rules with Read/Write/Execute masks
   and audit options; deploy via Intune (Settings catalog > Defender > Device Control) or GPO XML.
2. **Device installation restrictions** (GPO / Intune Device Restrictions): "Prevent installation of devices that match these device setup classes" (Disk drives class `{4d36e967-e325-11ce-bfc1-08002be10318}`) with allow lists by hardware ID.
3. **BitLocker To Go**: "Deny write access to removable drives not protected by BitLocker".

macOS: MDM restrictions or EDR/device-control products (Jamf Protect, Defender for Endpoint on macOS device control). Linux: `usbguard` (`usbguard generate-policy`, then allow by ID).

## Monitoring
Defender advanced hunting:
```
DeviceEvents | where ActionType in ("RemovableStorageFileEvent","PnpDeviceConnected","RemovableStoragePolicyTriggered")
| project Timestamp, DeviceName, InitiatingProcessAccountName, AdditionalFields
```
Large copies to approved USB devices feed DLP/insider risk.

## Gotchas
- VID/PID can be spoofed by malicious USB hardware; serial-number allow lists of issued devices are stronger.
- HID attacks (rogue keyboards, "Rubber Ducky") are not stopped by storage controls; consider blocking new HID devices on sensitive systems.
- Blocking phones (MTP) breaks charging-plus-sync for some workflows; communicate.

## Verify
- [ ] Unapproved USB stick: write blocked, event logged.
- [ ] Approved encrypted device: works for an approved user, blocked for others.
