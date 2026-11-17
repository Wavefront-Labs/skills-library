---
id: computing-software.systems-network-administration.windows-server.windows-update-policy-for-servers
name: windows-update-policy-for-servers
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, windows-updates, servicing, windows-update-policy, wufb, configure-automatic-updates, au-options, no-auto-reboot, sconfig-updates, group-policy, maintenance-window]
level: practitioner
status: docs-checked
description: "Control how servers take updates by GPO: Configure Automatic Updates options, download-only vs scheduled install, no auto-restart, WSUS vs Microsoft Update source."
sources:
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-server-update-services/deploy/4-configure-group-policy-settings-for-automatic-updates
  - https://learn.microsoft.com/en-us/windows/deployment/update/waas-wu-settings
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Windows Update policy for servers

Servers should never reboot themselves at a random time. Control the client with GPO:
*Computer Configuration > Policies > Administrative Templates > Windows Components > Windows Update*

## Core settings
| Setting | Server value |
|---|---|
| Configure Automatic Updates | Enabled, "Auto download and notify for install" (your patch tool orchestrates), or auto download and schedule install for simple estates |
| Specify intranet Microsoft update service location | `http://wsus01:8530` (if using WSUS) + status server |
| Do not connect to any Windows Update Internet locations | Enabled when WSUS-only |
| No auto-restart with logged on users for scheduled automatic updates installations | Enabled |
| Enable client-side targeting | WSUS group name per wave (e.g. `Servers-Wave1`) |


## Verify
- [ ] A sample server shows the intended update settings and WSUS URL.
- [ ] No unplanned reboots (System log event 1074 reasons) in a month.

## Checked
2026-10-28: Confirmed on Learn pages 4-configure-group-policy-settings-for-automatic-updates and waas-wu-settings: setting names 'Specify intranet Microsoft update service location', 'Do not connect to any Windows Update Internet locations', 'No auto-restart with logged on users...', 'Enable client-side targeting', and the 'Auto download and notify' option; event 1074 is described on the shutdown pages. Removed: ADMX location note, AUOptions number mapping and registry path, maintenance-install row, Windows Update for Business remark, sconfig and CIM on-demand scan sections.
Method: documentation only; no commands were run.
