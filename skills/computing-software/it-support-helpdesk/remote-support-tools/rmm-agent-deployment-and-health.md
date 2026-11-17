---
id: computing-software.it-support-helpdesk.remote-support-tools.rmm-agent-deployment-and-health
name: rmm-agent-deployment-and-health
category: computing-software
field: it-support-helpdesk
product: remote-support-tools
tags: [it-support-helpdesk, remote-support-tools, rmm-agent, rmm, ninjaone, datto-rmm, connectwise-automate, agent-health, unattended-access]
level: practitioner
status: draft
description: "Deploy RMM agents at scale with site tokens, keep them out of golden images, and diagnose offline, duplicate or stale agents from the endpoint side."
sources:
  - "https://www.cisa.gov/news-events/cybersecurity-advisories/aa23-025a"
  - "https://learn.microsoft.com/en-us/mem/intune/apps/apps-win32-app-management"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# rmm-agent-deployment-and-health

## Deployment
- Download the installer per client/site; most RMMs bake the org/site token into the
  installer or its filename. Do not rename it unless the vendor documents a parameter.
- Deploy with whatever already manages the fleet: Intune Win32 app (detection rule = agent
  service exists), GPO startup script, or ConfigMgr. Install silently as SYSTEM.
- macOS: the vendor PKG plus a PPPC/Full Disk Access and screen recording profile pushed
  by MDM before the agent, otherwise remote control shows a grey screen.
- Never leave an agent in a golden image or VM template: clones inherit the agent ID and
  show as one device flapping between hostnames. Install after sysprep, at first boot.

## Health checks on a device
| Check | How |
|---|---|
| Service running | `Get-Service` for the vendor service (NinjaOne `NinjaRMMAgent`, ConnectWise Automate `LTService`/`LTSvcMon`, Datto RMM `CagService`) |
| Outbound reachability | `Test-NetConnection <vendor host> -Port 443`; proxies and SSL inspection are the usual break |
| Clock | `w32tm /query /status`; large skew breaks TLS check-ins |
| AV/EDR | Agent folders excluded per vendor guidance and not quarantined |

## Console hygiene
- Alert on agents offline more than N days; most "offline" devices are retired kit.
- Reconcile weekly against Intune/Entra and the asset register; remove agents for
  disposed devices so licences and the attack surface shrink.
- Duplicate hostnames with different agent IDs usually mean a reinstall; delete the stale
  one after confirming its last check-in.

## Gotchas
- Uninstalling often needs a console-issued uninstall or a password/tamper token.
- Agents installed by a user from a phished link are an attacker's RMM; an unknown
  tenant/site ID is an incident (see detecting-unapproved-remote-access-tools).

## Verify
Device shows online with current check-in, correct site and hostname, and a test script
(e.g. `hostname`) returns from the console.
