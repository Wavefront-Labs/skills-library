---
id: computing-software.it-support-helpdesk.troubleshooting-methodology.slow-boot-and-logon-analysis
name: slow-boot-and-logon-analysis
category: computing-software
field: it-support-helpdesk
product: troubleshooting-methodology
tags: [it-support-helpdesk, troubleshooting-methodology, slow-logon, slow-boot, group-policy, startup-apps, diagnostics-performance, logon-scripts, startup-programs]
level: practitioner
status: draft
description: "Find what makes boot and logon slow: Diagnostics-Performance and Group Policy event timings, startup impact, logon scripts and drive maps, profile size, then a boot trace."
sources:
  - "https://learn.microsoft.com/en-us/troubleshoot/windows-server/group-policy/applying-group-policy-troubleshooting-guidance"
  - "https://learn.microsoft.com/en-us/sysinternals/downloads/autoruns"
  - "https://learn.microsoft.com/en-us/windows-hardware/test/wpt/windows-performance-recorder"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# slow-boot-and-logon-analysis

## Measure, do not guess
- Boot: Event Viewer > Applications and Services > Microsoft > Windows >
  Diagnostics-Performance > Operational. Event 100 gives BootTime (ms) and MainPathBootTime;
  events 101-110 name slow apps, drivers and services.
- Group Policy: Microsoft-Windows-GroupPolicy/Operational. Event 8001 = user logon policy
  processing time; 8000 = computer startup processing; 4016/5016 pairs show each client-side
  extension's duration (folder redirection, drive maps, scripts).
- Logon to desktop: Task Manager > Startup apps shows "Startup impact"; Autoruns (Sysinternals)
  shows everything that starts, including scheduled tasks and services.

## Usual causes
| Cause | Sign |
|---|---|
| Drive map or script to an unreachable server | GP extension takes 30+ s; times out off-network |
| Folder redirection / roaming profile copy | Large profile, slow network, events in Folder Redirection log |
| "Always wait for the network at computer startup and logon" policy | Sync foreground processing on every logon |
| Heavy startup apps | High Startup impact, many tray apps |
| Security agents and updates | Diagnostics-Performance names the service/driver |
| Fast Startup off with slow disk | Long BootTime on HDDs; replace with SSD |

## Fix
- Remove dead drive maps and scripts; use item-level targeting; move logon scripts to
  Intune/async.
- Disable or delay non-essential startup apps (Intune/GPO for managed ones).
- Use OneDrive KFM instead of roaming profiles and redirection where possible.

## Go deeper
If events do not explain it, capture a boot trace (see
windows-performance-recorder-traces) and look at the Boot Phases and Logon regions.

## Gotchas
- First logon on a new device is always slow (profile creation, app installs); measure
  the second.
- Laptops off-VPN fail differently; test both locations.

## Verify
Event 100 BootTime and GP 8001 times drop to target (e.g. under 60 s boot, under 30 s
policy) across three consecutive logons.
