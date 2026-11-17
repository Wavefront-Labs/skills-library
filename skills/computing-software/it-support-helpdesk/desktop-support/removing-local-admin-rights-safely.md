---
id: computing-software.it-support-helpdesk.desktop-support.removing-local-admin-rights-safely
name: removing-local-admin-rights-safely
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, workstation-security, least-privilege-workstation, local-admin-removal, standard-user, elevation-requests, endpoint-privilege-management, admin-by-request, comptia-a-plus]
level: practitioner
status: draft
description: "Remove local admin rights without flooding the desk: inventory, learn what admin is used for, self-service installs and elevation rules, then remove in waves."
sources:
  - "https://learn.microsoft.com/en-us/intune/intune-service/protect/epm-overview"
  - "https://learn.microsoft.com/en-us/windows/security/application-security/application-control/user-account-control/"
  - "https://www.cisa.gov/topics/cybersecurity-best-practices"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# removing-local-admin-rights-safely

Goal: users run as standard users (least privilege, a top control against
ransomware and malware), and the ticket volume doesn't spike when you make
the change.

## 1. Inventory
- Who's in local Administrators: Intune/Defender device inventory, script
  report (`Get-LocalGroupMember Administrators`) via remediation script or
  RMM.
- Entra-joined devices where users became admin at join (Autopilot profile
  "user account type: administrator").

## 2. Learn what admin is used for
For 2–4 weeks before removal: EPM in audit/report mode (Intune Endpoint
Privilege Management elevation reports) or third-party tools show which
executables requested elevation. Typical: installing apps, printer drivers,
VPN/network changes, developer tools, time zone changes.

## 3. Provide alternatives
- **Self-service catalogue** (Company Portal / Software Center) for the apps
  people installed themselves.
- Pre-approved **elevation rules** (Intune EPM: automatic or user-confirmed
  elevation for specific signed executables; supported elevation for
  everything else with justification and approval).
- Printer drivers pre-staged (see Point and Print skill); time zone
  auto-set allowed for standard users.
- Developers: dedicated policy (dev tools in catalogue, WSL, scoped
  elevation), not blanket admin.

## 4. Remove in waves
Pilot (IT) → departments with simple app needs → specialist teams last.
Use Intune **Local user group membership** (Account protection) policy to
set Administrators membership precisely; communicate the change, how to get
apps, and how to request elevation.

## 5. After
Track elevation requests and new-app requests; add frequent ones to the
catalogue/rules. Keep an approved exception list with expiry for genuine
needs.

## Gotchas
- Removing admin without the catalogue in place = flood of tickets and
  executive exceptions.
- Shared "IT admin" local passwords defeat the purpose — Windows LAPS.
- Some legacy apps need writable folders, not admin (see compatibility
  skill).

## Verify
Local Administrators on sampled devices = only approved accounts; elevation
requests per week falling after the first month; no rise in unresolved
install tickets.
