---
id: computing-software.systems-network-administration.active-directory.computer-account-and-secure-channel
name: computer-account-and-secure-channel
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, ad-users-and-groups, computer-account, test-computersecurechannel, secure-channel, trust-relationship-failed, reset-computermachinepassword, prestaging, machine-password, nltest-sc-verify, netlogon-secure-channel, dc-health]
level: practitioner
status: docs-checked
description: "Pre-stage computer accounts, and fix 'trust relationship between this workstation and the primary domain failed' without rejoining using Test-ComputerSecureChannel -Repair."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/test-computersecurechannel
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/reset-computermachinepassword
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/netdom-resetpwd
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/windows-security/use-netdom-reset-domain-controller-password
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/windows-security/disable-machine-account-password
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# Computer accounts and the secure channel

## Pre-stage a computer account
Lets a non-admin (or a build process) join into the right OU without broad rights:
```powershell
New-ADComputer -Name APP07 -Path 'OU=Servers,DC=ad,DC=example,DC=com' `
  -Description 'Payroll app server' -ManagedBy 'GG-Payroll-Admins'
# allow a specific group to join/reset this account (ADUC: "The following user or group can join this computer")
```
Pre-staging also avoids the default `ms-DS-MachineAccountQuota` path (any user can join 10
machines), which you should set to 0.

## "The trust relationship between this workstation and the primary domain failed"
Cause: the machine account password stored on the member no longer matches the one on the computer object.
Windows changes it automatically every 30 days by default.

Fix without rejoining (log on with a local admin or cached domain admin):
```powershell
Test-ComputerSecureChannel -Verbose                       # False = broken
Test-ComputerSecureChannel -Repair -Credential (Get-Credential AD\admin)
# or
Reset-ComputerMachinePassword -Server dc01 -Credential (Get-Credential AD\admin)
```
On a DC, `Test-ComputerSecureChannel` returns false positives; use `netdom resetpwd /server:<otherDC>
/userd:AD\admin /passwordd:*` from an elevated prompt on that DC (Microsoft's procedure stops the Kerberos Key
Distribution Center service and sets it to Manual first).

Check from outside:
```cmd
nltest /server:APP07 /sc_query:ad.example.com
```

## Prevention
- Do not revert member VMs to snapshots older than the machine password age (30 days by
  default) without expecting this.
- Never clone a domain-joined machine without sysprep.
- Do not disable machine password changes (`DisablePasswordChange`) as a workaround;
  it weakens the account.

## Verify
- [ ] `Test-ComputerSecureChannel` returns True.
- [ ] `Get-ADComputer APP07 -Properties PasswordLastSet` shows a fresh timestamp after repair.

## Checked
2026-10-27, against the Test-ComputerSecureChannel, Reset-ComputerMachinePassword and New-ADComputer cmdlet pages, the netdom resetpwd reference (windowsserverdocs), "Use Netdom.exe to reset machine account passwords of a domain controller", "Disable machine account password changes" and the domain-join articles (SupportArticles-docs). Confirmed: Test-ComputerSecureChannel -Repair -Server -Credential and its false positives on DCs; Reset-ComputerMachinePassword -Server -Credential; netdom resetpwd syntax, elevation and the KDC stop step; machine password changes every 30 days by default and the DisablePasswordChange value; ms-DS-MachineAccountQuota default of 10; New-ADComputer -Name -Path -Description -ManagedBy; `nltest /sc_query`. Removed as unconfirmed: `nltest /sc_verify` and the list of causes (snapshot, clone, reset object).

Method: documentation only; no commands were run.
