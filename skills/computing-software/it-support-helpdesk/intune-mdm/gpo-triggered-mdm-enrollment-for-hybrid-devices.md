---
id: computing-software.it-support-helpdesk.intune-mdm.gpo-triggered-mdm-enrollment-for-hybrid-devices
name: gpo-triggered-mdm-enrollment-for-hybrid-devices
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, gpo-mdm-enrollment, hybrid-entra-join, group-policy, enrollment-scheduled-task, device-credential, user-credential, windows-enrollment]
level: advanced
status: docs-checked
description: "Enroll hybrid Entra joined Windows PCs in Intune with the auto MDM enrollment GPO: user vs device credential, the scheduled task, event IDs, and common failures."
sources:
  - "https://learn.microsoft.com/en-us/windows/client-management/enroll-a-windows-10-device-automatically-using-group-policy"
  - "https://learn.microsoft.com/en-us/troubleshoot/mem/intune/device-enrollment/troubleshoot-windows-auto-enrollment"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# gpo-triggered-mdm-enrollment-for-hybrid-devices

Domain-joined PCs that are hybrid Microsoft Entra joined enroll in Intune with a
Group Policy: **Computer Configuration > Administrative Templates > Windows
Components > MDM > Enable automatic MDM enrollment using default Microsoft Entra
credentials**. Enrollment starts in the background after sign-in with an Entra
account, with no further user action (the user is prompted if MFA is required;
Conditional Access can avoid that).

## Requirements
- Supported Windows, an MDM service configured, AD integrated with Entra through
  Entra Connect, and the service connection point (SCP) configured (or Entra
  hybrid join targeted deployment where no SCP is published).
- The device must not already be enrolled through the classic Intune agent
  (fails with 0x80180026) or another MDM.
- If the policy is missing, install the latest administrative templates for your
  Windows version and copy PolicyDefinitions to the SYSVOL central store; wait
  for DFSR replication.
- Deploy via a GPO linked and security-group filtered to a group of PCs.

## Choose the credential type
| Option | Use |
|---|---|
| User Credential | Default. Intune's subscription is user centric; also supported for Azure Virtual Desktop personal host pools |
| Device Credential (Windows 10 1903+) | Only for Intune in co-management scenarios or AVD multi-session host pools |
Older releases default to User Credential.

## What happens
When Group Policy refreshes, a scheduled task is created under Task Scheduler
Library > Microsoft > Windows > EnterpriseMgmt named "Schedule created by
enrollment client for automatically enrolling in MDM from Microsoft Entra ID".
It runs every 5 minutes for one day and uses the user's existing Entra
information to enroll.

## Verify the configuration first
- User has a valid Intune licence.
- Entra > Mobility (MDM and MAM): MDM user scope covers the users (the Learn
  guide says All), MAM user scope is None (otherwise it takes precedence), and
  the MDM discovery URL is
  https://enrollment.manage.microsoft.com/enrollmentserver/discovery.svc. If both
  Microsoft Intune and Microsoft Intune Enrollment appear, configure
  auto-enrollment under Microsoft Intune.
- Windows 10 1709 or later, hybrid joined. `dsregcmd /status` shows
  `AzureAdJoined: YES`, `DomainJoined: YES`, and under SSO state `AzureAdPrt: YES`.
- Entra device settings: Users may join devices to Microsoft Entra ID is All, and
  the user is under the maximum devices per user quota.
- Intune enrollment restrictions allow Windows enrollment.

## Troubleshooting by event
Event Viewer > Applications and Services Logs > Microsoft > Windows >
DeviceManagement-Enterprise-Diagnostic-Provider > Admin:
| Event | Meaning |
|---|---|
| 75 | Auto MDM Enroll: Succeeded |
| 76 | Auto MDM Enroll: Failed, with a code such as 0x8018002b; see Troubleshoot Windows device enrollment problems |
| neither 75 nor 76 | Enrollment was not triggered: check the task |

The task: in Task Scheduler > Operational, Event ID 107 means the task was
triggered and 102 that it completed (logged whether or not enrollment
succeeded). If it will not start:
- Already enrolled in another MDM: Event 7016 with error code 2149056522;
  unenroll the device from that MDM.
- Group Policy problem: `gpupdate /force`, then investigate AD.
Error 0x80180026 (MENROLL_E_DEVICE_MANAGEMENT_BLOCKED) is a classic-agent
conflict and can also come from the Disable MDM Enrollment policy.

## Verify enrollment
Settings > Accounts > Access work or school > select the domain account > Info
shows MDM enrollment information; no Info button suggests failure, so check the
task's Last Run Result and History in Task Scheduler.

## Gotchas
- With the same policy in Group Policy and MDM, Group Policy wins (since
  Windows 10 1709); 1803 added a setting to switch precedence to MDM.
- GPEdit does not show organisation-set policies; use it only to set values.

## Checked
2026-11-08. Confirmed against the Microsoft Learn pages Enroll a Windows device
automatically using Group Policy (last updated 2025-08-04) and Troubleshooting
Windows 10 Group Policy-based auto-enrollment in Intune (2026-03-30): policy
path, requirements, credential types, task name and schedule, verification
list, event IDs 75, 76, 102, 107, 7016, 0x80180026. Removed as unconfirmed: the
claim that 0x8018002b means a non-routable UPN, the 0x80180026 description as
a legacy PC agent only, the proxy-timeout row, the PRT-timing and stale
Enrollments registry gotchas, primary-user effect, and the hybrid join how-to
source.
Method: documentation only; no commands were run.
