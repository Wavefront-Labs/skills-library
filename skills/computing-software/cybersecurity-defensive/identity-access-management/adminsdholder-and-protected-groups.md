---
id: computing-software.cybersecurity-defensive.identity-access-management.adminsdholder-and-protected-groups
name: adminsdholder-and-protected-groups
category: computing-software
field: cybersecurity-defensive
product: identity-access-management
tags: [active-directory-security, adminsdholder, sdprop, admincount, protected-groups, acl-persistence, privileged-groups]
level: advanced
status: docs-checked
description: "Understand and audit AdminSDHolder and SDProp: which groups are protected, adminCount leftovers, ACL backdoors on AdminSDHolder, and how to clean up and monitor."
sources: ["https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/plan/security-best-practices/appendix-c--protected-accounts-and-groups-in-active-directory", "https://adsecurity.org/?p=1906", "https://learn.microsoft.com/en-us/windows/security/threat-protection/auditing/event-5136"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AdminSDHolder and protected groups

## How it works
`CN=AdminSDHolder,CN=System,DC=corp,DC=example` holds a template ACL. Every 60 minutes the SDProp
process on the PDC emulator copies that ACL onto members of protected groups (Domain Admins, Enterprise
Admins, Schema Admins, Administrators, Account/Server/Print/Backup Operators, Domain Controllers,
krbtgt, Replicator, and others), disables inheritance on them, and sets `adminCount=1`.

Purpose: stop delegated OU admins from controlling privileged accounts.
Abuse: an attacker who adds an ACE to AdminSDHolder (e.g. GenericAll for a low-priv user) gets it
re-applied to every privileged account hourly, surviving cleanup of individual objects.

## Audit the template ACL
```powershell
$dn = "CN=AdminSDHolder,CN=System," + (Get-ADDomain).DistinguishedName
(Get-Acl "AD:$dn").Access | Where-Object { $_.IdentityReference -notmatch 'SYSTEM|Domain Admins|Enterprise Admins|Administrators|SELF|Authenticated Users|Pre-Windows|Windows Authorization|Cert Publishers|Terminal Server' } |
  Select IdentityReference, ActiveDirectoryRights, AccessControlType
```
Any user or non-default group with write rights is a finding. Compare with a fresh domain's default ACL.

## adminCount leftovers
Accounts removed from protected groups keep `adminCount=1` and inheritance disabled, so OU delegation
and GPO-delivered permissions do not apply to them; they also inflate "privileged" counts.
```powershell
Get-ADUser -LDAPFilter "(adminCount=1)" -Properties memberOf, adminCount | Select Name, memberOf
```
For accounts no longer privileged: clear `adminCount` and re-enable inheritance on the object
(Security > Advanced > Enable inheritance), carefully, one at a time.

## Monitor
- Event 5136 (directory service changes, requires SACL on AdminSDHolder) for modifications of
  the AdminSDHolder object's ACL: should be essentially never.
- Changes in protected group membership.

## Gotchas
- Changes take effect at the next SDProp run (every 60 minutes);
  wait for it when testing.
- Document any intentional extra ACEs on AdminSDHolder.
- Do not "fix" by changing the SDProp interval or excluding groups without a strong reason.

## Verify
AdminSDHolder ACL matches the approved baseline, the adminCount=1 population equals current protected
group membership (plus documented exceptions), and an alert fires on a test ACL change in a lab.

## Checked

2026-10-28. Confirmed against the adsecurity.org AdminSDHolder article and the Event 5136 page: SDProp runs every 60 minutes on the PDC emulator, protected group list, adminCount=1 with inheritance disabled and not cleared on removal, 5136 for directory object changes. Removed: nTSecurityDescriptor attribute name, 4728/4732/4756 event ids, Defender for Identity and PingCastle claim, RunProtectAdminGroupsTask, dsHeuristics, Exchange ACE history.

Method: documentation only; no commands were run.
