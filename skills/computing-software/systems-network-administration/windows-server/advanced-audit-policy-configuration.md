---
id: computing-software.systems-network-administration.windows-server.advanced-audit-policy-configuration
name: advanced-audit-policy-configuration
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, security-policy-settings, gpo-security-settings, advanced-audit-policy, auditpol, scenoapplylegacyauditpolicy, security-auditing, group-policy, audit-subcategories, event-log-size]
level: practitioner
status: docs-checked
description: "Configure Advanced Audit Policy by GPO: pick the subcategories Microsoft recommends for servers and DCs, and read or set them with auditpol."
sources:
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/plan/security-best-practices/audit-policy-recommendations
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/auditpol
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/auditpol-get
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/auditpol-set
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Advanced audit policy configuration

## Where it lives
GPO: *Computer Configuration > Policies > Windows Settings > Security Settings > Advanced
Audit Policy Configuration*. Set subcategories there rather than the legacy category
settings, and do not mix the two in the same GPO set.

## Subcategories Microsoft's recommendations table covers
The audit policy recommendations page grades each of these for Windows defaults, a
baseline and stronger settings, separately for member servers and domain controllers.
Read the success/failure setting for your tier from that page rather than from a copy:
- Account Logon: Credential Validation, Kerberos Authentication Service, Kerberos Service
  Ticket Operations, Other Account Logon Events (the Kerberos ones apply to DCs).
- Account Management: Computer Account Management, Security Group Management, User
  Account Management.
- Detailed Tracking: Process Creation.
- DS Access (DCs): Directory Service Access, Directory Service Changes.
- Logon/Logoff: Logon, Other Logon/Logoff Events, Special Logon.
- Object Access: File Share, Detailed File Share, Removable Storage.
- Policy Change: Audit Policy Change, Authentication Policy Change.
- Privilege Use: Sensitive Privilege Use.
- System: Security System Extension, System Integrity.
Audit Logon is enabled for both Success and Failure by default from Windows 10 version
1809; earlier versions default to Success only.

## Check and change what is effective
```cmd
auditpol /get /category:*
auditpol /get /subcategory:"Credential Validation"
auditpol /set /subcategory:"Logon" /success:enable /failure:enable
```
`/get` takes `/category` (`*` for all) or `/subcategory`, by name or GUID. `/set` takes
`/subcategory` or `/category` with `/success:` and `/failure:` set to `enable` or
`disable`; with neither given, success auditing is applied. `auditpol /list /category`
lists the categories. Use `/set` on a lab machine, since GPO re-applies policy on
domain members.

## Verify
- [ ] `auditpol /get /category:*` on a DC matches the settings chosen from the Microsoft table.

## Checked
2026-10-28. Confirmed against "Audit policy recommendations" (subcategory names, Audit Logon default from 1809) and the Learn pages for `auditpol`, `auditpol get` and `auditpol set` (`/get`, `/set`, `/list`, `/category:*`, `/subcategory`, `/success`, `/failure`, enable/disable, success default). Removed as unconfirmed: the S/F matrix (table columns do not survive in the page text), `SCENoApplyLegacyAuditPolicy` and the force-override policy name, `gpresult /h` hint, event-log sizes and the 4688/7-day checks.
Method: documentation only; no commands were run.
