---
id: computing-software.systems-network-administration.active-directory.account-expiration-and-account-properties
name: account-expiration-and-account-properties
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, users-groups, account-expiration, set-adaccountexpiration, logon-hours, useraccountcontrol]
level: intro
status: docs-checked
description: "Set and audit AD account expiry, logon hours and workstation restrictions with Set-ADAccountExpiration and Search-ADAccount, for contractors and leavers."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/activedirectory/set-adaccountexpiration
  - https://learn.microsoft.com/en-us/powershell/module/activedirectory/search-adaccount
  - https://learn.microsoft.com/en-us/windows/win32/adschema/a-accountexpires
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Account expiration and account restrictions

## Expiry for contractors
```powershell
Set-ADAccountExpiration -Identity c-jdoe -DateTime '2026-12-31 18:00'
Set-ADAccountExpiration -Identity c-jdoe -TimeSpan 90.00:00:00   # 90 days from now
Clear-ADAccountExpiration -Identity c-jdoe                       # never expires
Get-ADUser c-jdoe -Properties AccountExpirationDate,accountExpires | Select Name,AccountExpirationDate
```
`-DateTime` sets an exact time; `-TimeSpan` sets a period from the current time. `accountExpires` is a count of
100-nanosecond intervals since 1601-01-01 UTC; a value of 0 or 9223372036854775807 (0x7FFFFFFFFFFFFFFF) means the
account never expires. ADUC and PowerShell can present the end date differently, so pick one convention and record it.

An expired account cannot sign in. For urgent leavers also disable the account (`Disable-ADAccount`) and end
sessions that are already open.

## Find accounts
```powershell
Search-ADAccount -AccountExpiring -TimeSpan 14.00:00:00 -UsersOnly | Select Name,AccountExpirationDate
Search-ADAccount -AccountExpired -UsersOnly
```
Email managers from that list on a scheduled task.

## Logon hours and workstations
```powershell
Set-ADUser c-jdoe -LogonWorkstations 'BR1-PC01,BR1-PC02'      # comma-separated computer names
```
Logon hours are stored in the `logonHours` attribute and are easiest to set in ADUC > Account > Logon Hours.

## Verify
- [ ] Contractor accounts all have an AccountExpirationDate; `Search-ADAccount -AccountExpired` shows no enabled
      leavers still in privileged groups.

## Checked
2026-10-27. Documentation: Microsoft Learn ActiveDirectory module reference (Windows Server 2025 docset) and the
Windows AD schema reference. Confirmed: `Set-ADAccountExpiration` has `-DateTime` (exact time) and `-TimeSpan` (period
from now); `Search-ADAccount -AccountExpiring -TimeSpan -UsersOnly` and `-AccountExpired`; `Set-ADUser -LogonWorkstations`
takes a comma-separated list; `accountExpires` is 100-ns intervals since 1601 UTC and 0 or 0x7FFFFFFFFFFFFFFF means never.
Removed as unconfirmed in readable documentation: the event 4768/4625 failure codes, the 10-hour ticket statement, the
1024-character workstation limit, the 21-byte/UTC logon-hours detail and the ADUC end-of-day behaviour.
Method: documentation only; no commands were run.
