---
id: computing-software.cybersecurity-defensive.identity-access-management.endpoint-privilege-management
name: endpoint-privilege-management
category: computing-software
field: cybersecurity-defensive
product: identity-access-management
tags: [endpoint-privilege-management, epm, intune-epm, admin-rights-removal, elevation-rules, just-in-time-elevation, privileged-access]
level: practitioner
status: draft
description: "Remove standing local admin and handle elevation with EPM: Intune EPM or third-party rules (file hash, publisher), user-confirmed vs support-approved elevation, and audit."
sources: ["https://learn.microsoft.com/en-us/mem/intune/protect/epm-overview", "https://learn.microsoft.com/en-us/mem/intune/protect/epm-guidance-for-creating-rules", "https://www.cisecurity.org/controls/v8"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Endpoint privilege management

Removing local admin blocks a large share of malware and attacker tooling. EPM handles the remaining
legitimate elevation needs without giving the user admin.

## Intune EPM setup
1. Licence (Intune Suite/EPM add-on), create an **Elevation settings policy**: enable EPM, default elevation response for unmanaged files = deny / require support approval, reporting on.
2. **Elevation rules policy**: per app, identify by file hash and/or certificate (publisher) plus file name/path; elevation type:
   - Automatic (silent) for well-known installers/tools.
   - User confirmed (justification, optionally Windows authentication).
   - Support approved (user requests, admin approves in console).
3. Users right-click -> "Run with elevated access".
4. Child process behaviour: deny child process elevation for interpreters (cmd, PowerShell) launched from elevated apps unless needed.

## Rule hygiene
- Prefer publisher certificate + product name over path; hash rules break on updates, path rules can be hijacked if the folder is user-writable.
- Never create rules for cmd.exe, powershell.exe, mmc.exe, regedit.exe generically - that is admin rights by another name.
- Review EPM elevation reports monthly to convert repeated support approvals into rules.

## Third-party equivalents
BeyondTrust Privilege Management, CyberArk EPM, Admin By Request - same model: allow lists, approval workflow, audit.

## Gotchas
- Developer machines: provide a separate admin workflow or dev VMs rather than blanket elevation.
- Remove users from local Administrators via Intune account protection policy (local user group membership) or LAPS-managed admin only.

## Verify
- [ ] Local Administrators group contains only LAPS admin and the device-admin role.
- [ ] Elevation events reported; unmanaged elevation attempts reviewed.
