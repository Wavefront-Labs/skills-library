---
id: computing-software.it-support-helpdesk.intune-mdm.windows-safeguard-holds
name: windows-safeguard-holds
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, safeguard-hold, feature-update, windows-release-health, compatibility-hold, feature-update-policy, windows-update-reports]
level: practitioner
status: docs-checked
description: "Explain and manage Windows safeguard holds: finding hold IDs in reports and the registry, Windows release health, opt-out for validation only, and outdated holds."
sources:
  - "https://learn.microsoft.com/en-us/windows/deployment/update/safeguard-holds"
  - "https://learn.microsoft.com/en-us/windows/deployment/update/safeguard-opt-out"
  - "https://learn.microsoft.com/en-us/intune/device-updates/windows/monitor-compatibility"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# windows-safeguard-holds

Microsoft applies a safeguard hold to the Windows Update service when it finds an
issue that could make a feature update fail or roll back (or cause data loss,
loss of connectivity or key functionality) and no workaround exists yet. Held
devices are not offered the new OS version until a fix is verified, then the
hold is released. Holds only affect devices updating through Windows Update;
media installs and WSUS are not blocked, so watch known issues yourself there.
Autopatch-managed devices also benefit from holds.

## Find out if a device is held
- Windows Update for Business reports list active safeguard holds, each
  identified by an 8-digit ID.
- Look the ID up on the Windows release health dashboard, Known issues page for
  the release, which describes the issue.
- The Intune Windows update compatibility reports show safeguard entries as a
  placeholder for apps or drivers carrying the safeguard tag, not as installed
  software.
- On a device using Windows Update (not Windows Update client policies),
  Settings > Windows Update says an update is on its way but not ready for the
  device, with no download option.
- Manual check, registry
  `HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Appraiser\GWX`
  value GStatus: 2 = no hold, 0 = hold in effect. For the ID, open
  `...\AppCompatFlags\TargetVersionUpgradeExperienceIndicators\<version key>`
  (for example GE24H2) and read GatedBlockId and GatedBlockReason alongside
  GStatus.

## What to do
1. Do not manually update; wait for the hold to be released. Microsoft's own
   advice is not to attempt a manual update until the issue is resolved.
2. Opt out only to validate, in a test environment, after reading the report and
   release health: MDM CSP `Update/DisableWUfBSafeguards`, or the Group Policy
   Disable safeguards for Feature Updates (Windows 11; Windows 10 1809+ with the
   October 2020 security update). The opt-out is temporary: protection returns
   after the update completes. It does not guarantee the update succeeds and will
   likely give a bad experience on affected devices. Alternatively validate
   upcoming versions through the Release Preview channel of the Windows Insider
   Program for Business.
3. Do not opt out the whole estate to hit a target date.

## Outdated holds
A hold can stay on a device after the issue is fixed when the mechanism that
refreshes it is blocked, most commonly by SSL inspection on endpoints such as
adl.windows.com (compatibility database updates), settings-win.data.microsoft.com
and settings.data.microsoft.com. Check those are not intercepted.

## Verify
Each held device has its hold ID recorded with the release health description
and a decision (wait, opt out for test, other); the report shows holds clearing.

## Checked
2026-11-08. Confirmed against the Microsoft Learn pages Safeguard holds (last
updated 2025-08-15), Opt out of safeguard holds (2026-01-17) and the Windows
update compatibility reports page (safeguard entries). Removed as unconfirmed:
the claim that the Intune feature update report shows a Safeguard hold state,
the hardware-requirements and ISO-upgrade gotchas, the OEM driver update
advice, and the examples of user symptoms.
Method: documentation only; no commands were run.
