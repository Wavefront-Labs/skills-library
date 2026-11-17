---
id: computing-software.systems-network-administration.active-directory.rodc-compromise-response
name: rodc-compromise-response
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, rodc, read-only-domain-controller, rodc-compromise, rodc-reset-passwords, stolen-dc, incident-response, krbtgt-rodc, revealed-accounts, metadata-cleanup]
level: advanced
status: gated
description: "Respond to a stolen or compromised RODC: delete its account with password resets, reset every revealed credential, its krbtgt_xxxx, and rebuild."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/activedirectory/get-addomaincontrollerpasswordreplicationpolicyusage
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/forest-recovery-guide/ad-forest-recovery-reset-the-krbtgt-password
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RODC stolen or compromised

**Goal:** make everything the RODC knew worthless, then rebuild it.

## What an attacker holding the disk has
- Credentials of every account whose password was cached on the RODC (the **revealed** list; users and computers).
- Its own **krbtgt_NNNNN** account key (each RODC has a separate krbtgt) (gated: unconfirmed, source is paywalled or blocked).
- A read-only copy of the directory.

## Response
1. **Capture the revealed list first** (deleting the account removes it):
```powershell
Get-ADDomainControllerPasswordReplicationPolicyUsage -Identity BR01-RODC -RevealedAccounts |
  Select Name,SamAccountName,ObjectClass | Export-Csv revealed-BR01.csv -NoTypeInformation
```
2. **Delete the RODC computer object** in ADUC (Domain Controllers OU). The wizard offers (gated: unconfirmed, source is paywalled or blocked):
   - Reset all passwords for user accounts that were cached on this RODC
   - Reset all passwords for computer accounts that were cached on this RODC
   - Export the list of cached accounts to a file
   Tick all three. Users must then have passwords reset by the helpdesk before next logon;
   computers lose their secure channel and must be rejoined.
   Deleting the object also performs metadata cleanup and removes its `krbtgt_NNNNN` account (gated: unconfirmed, source is paywalled or blocked).
3. **Service accounts in the list:** reset them deliberately and update every service using them.
4. **DNS:** remove its DNS records if they remain.
5. **Hunt:** review security logs on writable DCs for logons by revealed accounts after the
   theft time; check whether any privileged account appears in the list (if so, treat as a
   full domain compromise and follow the forest recovery guidance for resetting the krbtgt password).
6. **Rebuild** with a new name or same name via a fresh staged install; re-establish PRP.

## Gotchas
- If you delete the object without the reset options, you lose the easy reset path; use the CSV export.

## Verify
- [ ] Every account in the CSV shows `PasswordLastSet` after the incident time.
- [ ] `Get-ADUser -Filter 'Name -like "krbtgt_*"'` no longer lists the old RODC's krbtgt.
- [ ] No replication errors referring to the removed RODC.

## Checked
Checked 2026-10-27 against Microsoft Learn (Get-ADDomainControllerPasswordReplicationPolicyUsage reference, Windows Server 2025; AD forest recovery guide, krbtgt reset page).
- Confirmed: Get-ADDomainControllerPasswordReplicationPolicyUsage -Identity <rodc> -RevealedAccounts returns the accounts with passwords stored on the RODC; -AuthenticatedAccounts lists accounts the RODC authenticated.
- Gated: the delete-account wizard options and the per-RODC krbtgt_NNNNN behaviour. Reason: the RODC administration pages are previous-versions only and could not be read.
- Removed: the claims about ticket trust scope, password-history behaviour and BitLocker.
This is incident-response guidance; follow your organisation's incident process and Microsoft's current RODC documentation.

Method: documentation only; no commands were run.
