---
id: computing-software.systems-network-administration.active-directory.rodc-password-replication-policy
name: rodc-password-replication-policy
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, rodc, read-only-domain-controller, password-replication-policy, rodc-prp, prepopulate-passwords, allowed-rodc-password-replication-group, denied-rodc-password-replication-group, get-addomaincontrollerpasswordreplicationpolicy, msds-revealedlist, branch-office]
level: practitioner
status: docs-checked
description: "Manage RODC Password Replication Policy: allowed vs denied lists, never caching admins, prepopulating branch users, and auditing what was revealed."
sources:
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/deploy/rodc/install-a-windows-server-2012-active-directory-read-only-domain-controller--rodc---level-200-
  - https://learn.microsoft.com/en-us/powershell/module/activedirectory/add-addomaincontrollerpasswordreplicationpolicy
  - https://learn.microsoft.com/en-us/powershell/module/activedirectory/get-addomaincontrollerpasswordreplicationpolicyusage
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RODC Password Replication Policy (PRP)

**Goal:** the RODC can authenticate branch users and computers locally when the WAN is down,
while caching nothing that would hurt if the box were stolen.

## The model
Accounts on the RODC's list set to **Deny**, or not on the list, do not cache their password; those that cannot cache and
cannot reach a writable DC cannot access resources provided by AD (Microsoft's RODC install page). When you install an
RODC without the advanced-mode wizard, the defaults are:
- Administrators: Deny; Server Operators: Deny; Backup Operators: Deny; Account Operators: Deny;
- `Denied RODC Password Replication Group`: Deny; `Allowed RODC Password Replication Group`: Allow.

Design per RODC: allow the branch's user group **and** its computer accounts, and never allow privileged accounts.

## Manage
```powershell
# Per-RODC allow list
Add-ADDomainControllerPasswordReplicationPolicy -Identity BR01-RODC `
  -AllowedList 'GG-BR01-Users','GG-BR01-Computers'
# Explicit deny for anything sensitive that could log on there
Add-ADDomainControllerPasswordReplicationPolicy -Identity BR01-RODC -DeniedList 'GG-Tier0-Admins'
Get-ADDomainControllerPasswordReplicationPolicy -Identity BR01-RODC -Allowed
Get-ADDomainControllerPasswordReplicationPolicy -Identity BR01-RODC -Denied
```
At install time the same lists are set with `-AllowPasswordReplicationAccountName` and `-DenyPasswordReplicationAccountName`
on `Add-ADDSReadOnlyDomainControllerAccount` / `Install-ADDSDomainController`.

## Audit what is cached
```powershell
Get-ADDomainControllerPasswordReplicationPolicyUsage -Identity BR01-RODC -RevealedAccounts |
  Select Name,ObjectClass
Get-ADDomainControllerPasswordReplicationPolicyUsage -Identity BR01-RODC -AuthenticatedAccounts
```
`-RevealedAccounts` returns the accounts in the revealed list of the RODC; `-AuthenticatedAccounts` lists accounts that
have authenticated to it. An admin account in the revealed list means the PRP was wrong.

## Verify
- [ ] No member of a privileged group appears in `-RevealedAccounts`.
- [ ] Both the branch user group and the branch computer group are in the allowed list.

## Checked

Documentation: Microsoft Learn "Install a Windows Server 2012 AD RODC" (default PRP) and the
Add-/Get-ADDomainControllerPasswordReplicationPolicy and Get-ADDomainControllerPasswordReplicationPolicyUsage references,
from MicrosoftDocs/windowsserverdocs and MicrosoftDocs/windows-powershell-docs, main branch (latest commits 2026-10-23).
Confirmed: default allow/deny list when not using advanced mode, deny/implicit behaviour, cmdlet parameters
(`-AllowedList`, `-DeniedList`, `-Allowed`, `-Denied`, `-RevealedAccounts`, `-AuthenticatedAccounts`), install-time
parameters. Removed unconfirmed claims: attribute names `msDS-RevealOnDemandGroup`/`msDS-NeverRevealGroup`, the contents
of the Denied group, the `repadmin /rodcpwdrepl` prepopulate command, the "deny wins" tie rule and WAN-cut test.

Method: documentation only; no commands were run.
