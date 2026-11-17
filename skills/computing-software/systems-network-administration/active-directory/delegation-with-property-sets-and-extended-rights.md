---
id: computing-software.systems-network-administration.active-directory.delegation-with-property-sets-and-extended-rights
name: delegation-with-property-sets-and-extended-rights
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, ou-delegation, property-sets, extended-rights, dsacls, reset-password]
level: advanced
status: docs-checked
description: "Delegate granular AD rights with property sets and extended rights (Reset Password, Personal Information, Validated writes) using dsacls and the GUI wizard."
sources:
  - https://learn.microsoft.com/en-us/windows/win32/adschema/property-sets
  - https://learn.microsoft.com/en-us/windows/win32/adschema/r-user-account-restrictions
  - https://learn.microsoft.com/en-us/windows/win32/adschema/extended-rights
  - https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2012-r2-and-2012/cc771151(v=ws.11)
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Granular delegation with property sets and extended rights

Granting Full Control on an OU to a helpdesk group is the common shortcut that becomes an attack path. Delegate
the exact right instead.

## Building blocks
- **Property sets** group attributes under one GUID, so one ACE covers every attribute in the set. Active Directory
  defines sets such as Personal Information, Public Information, General Information, Web Information, Email
  Information, Logon Information (`User-Logon`) and Account Restrictions (`User-Account-Restrictions`, whose members
  are `accountExpires`, `pwdLastSet`, `userAccountControl` and `userParameters`).
- **Extended rights**: control-access rights such as `Reset Password` (`User-Force-Change-Password`),
  `Change Password` (`User-Change-Password`), `Send As` and `Replicating Directory Changes All`.
- **Validated writes**: e.g. `Validated write to DNS host name` and `Validated write to service principal name`
  (writes restricted to valid values).

## dsacls examples
```cmd
REM helpdesk resets passwords and forces change at next logon on user objects
dsacls "OU=Staff,DC=ad,DC=example,DC=com" /I:S /G "AD\GG-Helpdesk:CA;Reset Password;user"
dsacls "OU=Staff,DC=ad,DC=example,DC=com" /I:S /G "AD\GG-Helpdesk:RPWP;pwdLastSet;user"
REM unlock accounts
dsacls "OU=Staff,DC=ad,DC=example,DC=com" /I:S /G "AD\GG-Helpdesk:RPWP;lockoutTime;user"
REM HR edits phone/address (property set)
dsacls "OU=Staff,DC=ad,DC=example,DC=com" /I:S /G "AD\GG-HR:RPWP;Personal Information;user"
```
`/I:S` = child objects only; the last field is the object type the ACE is inherited by.

## Check
```powershell
(Get-Acl "AD:OU=Staff,DC=ad,DC=example,DC=com").Access | ? IdentityReference -like '*Helpdesk*' |
  ft ActiveDirectoryRights,ObjectType,InheritedObjectType,InheritanceType
```
ObjectType GUIDs map to names via the schema (`schemaIDGUID`) and Extended-Rights container (`rightsGuid`).

## Gotchas
- Protected accounts are managed by AdminSDHolder and SDProp (default every 60 minutes), which resets their
  permissions, so OU delegations do not stick on them. That is a feature.
- Write `member` on a group is a separate right. The Account Restrictions property set includes
  `userAccountControl`, which holds the Kerberos delegation flag (`TRUSTED_FOR_DELEGATION`, 0x80000), so grant it
  narrowly.

## Verify
- [ ] A helpdesk test account can reset a password and unlock, but cannot edit group membership or other attributes.

## Checked
2026-10-27. Documentation: Microsoft Learn AD schema reference (property sets, extended rights, User-Account-
Restrictions, Personal-Information, User-Force-Change-Password), dsacls reference and Appendix C. Confirmed: the listed
property sets exist (Display names Personal Information and Account Restrictions); Account Restrictions members are Account-
Expires, Pwd-Last-Set, User-Account-Control and User-Parameters; `Reset Password` is `User-Force-Change-Password`; the
`Send-As`, `User-Change-Password` and replication rights exist; `TRUSTED_FOR_DELEGATION` is 0x80000 in userAccountControl;
dsacls syntax as in the delegation skill. Removed as unconfirmed: the adminCount wording and the Public/Web membership
detail beyond the set names.
Method: documentation only; no commands were run.
