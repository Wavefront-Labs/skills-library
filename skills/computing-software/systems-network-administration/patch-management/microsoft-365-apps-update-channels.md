---
id: computing-software.systems-network-administration.patch-management.microsoft-365-apps-update-channels
name: microsoft-365-apps-update-channels
category: computing-software
field: systems-network-administration
product: patch-management
tags: [microsoft-365-apps-updates, update-channel, third-party-patching, click-to-run, intune, configmgr]
level: practitioner
status: docs-checked
description: "Manage Microsoft 365 Apps (Click-to-Run) updates: choosing update channels, deadlines, Intune, ConfigMgr and Group Policy control, and checking versions."
sources:
  - https://learn.microsoft.com/en-us/microsoft-365-apps/updates/overview-update-channels
  - https://learn.microsoft.com/en-us/microsoft-365-apps/updates/configure-update-settings-microsoft-365-apps
  - https://learn.microsoft.com/en-us/microsoft-365-apps/updates/change-update-channels
  - https://learn.microsoft.com/en-us/microsoft-365-apps/updates/manage-microsoft-365-apps-updates-configuration-manager
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Microsoft 365 Apps update channels

Office Click-to-Run updates are **not** Windows updates; they use their own update channels.
Update channels deliver security and non-security updates every month.

## Channels
| Channel | Feature updates | Typical use |
|---|---|---|
| Current Channel | monthly | default for most users |
| Monthly Enterprise Channel | monthly, on the second Tuesday, predictable | managed enterprises |
| Semi-Annual Enterprise Channel | January and July until June 2026; from July 2026 monthly, on the same basis as Monthly Enterprise Channel | see Microsoft's channel unification notice before choosing it |
| Current Channel (Preview), Beta Channel | early (Microsoft 365 Insider program) | pilot/IT |

Pilot ring on preview channels, broad ring on Monthly Enterprise or Current.

## Control planes (pick one, conflicts are the usual problem)
- **Intune**: the ADMX-ingested Administrative Template for Office (the same settings as Group Policy).
- **Group Policy** (the Administrative Template for Office): the Updates settings include Update Channel, Update Path (where to look for updates), Target Version and Update Deadline.
- **ConfigMgr**: Software Updates client setting "Enable management of the Office 365 Client Agent"; Office updates are then deployed through Configuration Manager software updates.
Use one control plane per device; moving to a channel with an older build is not supported when Configuration Manager manages updates.

## Check
Compare installed versions from your inventory tool against Microsoft's update history page for the channel each device is assigned.

## Gotchas
- Set an **update deadline** (the Update Deadline setting) so updates are applied by a set date.
- Moving to a channel with an older build removes features that exist only in the newer version.

## Verify
Version report shows ≥ 95% on a supported build of the assigned channel within the
deadline; no devices on unsupported builds (check Microsoft's "update history" table).

## Checked
Date: 2026-10-27. Documentation checked: Microsoft Learn "Overview of update channels for Microsoft 365 Apps" (channels, Monthly Enterprise Channel on the second Tuesday, Semi-Annual Enterprise Channel January and July with the July 2026 change to monthly updates, Insider channels Beta and Current Channel (Preview)), "Configure update settings" (Update Path, Target Version, Update Deadline, Administrative Template in Intune), "Change update channels" (older-build behaviour, Configuration Manager restriction) and "Manage updates with Configuration Manager" (Office 365 Client Agent client setting). Removed the Cloud Update claims, the OfficeC2RClient command, the registry query and CDN GUID table, the Preview Semi-Annual channel and the VDI line, none of which the pages confirm.

Method: documentation only; no commands were run.
