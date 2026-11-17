---
id: computing-software.cybersecurity-defensive.endpoint-security.macos-removable-media
name: macos-removable-media
category: computing-software
field: cybersecurity-defensive
product: endpoint-security
tags: [macos-removable-media, macos-device-control, mdm-media-restrictions, jamf-protect, defender-device-control-mac, device-control]
level: practitioner
status: draft
description: "Restrict removable media on macOS: Defender for Endpoint device control for Mac, MDM restrictions, read-only and encrypted-only USB, and auditing mounts."
sources: ["https://learn.microsoft.com/en-us/defender-endpoint/mac-device-control-overview", "https://support.apple.com/guide/deployment/restrictions-for-mac-dep0f7dd3d8/web", "https://learn.jamf.com/en-US/bundle/jamf-protect-documentation/page/Removable_Storage_Control.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# macOS removable media restriction

Apple's MDM restrictions for external media are limited and partly deprecated (`com.apple.systemuiserver`
media mount controls); use an endpoint agent for real control.

## Defender for Endpoint on macOS device control
- JSON policy (deployed via MDM `com.microsoft.wdav` configuration or Intune settings catalog) with groups (e.g. `removableMedia` by vendor ID/product ID/serial, `apple devices`, `portable devices`) and rules: allow/deny read, write, execute; audit.
- Example intent: deny write to all removable media except encrypted corporate USB keys (by serial), allow read.
- Check: `mdatp device-control policy` / `mdatp health --details device_control`.

## Jamf Protect / other agents
Removable Storage Control with modes: read-only, read/write, prevented; override for encrypted (APFS encrypted) devices only.

## Encrypted-only approach
Allow write only if the volume is APFS encrypted - users encrypt via Finder (right-click -> Encrypt) on
first use; reduces loss-of-data risk while keeping usability.

## Auditing
- Unified log: `log show --predicate 'subsystem == "com.apple.diskarbitration"'` for mounts.
- Agent events (Defender `DeviceEvents` RemovableStoragePolicyTriggered) to SIEM.

## Gotchas
- Policies must cover APFS, HFS+, exFAT/FAT32 and also SD cards and Thunderbolt drives.
- Users with admin rights may unload agents/profiles; ensure tamper protection and standard users.
- Network shares and AirDrop are separate exfil paths (AirDrop restrictions via MDM).

## Verify
- [ ] Write to an unapproved USB key denied on a test Mac; read works if intended.
- [ ] Events appear in SIEM with device serial.
