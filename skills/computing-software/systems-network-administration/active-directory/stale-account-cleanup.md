---
id: computing-software.systems-network-administration.active-directory.stale-account-cleanup
name: stale-account-cleanup
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, ad-users-and-groups, stale-accounts, search-adaccount, lastlogontimestamp, inactive-computers, account-hygiene, disable-adaccount, pwdlastset, quarantine-ou]
level: practitioner
status: docs-checked
description: "Find and retire inactive users and computers: lastLogonTimestamp limits, Search-ADAccount, pwdLastSet for computers, and a disable-move-delete workflow."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/activedirectory/search-adaccount
  - https://learn.microsoft.com/en-us/windows/win32/adschema/a-lastlogontimestamp
  - https://learn.microsoft.com/en-us/windows/win32/adschema/a-lastlogon
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/active-directory/accounts-lastlogontimestamp-future-time
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Clean up stale users and computers

## Which attribute
- `lastLogon`: not replicated; it is maintained separately on each DC, so an accurate value means querying every DC.
- `lastLogonTimestamp` (`LastLogonDate` in the ActiveDirectory module): updated at logon only if the stored value is older
  than `msDS-LogonTimeSyncInterval`; the first update after a functional level raise is 14 days minus a random
  percentage of 5 days. It is coarse: good for "inactive > 30/60/90 days", not for "last week".
- Computers change their password every 30 days by default (`pwdLastSet`); a computer with `PasswordLastSet` far
  beyond that, and no recent logon, is very likely gone.
- `lastLogonTimestamp` has limits: for example Kerberos S4U can update it, and a DC with a wrong clock can set it to a
  future time. Use other signals too (such as `pwdLastSet`), and check before disabling service accounts.

## Find
```powershell
$cut = (Get-Date).AddDays(-90)
Search-ADAccount -AccountInactive -TimeSpan 90.00:00:00 -UsersOnly |
  ? Enabled | Select Name,SamAccountName,LastLogonDate,DistinguishedName
Get-ADComputer -Filter {Enabled -eq $true} -Properties LastLogonDate,PasswordLastSet,OperatingSystem |
  ? { $_.LastLogonDate -lt $cut -and $_.PasswordLastSet -lt $cut } |
  Select Name,OperatingSystem,LastLogonDate,PasswordLastSet
Search-ADAccount -AccountDisabled -UsersOnly          # already disabled
Get-ADUser -Filter {LastLogonTimestamp -notlike '*' -and Enabled -eq $true} -Properties whenCreated  # never logged on
```

## Workflow
1. Exclude by rule: service accounts, break-glass, accounts on leave (an attribute or group
   flag), objects created in the last 30 days.
2. **Disable and move** to a quarantine OU, stamp the description with date and ticket:
```powershell
$stale | ForEach-Object {
  Disable-ADAccount $_ -WhatIf
  Set-ADObject $_ -Description "Disabled $(Get-Date -f yyyy-MM-dd) stale review CHG1234" -WhatIf
  Move-ADObject $_ -TargetPath 'OU=Disabled,DC=ad,DC=example,DC=com' -WhatIf }
```
3. Wait 30-90 days, then delete (with the Recycle Bin enabled you still have a recovery window).
4. Check hybrid: confirm in your sync tool whether the quarantine OU is in sync scope before moving objects there.

## Verify
- [ ] Monthly report count trending down; no business-critical service broken (review helpdesk tickets).
- [ ] Quarantine OU has GPO/permissions that block logon even if re-enabled accidentally (optional).

## Checked
2026-10-27. Documentation: Microsoft Learn `Search-ADAccount`/`Get-ADComputer` references, AD schema pages for
`lastLogon` and `lastLogonTimestamp`, the lastLogonTimestamp future-time article and the machine-account password policy page.
Confirmed: `lastLogon` is not replicated and kept per DC; lastLogonTimestamp updates only when older than
`msDS-LogonTimeSyncInterval` and the initial update after a functional-level raise is 14 days minus a random percentage of
5 days; default machine-account password change every 30 days; Kerberos S4U and wrong DC clocks affect the value;
`Search-ADAccount -AccountInactive -TimeSpan -UsersOnly`, `-AccountDisabled`; `LastLogonDate` and `PasswordLastSet` are
Get-ADComputer properties. Removed as unconfirmed: the 9-14 day range from the description, the statement that LDAP simple
bind and cloud paths do not update logon attributes, and the 30-day Entra soft-delete note (the description was shortened to
match).
Method: documentation only; no commands were run.
