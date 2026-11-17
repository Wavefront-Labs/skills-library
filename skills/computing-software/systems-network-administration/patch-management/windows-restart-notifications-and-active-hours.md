---
id: computing-software.systems-network-administration.patch-management.windows-restart-notifications-and-active-hours
name: windows-restart-notifications-and-active-hours
category: computing-software
field: systems-network-administration
product: patch-management
tags: [restart-notification, active-hours, install-deadline, reboot-management, windows-update-for-business, intune]
level: practitioner
status: docs-checked
description: "Get Windows endpoints to restart after updates without angering users: active hours, deadlines and grace, notification levels, engaged restart, and ConfigMgr restart settings."
sources:
  - https://learn.microsoft.com/en-us/windows/deployment/update/waas-restart
  - https://learn.microsoft.com/en-us/mem/intune/protect/windows-update-settings
  - https://learn.microsoft.com/en-us/mem/configmgr/core/clients/deploy/device-restart-notifications
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Windows restart notifications and active hours

## Windows Update for Business / Intune
| Setting | Purpose |
|---|---|
| Active hours (default 8 AM to 5 PM on PCs; maximum range 18 hours, 12 hours on Windows 10 1607 and Windows Server 2016) | no automatic restarts in this window |
| Deadline for quality updates (Intune: 2-30 days) + grace period (Intune: 0-7 days) | minimum days after the deadline until restarts occur automatically; with auto reboot before deadline set to No, the restart waits for deadline plus grace and can fall in active hours |
| Auto reboot before deadline (Intune; recommended Yes) | lets the device restart outside active hours before the deadline and grace period expire |
| Notification level (GP "Display options for update notifications": 0 default, 1 turn off most notifications but keep restart warnings, 2 turn off all including restart warnings) | user experience; keep restart warnings on |
| Engaged restart | legacy policies (transition, snooze, deadline); not applicable to Windows 11 |
Group Policy path: Computer Configuration → Administrative Templates → Windows Components →
Windows Update ("Turn off auto-restart for updates during active hours", "Display options for
update notifications", "No auto-restart with logged on users for scheduled automatic updates
installations"). Deadline policy names vary by Windows build, so check the policy list on your ADMX version.

## ConfigMgr (client settings → Computer Restart)
- "Specify the amount of time after the deadline before a device gets restarted (minutes)": default 90, maximum 20160 (two weeks); it must be shorter than the shortest maintenance window that applies to the device.
- "Specify the amount of time that a user is presented a final countdown notification before a device gets restarted (minutes)": default 15.
- "Specify the frequency of reminder notifications presented to the user, after the deadline, before a device gets restarted (minutes)".
- Maintenance windows on collections limit when Configuration Manager restarts devices.

## Servers
Never rely on user prompts: restart inside the maintenance window via orchestration
(ConfigMgr maintenance windows, Ansible, Azure Update Manager schedules), then verify. For servers Microsoft's restart guidance suggests Configure Automatic Updates option 7 (notify to install and notify to reboot) rather than relying on user prompts.

## Communicating
- Announce Patch Tuesday deadlines; show expected restart day in the self-service portal.
- Users on long-running workloads (render, analysis) belong in a separate ring with
  scheduled windows.

## Gotchas
- Grace period 0 means no extra days after the deadline before automatic restarts.
- Microsoft lists "updates may not be installed with Fast Startup" among known Windows Update issues; ask users to restart rather than shut down.
- Third-party "reboot blockers" (apps vetoing shutdown) delay compliance: report devices
  with pending reboot > N days.

## Verify
Pending-reboot report shows < 5% of devices pending beyond deadline+grace; helpdesk tickets
about surprise restarts stay low after changes.

## Checked

Checked 2026-10-27 against Microsoft Learn: Manage device restarts after updates (waas-restart), Intune Windows 10/11 update ring settings, and Configuration Manager Device restart notifications.
- Active hours default (8 AM to 5 PM) and maximum range (18 hours; 12 on Windows 10 1607 and Server 2016): confirmed.
- Notification level values 0, 1, 2; engaged restart policies are legacy and not applicable to Windows 11; Configure Automatic Updates option 7 for servers: confirmed.
- Intune deadline 2-30 days, grace period 0-7 days, auto reboot before deadline semantics: confirmed.
- ConfigMgr restart settings: current names, defaults (90 and 15 minutes) and maximum 20160 minutes: confirmed; older setting titles were replaced.
- Removed unconfirmed: the `RebootIfRequired` parameter, the "returning from leave" restart claim, the Group Policy folder name "Manage end user experience".
Method: documentation only; no commands were run.
