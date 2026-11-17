---
id: computing-software.it-support-helpdesk.device-provisioning.device-naming-conventions
name: device-naming-conventions
category: computing-software
field: it-support-helpdesk
product: device-provisioning
tags: [it-support-helpdesk, device-provisioning, standard-build, device-naming, netbios-name, autopilot-naming-template, rename-computer, hostname, asset-tag]
level: intro
status: draft
description: "Design and apply device names that work everywhere: 15-character NetBIOS limit, no PII, Autopilot %SERIAL%/%RAND% templates, Intune rename, macOS and mobile naming."
sources:
  - "https://learn.microsoft.com/en-us/troubleshoot/windows-server/active-directory/naming-conventions-for-computer-domain-site-ou"
  - "https://learn.microsoft.com/en-us/autopilot/profiles"
  - "https://learn.microsoft.com/en-us/intune/intune-service/remote-actions/device-rename"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# device-naming-conventions

Goal: a name that tells support what the device is, is unique forever, and
doesn't break AD, DNS or privacy rules.

## Constraints
- **15 characters max** for Windows (NetBIOS); letters, digits, hyphen; not
  all digits; no spaces or `\ / : * ? " < > |`.
- Unique across AD/Entra/Intune/CMDB — duplicates break trust relationships
  and confuse remote tools.
- **No personal data** (user names) — devices change hands; names leak in
  network broadcasts, logs, Wi-Fi.

## Good patterns
`<ORG><TYPE>-<ID>`:
- `CTLT-5CG1234XYZ` (org, laptop, serial) — serial is unique and on the
  sticker; trim to fit 15 chars.
- `CTDT-012345` (desktop, asset tag).
- Kiosks/shared: `CTKS-LDN-RECEP1` only if location naming is stable.
Type codes (LT laptop, DT desktop, VM, KS kiosk, SV server) help triage at a
glance.

## Applying names
- **Autopilot profile**: "Apply device name template" e.g. `CTLT-%SERIAL%`
  (truncated to 15) or `CTLT-%RAND:6%`. Entra-joined only; hybrid-join uses
  the domain join profile prefix.
- **Intune remote action** "Rename device" (Windows Entra-joined; reboot
  needed).
- Script: `Rename-Computer -NewName CTLT-012345 -Restart` (domain:
  `-DomainCredential`).
- macOS: `sudo scutil --set ComputerName/LocalHostName/HostName` or Jamf
  "Enforce computer name"; iOS: MDM device name setting (supervised).

## Gotchas
- Renaming a domain-joined PC without domain credentials breaks its AD
  account.
- Serial numbers from VMs and some white-box PCs are blank or
  "To be filled by O.E.M." → `%SERIAL%` template produces junk — use
  `%RAND%`.
- Changing the convention mid-life: rename on refresh, not all at once
  (breaks monitoring, licences tied to hostname).

## Verify
New devices appear in Intune/Entra/CMDB with names matching the regex for
the convention (e.g. `^CT(LT|DT|KS)-[A-Z0-9]{1,10}$`) and no duplicates in a
report.
