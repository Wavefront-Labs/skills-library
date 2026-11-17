---
id: computing-software.it-support-helpdesk.intune-mdm.hotpatch-and-pausing-update-rings
name: hotpatch-and-pausing-update-rings
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, hotpatch, update-ring-pause, windows-update-for-business, quality-updates, update-rollback]
level: practitioner
status: docs-checked
description: "Enable Windows hotpatch updates through Intune, and pause, extend or uninstall updates from an update ring when a bad quality or feature update hits."
sources:
  - "https://learn.microsoft.com/en-us/windows/deployment/windows-autopatch/manage/windows-autopatch-hotpatch-updates"
  - "https://learn.microsoft.com/en-us/intune/device-updates/windows/manage-update-rings"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# hotpatch-and-pausing-update-rings

## Hotpatch
Hotpatch updates are monthly security updates that take effect without a restart.
They are an extension of Windows Update and need Windows Autopatch to create and
deploy them to devices enrolled in the Autopatch quality update policy. Your
existing update ring configuration is honoured alongside.

Cycle: a **baseline** (standard cumulative update, restart required) each
quarter, in January, April, July and October; the other eight months are
hotpatch months with no restart. Occasionally an out-of-cycle baseline
happens for security reasons and the planned cadence does not change. In a
hotpatch month a device not on the latest baseline gets both the baseline
(restart) and the hotpatch. Upgrading a device to a new Windows version in a
baseline month keeps it on the hotpatch cycle; in a hotpatch month it falls back
to standard updates until the next baseline.

Prerequisites:
- Licence: Windows 11 Enterprise E3 or E5, Microsoft 365 F3, Windows 11 Education
  A3 or A5, Microsoft 365 Business Premium, or Windows 365 Enterprise.
- Windows 11 24H2 or later, on the latest baseline.
- Virtualization-based security (VBS) running (CSP VirtualizationBasedTechnology
  can enable it). Autopatch raises the alert "Hotpatch - VBS not running".
- Arm64 only: disable CHPE (DisableCHPE system policy CSP, or DWORD
  HotPatchRestrictions=1 under
  HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management,
  then restart). Beware 32-bit x86 apps such as 32-bit COM add-ins.
- Ineligible devices simply get the normal latest cumulative update (restart
  required) with their ring settings unchanged.

Enable in Intune: Devices > Manage updates > Windows updates > Quality updates >
Create > Windows quality update policy; in Settings set "When available, apply
without restarting the device (Hotpatch)" to Allow; assign devices. Deferral and
active hours still apply. The Hotpatch quality update report shows per-policy
status.

Troubleshooting: confirm baseline and eligibility, then System information shows
Virtualization-based security = Running; on the device Settings > Windows Update
> Advanced options > Configured update policies lists "Enable hotpatching when
available"; Event Viewer search `AllowRebootlessUpdates` = 1 means enrolled.
An inbox monitor logs hotpatch errors to the Application log and installs the
standard cumulative update after a critical error.

Rollback: no automatic rollback; you can uninstall a hotpatch (quick, but needs a
restart) and install the LCU.

## Pausing an update ring
Devices > Manage updates > Windows updates > Update rings > select the ring.
- **Pause** feature and/or quality updates for up to 35 days from the pause;
  then the pause expires and the device scans. Resume then pause again resets to
  35 days. Overview shows days remaining.
- **Extend** resets the pause for both update types to 35 days.
- **Resume** restores updates for the chosen type.
- Devices learn of a pause at their next check-in, so a scheduled update may
  install first; a device powered off at the time may install on start-up.
- Delete removes the ring's settings from Intune but does not change settings
  already on devices.
Pause the broad ring when the pilot ring finds a problem; leave pilot running to
test the fix.

## Uninstalling an update (rollback)
Ring > **Uninstall**, choose Feature or Quality (the latest installed update of
that type), for an active or paused ring.
- Intune sends it immediately, ignoring maintenance schedules; a needed restart
  happens with no option to delay.
- It also pauses that update type on the ring. When the pause elapses devices
  reinstall the update if still applicable.
- Only for the servicing channel the device is on, and the device must have the
  latest update installed.
- Feature update rollback is limited by the ring setting Set feature update
  uninstall period (2 to 60 days); past it the bits are gone. It does not work if
  the feature update was applied with an enablement package.
- A rolled-back quality update still shows in Update History.
- Intune does not manage users uninstalling updates themselves.
To keep a removed feature update from returning, pin a version with a feature
update policy.

## Verify
Hotpatch devices install in non-baseline months without restarting; after a
pause and uninstall, affected devices report the previous build.

## Checked
2026-11-08. Confirmed against the Microsoft Learn pages Hotpatch updates (last
updated 2026-06-02) and Manage Windows Update ring policies (2026-04-09):
release cycle, prerequisites, enable steps, rollback, troubleshooting steps,
pause, extend, resume, uninstall rules and the 2 to 60 day period. Removed or
corrected: the claim that uninstall requires a pause first (the page says an
active or paused ring; uninstall pauses it), the 10-day default uninstall
period, the Arm64 x64 wording, and the WinRE and wusa single-device steps.
Method: documentation only; no commands were run.
