---
id: computing-software.systems-network-administration.active-directory.clean-up-built-in-privileged-groups
name: clean-up-built-in-privileged-groups
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, privileged-access, privileged-groups-cleanup, adminsdholder, ad-tiering]
level: advanced
status: docs-checked
description: "Empty and monitor built-in privileged groups (Schema, Enterprise and Domain Admins, Account, Server, Backup and Print Operators, DnsAdmins) and alert on changes."
sources:
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/plan/security-best-practices/appendix-b--privileged-accounts-and-groups-in-active-directory
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/plan/security-best-practices/reducing-the-active-directory-attack-surface
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/plan/appendix-l--events-to-monitor
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cleaning up built-in privileged groups

Operator groups are forgotten Tier 0. Per Microsoft's privileged-groups appendix: Backup Operators can override
security restrictions to back up and restore files; Server Operators administer domain controllers (log on
locally, back up and restore files, change the system time, shut down); Print Operators hold "Load and unload
device drivers" and log on locally; DnsAdmins have administrative access to the DNS Server service.

## Report membership (recursive)
```powershell
$groups = 'Enterprise Admins','Schema Admins','Domain Admins','Administrators','Account Operators',
  'Server Operators','Backup Operators','Print Operators','DnsAdmins','Group Policy Creator Owners','Cert Publishers'
foreach ($g in $groups) {
  Get-ADGroupMember $g -Recursive -ErrorAction SilentlyContinue |
    Select @{n='Group';e={$g}},Name,objectClass,SamAccountName }
```

## Target state (recommended practice)
| Group | Target |
|---|---|
| Schema Admins, Enterprise Admins | empty; add for the change window only (Microsoft: Schema Admins is meant to be populated only temporarily) |
| Domain Admins | a handful of named Tier 0 admin accounts, no service accounts (Microsoft: break-glass use in a well-delegated model) |
| Account, Server, Print, Backup Operators | empty; delegate specific rights instead |
| DnsAdmins | empty or Tier 0 only; delegate DNS zone rights per zone |
| Administrators (builtin) | Domain Admins, Enterprise Admins, Administrator only |

## Handling leftovers
- Service accounts in Domain Admins: find what they need (often local admin on some servers or rights in one OU)
  and grant that; consider gMSAs.
- Protected accounts and groups keep non-default ACLs set by AdminSDHolder; check any former member for
  inheritance and permissions before treating it as an ordinary object.
- Built-in Administrator account: long random password in a vault, used only for recovery.

## Monitor
- Security events **4728** (member added to a security-enabled global group), **4732** (local group) and **4756**
  (universal group) on DCs for these group SIDs; alert in your SIEM.

## Verify
- [ ] Report shows target state; alerts tested by adding and removing a test account.

## Checked
2026-10-27. Documentation: Microsoft Learn Appendix B (Privileged Accounts and Groups), Reducing the AD Attack
Surface and Appendix L (Events to Monitor). Confirmed: default rights of Backup, Server and Print Operators and the
DnsAdmins description; Schema Admins is intended to be populated only temporarily; Domain Admins membership should be
needed only in break-glass cases in a well-designed delegation model; events 4728, 4732 and 4756 mean a member was added
to a global, local or universal security group. Removed as unconfirmed: Backup Operators reading NTDS.dit, Server
Operators changing services, DnsAdmins loading a DLL, the adminCount reset step and the Defender for Identity alert name.
The target-state table is recommended practice, not a Microsoft requirement.
Method: documentation only; no commands were run.
