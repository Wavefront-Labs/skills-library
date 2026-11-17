---
id: computing-software.systems-network-administration.active-directory.rodc-krbtgt-accounts
name: rodc-krbtgt-accounts
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, rodc, rodc-krbtgt, kerberos, krbtgt-reset]
level: advanced
status: docs-checked
description: "Understand and manage per-RODC krbtgt_NNNNN accounts: ticket isolation, what happens when an RODC is lost, and resetting or cleaning them up."
sources:
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/forest-recovery-guide/ad-forest-recovery-reset-the-krbtgt-password
  - https://learn.microsoft.com/en-us/powershell/module/activedirectory/get-addomaincontrollerpasswordreplicationpolicyusage
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Per-RODC krbtgt accounts

Every RODC has its own Kerberos ticket-granting account named `krbtgt_<number>` (for example `krbtgt_35512`), separate
from the domain `krbtgt`.

## What Microsoft's docs say
- RODC `krbtgt_<number>` accounts are listed in that format; in a forest recovery, do not delete the krbtgt accounts of
  RODCs you plan to recover.
- The forest recovery procedure for resetting the domain `krbtgt` password applies to writable DCs, not to RODCs. Resetting
  the domain `krbtgt` does not reset RODC krbtgt accounts, so plan RODC handling separately.
- `Get-ADDomainControllerPasswordReplicationPolicyUsage` output lists `krbtgt_<number>` accounts among an RODC's
  accounts (they appear disabled).

## Find them
```powershell
Get-ADUser -Filter 'Name -like "krbtgt_*"' -Properties pwdLastSet |
  Select Name,@{n='PwdSet';e={[datetime]::FromFileTime($_.pwdLastSet)}}
```

## Gotchas
- Do not delete a krbtgt_ account while its RODC still exists.
- Mechanics such as how the RODC signs tickets, the link attributes between the account and the RODC, what happens when
  the RODC computer object is deleted, and Microsoft's reset scripts are not covered by the GitHub-hosted docs used for
  this check; read the RODC documentation before acting on them.

## Verify
- [ ] Every RODC has a krbtgt_<number> account and no krbtgt_ account is deleted while its RODC exists.
- [ ] RODC krbtgt handling is written into the same runbook as the domain krbtgt reset.

## Checked

Documentation: Microsoft Learn "AD Forest Recovery - Reset the krbtgt password" (updated 2025-05) and the
Get-ADDomainControllerPasswordReplicationPolicyUsage reference, from MicrosoftDocs/windowsserverdocs and MicrosoftDocs/windows-powershell-docs, main branch (latest commits 2026-10-23).
Confirmed: the `krbtgt_<number>` naming, the do-not-delete instruction for RODCs being recovered, the reset procedure
applying to writable DCs only. Removed unconfirmed claims: `msDS-KrbTgtLink`/`msDS-KrbTgtLinkBl` attributes, ticket
re-issue behaviour, the deletion prompt, the New-KrbtgtKeys script, and orphan handling.

Method: documentation only; no commands were run.
