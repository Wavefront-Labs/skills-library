---
id: computing-software.systems-network-administration.active-directory.delegate-ou-permissions-with-dsacls
name: delegate-ou-permissions-with-dsacls
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, delegation-of-control, ou-delegation, dsacls, delegate-password-reset, helpdesk-delegation, extended-rights, inheritance, least-privilege, ad-acl]
level: practitioner
status: docs-checked
description: "Delegate helpdesk tasks on an OU with dsacls or the wizard: password reset and unlock, create/delete users or computers, scoped to object class, to a group."
sources:
  - https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2012-r2-and-2012/cc771151(v=ws.11)
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/plan/security-best-practices/implementing-least-privilege-administrative-models
  - https://learn.microsoft.com/en-us/windows/win32/adschema/a-pwdlastset
  - https://learn.microsoft.com/en-us/windows/win32/adschema/a-lockouttime
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Delegate OU permissions (dsacls / wizard)

**Goal:** helpdesk and local IT can do their routine jobs on their OUs without Domain Admins.

## Principles
- Delegate to a **group** (`DL-Delegation-Helpdesk-PwdReset-LON`), never a user.
- Scope to the narrowest OU and to the specific **object class** (user, computer, group).
- No delegation on the domain root or on OUs containing admin accounts. Protected accounts are reset by
  AdminSDHolder/SDProp (every 60 minutes by default), but do not rely on that.

## dsacls permission syntax
`dsacls "<ObjectDN>" /G <principal>:<Permissions>[;<ObjectType or Property>][;<InheritedObjectType>]`.
`/I:T` applies to the object and its children (the default), `/I:S` to child objects only, `/I:P` to one level.
`CA` = control access (an extended right), `RP`/`WP` = read/write property, `CC`/`DC` = create/delete child,
`GA` = generic all.

## Password reset and unlock on users
```cmd
set OU="OU=Users,OU=London,DC=ad,DC=example,DC=com"
set G="AD\DL-Delegation-Helpdesk-LON"
dsacls %OU% /I:S /G %G%:CA;"Reset Password";user
dsacls %OU% /I:S /G %G%:RPWP;pwdLastSet;user
dsacls %OU% /I:S /G %G%:RPWP;lockoutTime;user
```
A `pwdLastSet` of 0 (without the never-expires flag) makes the user set a new password at the next logon, so write
access to it supports "must change at next logon". `lockoutTime` of zero means the account is not currently locked
out, so write access to it supports unlocking.

## Create and delete computer objects in a Workstations OU
```cmd
dsacls "OU=Workstations,OU=London,DC=ad,DC=example,DC=com" /I:T /G AD\DL-Delegation-Desktop-LON:CCDC;computer
dsacls "OU=Workstations,OU=London,DC=ad,DC=example,DC=com" /I:S /G AD\DL-Delegation-Desktop-LON:GA;;computer
```
(`CCDC;computer` = create and delete child computer objects; `GA;;computer` grants full control on computer
objects, which is broad; narrow it if you can.)

## Group membership management
```cmd
dsacls "OU=Groups,OU=London,DC=ad,DC=example,DC=com" /I:S /G AD\DL-Delegation-GroupMgr-LON:RPWP;member;group
```

## Wizard alternative
ADUC > right-click OU > Delegate Control. It writes ordinary ACEs; record what you delegated so it can be reviewed
and removed later.

## Remove / review
```cmd
dsacls "OU=Users,OU=London,DC=ad,DC=example,DC=com" /R AD\DL-Delegation-Helpdesk-LON
dsacls "OU=Users,OU=London,DC=ad,DC=example,DC=com" | findstr /i delegation
```

## Verify
- [ ] As a helpdesk test account: reset/unlock a London user works, a Paris user fails.
- [ ] The helpdesk account cannot reset a Domain Admin (protected by AdminSDHolder).

## Checked
2026-10-27. Documentation: Microsoft Learn dsacls reference (2012 R2 library, the current target of Microsoft's links),
Appendix C and the AD schema reference for `pwdLastSet` and `lockoutTime`. Confirmed: the PermissionStatement syntax
`principal:Permissions;ObjectType;InheritedObjectType`, `/I:{T|S|P}` meanings (T default), `/G`, `/R`, the permission codes
CA, RP, WP, CC, DC and GA, the `CC;computer` object-type scoping and the `;;user` inherited-type form; SDProp every 60
minutes by default; `pwdLastSet` 0 forces a change at next logon and `lockoutTime` 0 means not locked out. Removed as
unconfirmed: the wizard task names and the statement that the wizard cannot remove ACEs.
Method: documentation only; no commands were run.
