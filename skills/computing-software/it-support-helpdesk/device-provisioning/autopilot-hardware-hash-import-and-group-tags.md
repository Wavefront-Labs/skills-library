---
id: computing-software.it-support-helpdesk.device-provisioning.autopilot-hardware-hash-import-and-group-tags
name: autopilot-hardware-hash-import-and-group-tags
category: computing-software
field: it-support-helpdesk
product: device-provisioning
tags: [it-support-helpdesk, device-provisioning, autopilot-group-tag, autopilot, hardware-hash, get-windowsautopilotinfo, dynamic-groups, intune, autopilot-profile-assignment, autopilot-reseller-registration]
level: practitioner
status: draft
description: "Register devices for Windows Autopilot: collect hardware hashes, CSV format and import, group tags with matching dynamic group rules, OEM registration and fixing tags later."
sources:
  - "https://learn.microsoft.com/en-us/autopilot/add-devices"
  - "https://learn.microsoft.com/en-us/autopilot/enrollment-autopilot"
  - "https://www.powershellgallery.com/packages/Get-WindowsAutopilotInfo"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# autopilot-hardware-hash-import-and-group-tags

## Ways to register
1. **OEM/reseller** registers at purchase (best; ask your supplier, give them your tenant
   and preferred group tag).
2. **Hash upload** for existing devices:
```powershell
Install-Script -Name Get-WindowsAutopilotInfo -Force
Get-WindowsAutopilotInfo -OutputFile "$env:TEMP\ap.csv" -GroupTag SALES
# or straight into the tenant (prompts for admin sign-in):
Get-WindowsAutopilotInfo -Online -GroupTag SALES
```
   At OOBE: `Shift`+`F10` opens a command prompt; run PowerShell from there.
3. Intune automatic conversion of already-enrolled devices ("Convert all targeted devices
   to Autopilot" in the profile).

## CSV import
Intune > Devices > Windows > Enrollment > Devices (Windows Autopilot) > Import. Columns:
`Device Serial Number,Windows Product ID,Hardware Hash,Group Tag,Assigned User`. Keep files
to 500 rows; ANSI/UTF-8 without extra columns or quotes added by Excel.

## Group tags and dynamic groups
- All Autopilot devices: `(device.devicePhysicalIDs -any (_ -startsWith "[ZTDId]"))`
- By tag: `(device.devicePhysicalIds -any (_ -eq "[OrderID]:SALES"))`
Assign Autopilot profiles, ESP and apps to these groups. Dynamic membership can take
minutes to update; wait for the profile status to show Assigned before deploying.

## Fixing tags
Change the group tag on the Autopilot device record, then Sync; the device moves groups
and gets the right profile at next OOBE. Already-deployed devices need a reset to rerun.

## Gotchas
- Hashes captured after motherboard replacement differ; re-register after board swaps.
- Deleting the Intune device does not remove the Autopilot registration (and vice versa).
- Typos in tags silently leave devices out of every group.

## Verify
The device shows in the Autopilot list with the correct tag, profile status Assigned, and
OOBE shows the organisation's branded sign-in.
