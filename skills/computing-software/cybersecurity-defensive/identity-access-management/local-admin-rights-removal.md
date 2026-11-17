---
id: computing-software.cybersecurity-defensive.identity-access-management.local-admin-rights-removal
name: local-admin-rights-removal
category: computing-software
field: cybersecurity-defensive
product: identity-access-management
tags: [pam, local-admin-removal, least-privilege, intune-account-protection, restricted-groups, elevation-requests]
level: practitioner
status: draft
description: "Remove standing local admin rights from users: discovery of who has them, Intune/GPO enforcement, handling elevation needs with EPM or request workflows, and measuring exceptions."
sources: ["https://learn.microsoft.com/en-us/mem/intune/protect/endpoint-security-account-protection-policy", "https://learn.microsoft.com/en-us/mem/intune/protect/epm-overview", "https://www.cisecurity.org/controls/account-management"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Removing local admin rights

Local admin lets malware disable security tools, dump credentials and persist. Removing it is one of
the highest-value endpoint controls (CIS Control 5.4: restrict admin privileges to dedicated accounts).

## Discover current state
- Intune: Devices > Monitor or a remediation script reporting `Get-LocalGroupMember Administrators`.
- EDR advanced hunting / osquery: members of the local Administrators group per device.
- Group Policy: Restricted Groups or Group Policy Preferences that add domain groups to local admins.
Categorise: IT support accounts (keep via LAPS or dedicated groups), developers, specific apps, everyone else.

## Enforce
- **Intune Account protection > Local user group membership** policy: action "Replace" for the
  Administrators group with only the built-in Administrator (LAPS-managed) and an IT admin group.
  "Add (Update)" only adds; "Replace" removes others.
- GPO: Restricted Groups or GPP Local Users and Groups with "Delete all member users/groups".
- macOS: demote users via MDM (Jamf/Intune scripts), use privilege-on-demand tools (e.g. SAP Privileges
  app with logging) if needed.

## Handle real needs
- **Endpoint Privilege Management** (Intune EPM, BeyondTrust, CyberArk EPM, Admin By Request):
  elevation rules for specific signed installers/tools (automatic), user-confirmed elevation with
  justification, or support-approved elevation; all logged.
- Self-service software via Company Portal removes most install requests.
- Developers: dev VMs/containers, package managers that install per user, or EPM rules for toolchains.

## Rollout
1. Pilot IT and a willing department; collect elevation requests for two weeks.
2. Build EPM rules for the top requests; publish missing apps in the portal.
3. Wave rollout by department with communications and a fast help-desk path.
4. Exceptions: named, time-bound, reviewed monthly.

## Gotchas
- Removing admin without self-service app delivery floods the help desk and creates pressure to roll back.
- Cached domain admin logons and shared IT accounts on endpoints remain an exposure; use LAPS and
  tiered admin accounts.
- Users added via nested domain groups survive naive removal scripts.

## Verify
Report shows Administrators group = approved members only on > 98% of devices; EPM logs show elevations
are for expected apps; exception list is small and dated.
