---
id: computing-software.systems-network-administration.active-directory.bulk-user-provisioning-from-csv
name: bulk-user-provisioning-from-csv
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, ad-users-and-groups, activedirectory-module, new-aduser, set-aduser, bulk-user-import, import-csv, provisioning, upn, samaccountname, idempotent]
level: practitioner
status: docs-checked
description: "Create and update AD users in bulk from CSV with New-ADUser/Set-ADUser: idempotent script, UPN/sAMAccountName rules, initial passwords, groups and a dry run."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/activedirectory/new-aduser
  - https://learn.microsoft.com/en-us/powershell/module/activedirectory/set-aduser
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/plan/active-directory-domain-services-maximum-limits
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bulk-create and update users from CSV

**Goal:** an idempotent import: running it twice changes nothing; new rows create users,
changed rows update them.

## CSV
```
SamAccountName,GivenName,Surname,Department,Title,Manager,OU,Groups
jsmith,Jane,Smith,Finance,Analyst,mbrown,"OU=Users,OU=Finance,DC=ad,DC=example,DC=com",GG-Finance-Staff;GG-VPN
```

## Script
```powershell
[CmdletBinding(SupportsShouldProcess)]
param([string]$Path = '.\users.csv', [string]$UpnSuffix = 'example.com',
      [scriptblock]$NewPassword = { throw 'Supply a generator that returns a random password string' })
Import-Module ActiveDirectory
foreach ($r in Import-Csv $Path) {
  $sam = $r.SamAccountName.Trim().ToLower()
  if ($sam.Length -gt 20) { Write-Warning "$sam > 20 chars"; continue }   # AD limit for user sAMAccountName
  $attrs = @{ GivenName=$r.GivenName; Surname=$r.Surname; Department=$r.Department; Title=$r.Title
              DisplayName="$($r.GivenName) $($r.Surname)" }
  $u = Get-ADUser -Filter "sAMAccountName -eq '$sam'" -Properties Department,Title,Manager
  if (-not $u) {
    $pw = & $NewPassword
    if ($PSCmdlet.ShouldProcess($sam,'New-ADUser')) {
      New-ADUser -Name $attrs.DisplayName -SamAccountName $sam -UserPrincipalName "$sam@$UpnSuffix" `
        -Path $r.OU @attrs -AccountPassword (ConvertTo-SecureString $pw -AsPlainText -Force) `
        -ChangePasswordAtLogon $true -Enabled $true
      # deliver $pw through your secure channel, never a log file
    }
  } else {
    if ($PSCmdlet.ShouldProcess($sam,'Set-ADUser')) { Set-ADUser $u @attrs }
    if ($u.DistinguishedName -notlike "*,$($r.OU)") { Move-ADObject $u -TargetPath $r.OU }
  }
  if ($r.Manager) { Set-ADUser $sam -Manager (Get-ADUser $r.Manager) }
  foreach ($g in $r.Groups -split ';' | ? { $_ }) { Add-ADGroupMember $g -Members $sam }
}
```
Run with `-WhatIf` first. The `$NewPassword` script block is your approved password generator (a vault or
`System.Security.Cryptography.RandomNumberGenerator`); never hard-code initial passwords.

## Gotchas
- Filter strings with apostrophes (`O'Brien`) break `-Filter "... '$x'"`; escape `'` as `''`.
- `-Name` (CN) must be unique within the OU; duplicates fail. Append a number or the sam.
- Check that a UPN is unused before creating it: `Get-ADUser -Filter "UserPrincipalName -eq '...'" -Server <gc>:3268`
  searches the global catalog.
- Write to one DC (`-Server`) inside a run to avoid replication races between create and update.

## Verify
- [ ] Second run reports no creates and no changes.
- [ ] Spot-check: `Get-ADUser jsmith -Properties MemberOf,Manager,Department`.

## Checked
2026-10-27. Documentation: Microsoft Learn `New-ADUser`/`Set-ADUser` reference (Windows Server 2025 docset) and AD
maximum limits. Confirmed: `New-ADUser` and `Set-ADUser` parameters used (`-Path`, `-AccountPassword`,
`-ChangePasswordAtLogon`, `-Enabled`, `-Manager`, `-UserPrincipalName`), `Move-ADObject -TargetPath`, `Add-ADGroupMember`
and the 20-character limit for user sAMAccountName; the global catalog port 3268 is documented for ldifde and AD search.
The `System.Web.Security.Membership.GeneratePassword` call and its PowerShell-version note could not be confirmed in
readable documentation and were replaced with a caller-supplied password generator; the UPN forest-wide uniqueness
statement was reworded to a check instead of a rule.
Method: documentation only; no commands were run.
