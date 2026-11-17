---
id: computing-software.it-support-helpdesk.remote-support-tools.offline-rmm-agent-triage
name: offline-rmm-agent-triage
category: computing-software
field: it-support-helpdesk
product: remote-support-tools
tags: [it-support-helpdesk, remote-support-tools, offline-agent, rmm-agent, agent-health, stale-devices, rmm, device-inventory]
level: practitioner
status: draft
description: "Triage devices whose RMM agent shows offline: separate powered-off from broken agents, cross-check Intune/AD/EDR last-seen, repair or reinstall, and retire stale records."
sources:
  - "https://rmm.datto.com/help/en/Content/2SETUP/Devices/AgentTroubleshooting.htm"
  - "https://learn.microsoft.com/en-us/mem/intune/remote-actions/devices-wipe"
  - "https://www.cisa.gov/resources-tools/resources/cisa-insights-remote-monitoring-and-management-software"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# offline-rmm-agent-triage

An offline agent means no patching, no monitoring and no remote access. The list grows
quietly; work it weekly.

## Sort the offline list
Export devices offline > 7 days with last-seen time, last user, site. For each, compare
other telemetry:
| Signal | Where |
|---|---|
| Intune last check-in | Intune device record |
| Entra/AD activity | Entra device "Activity", AD `lastLogonTimestamp` |
| EDR last seen | Defender/CrowdStrike/SentinelOne console |
| Network | DHCP leases, VPN logs, switch port |

- All signals old -> device is off, lost, or retired: contact the user/asset owner.
- Other tools current but RMM offline -> broken agent: repair.

## Repair a broken agent
1. Remote in via another channel (Intune Remote Help, RDP, EDR live response) or ask the
   user.
2. Check the agent service: `Get-Service *agent*` (names vary: `CagService` for Datto,
   `NinjaRMMAgent`, `LTService` for Automate). Start it; set Startup = Automatic; check
   Event Viewer > Application for crashes.
3. Connectivity: `Test-NetConnection <rmm-endpoint> -Port 443`; proxy or TLS inspection
   breaking agent certificate pinning; firewall rules after a network change.
4. Clock skew breaks TLS: `w32tm /query /status`.
5. Disk full or AV quarantined the agent binaries: check AV logs, add the vendor's
   recommended exclusions.
6. Reinstall: deploy the site-specific installer via Intune/GPO or EDR "run script";
   ensure it matches the existing device record (most RMMs match by device ID/MAC) to
   avoid duplicates.

## Retire stale records
- Not seen in 90 days and confirmed disposed/lost: delete from RMM (frees licence),
  update the asset record, and check the device isn't still in Intune/AD.
- Lost/stolen: security process (remote wipe via MDM, disable accounts), not just delete.

## Prevent
- Deploy the agent via two channels (Intune Win32 app required + RMM self-heal).
- Alert on "agent offline > 3 days while Intune check-in is current" via a report join.
- Include agent health in the standard build QA and in device handover.

## Gotchas
- Duplicates: reimaged devices register as new; the old record stays offline forever.
- Laptops in drawers aren't broken agents; they need a patch catch-up on return.

## Verify
Offline count trend falls, each remaining offline device has a reason (off, lost, retired,
under repair), and repaired agents report and pass a test job.
