---
id: computing-software.it-support-helpdesk.intune-mdm.expedited-quality-updates
name: expedited-quality-updates
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, expedite-quality-update, quality-updates, zero-day, emergency-patching, update-health-tools, intune]
level: practitioner
status: docs-checked
description: "Push an urgent Windows quality update with expedite policies: prerequisites, licensing, Update Health Tools, readiness test, Graph deployment settings and how to stop one."
sources:
  - "https://learn.microsoft.com/en-us/mem/intune/protect/windows-10-expedite-updates"
  - "https://learn.microsoft.com/en-us/windows/deployment/update/deployment-service-expedited-updates"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# expedited-quality-updates

Expedite accelerates installation of a specific security or critical quality update when standard
timelines are not acceptable. You can use an expedite policy without creating a Windows quality
update policy. Devices with no quality update policy still receive monthly updates via update
rings and Windows Update client policies. Restart settings, deadlines, notifications and
deferrals stay in the update ring and Windows Update client policies.

## Prerequisites (Intune quality updates page)
- Licences: Microsoft Intune Plan 1 and a Windows licence that includes the Autopatch
  entitlement.
- Editions: Pro, Pro Education, Enterprise, Education. Enterprise LTSC is not supported (use
  update rings).
- Devices managed by Intune, and Entra joined or hybrid joined.
- Telemetry on at minimum **Required**; allow Intune to use Windows diagnostic data for
  reporting.
- The Microsoft Account Sign-In Assistant service (`wlidsvc`) enabled and running.
- Reach Intune, Windows Update and Windows Autopatch endpoints. The Graph article lists:
  `*.prod.do.dsp.mp.microsoft.com`, `*.windowsupdate.com`, `*.dl.delivery.mp.microsoft.com`,
  `*.update.microsoft.com`, `*.delivery.mp.microsoft.com`,
  `tsfe.trafficshaping.dsp.mp.microsoft.com`, `devicelistenerprod.microsoft.com`,
  `login.windows.net` and `payloadprod*.blob.core.windows.net`.
- Update Health Tools (installed from KB4023057). Not required on Windows 11 24H2 and later.
  Check for the folder `%ProgramFiles%\Microsoft Update Health Tools` or the Add or remove
  programs entry. Logs are `.etl` files in `%ProgramFiles%\Microsoft Update Health
  Tools\Logs` (open with PerfView).
- Roles: Policy and Profile manager, or a custom role with Device configurations Assign, Create,
  Delete, View Reports, Update and Read plus device visibility. Reports: Endpoint Security
  Manager, Read Only Operator, Help Desk Operator or a role with Managed devices/View Reports.
- Public cloud and GCC are supported.

## Programmatic control (Microsoft Graph, beta)
- Find expeditable updates: `GET /beta/admin/windows/updates/catalog/entries` filtered on
  `qualityUpdateCatalogEntry/isExpeditable eq true`, newest first. The returned `id` is the
  catalog ID. Needs `WindowsUpdates.ReadWrite.All` and at least `Device.Read.All`.
- Create a deployment: `POST /beta/admin/windows/updates/deployments` with
  `settings.expedite.isExpedited: true` and optionally
  `settings.userExperience.daysUntilForcedReboot` (Microsoft's example uses 2).
- Add devices to the returned audience with `.../deploymentAudiences/{id}/updateAudience`
  (`addMembers` with `#microsoft.graph.windowsUpdates.azureADDevice`, using the Entra device
  ID, not the object ID). While the deployment exists and the device is in the audience, the
  update is expedited.
- **Stop it**: `DELETE` the deployment; content not yet delivered is no longer offered. Create a
  new approval to resume.
- **Readiness test**: set `expedite.isReadinessTest: true` and add devices; results appear in the
  Windows Update for Business reports workbook > Quality updates > Expedite status > Readiness.

## Hotpatch
On supported devices, hotpatch can be turned on through quality update policies so qualifying
security updates install without an immediate restart (see hotpatch-and-pausing-update-rings).

## Checked
Date: 2026-11-08. Read in full: Intune "Manage Windows quality updates" (updated 2026-04-09; it replaced the older expedite profile page) and "Programmatic controls for expedited Windows quality updates" (updated 2025-03-31). The Windows Update settings page was dropped as a source. Removed as unconfirmed: the profile fields (restart days 0-2 as a UI range, the "if device OS version is less than" wording), the reporting state names, the WSUS/ConfigMgr scan source rows, the optional-update and low-disk gotchas, and the offline-device behaviour.
Method: documentation only; no commands were run.
