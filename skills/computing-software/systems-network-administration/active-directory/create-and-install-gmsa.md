---
id: computing-software.systems-network-administration.active-directory.create-and-install-gmsa
name: create-and-install-gmsa
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, gmsa, group-managed-service-account, new-adserviceaccount, principalsallowedtoretrievemanagedpassword, install-adserviceaccount, test-adserviceaccount, spn, kerberos]
level: practitioner
status: docs-checked
description: "Create a gMSA scoped to a host group, install and test it on servers, set SPNs and encryption types, and fix 'cannot retrieve password' errors."
sources:
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/group-managed-service-accounts/group-managed-service-accounts/manage-group-managed-service-accounts
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/group-managed-service-accounts/group-managed-service-accounts/group-managed-service-accounts-overview
  - https://learn.microsoft.com/en-us/powershell/module/activedirectory/new-adserviceaccount
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Create and install a gMSA

**Goal:** a service account whose password AD manages automatically and that only named hosts can use.
Prerequisite: a KDS root key (see the KDS skill) and domain and forest functional levels of Windows Server 2012 or
later (Microsoft's recommendation to support gMSA features for all devices).

## Create
```powershell
New-ADGroup 'GG-gMSA-SQLProd-Hosts' -GroupScope Global -Path 'OU=Service Groups,DC=ad,DC=example,DC=com'
Add-ADGroupMember 'GG-gMSA-SQLProd-Hosts' -Members 'SQL01$','SQL02$'
New-ADServiceAccount -Name gmsaSqlProd -DNSHostName gmsaSqlProd.ad.example.com `
  -PrincipalsAllowedToRetrieveManagedPassword 'GG-gMSA-SQLProd-Hosts' `
  -KerberosEncryptionType AES128,AES256 `
  -ServicePrincipalNames 'MSSQLSvc/sql01.ad.example.com:1433','MSSQLSvc/sql01.ad.example.com'
```
- Put the computer accounts that may use the gMSA in a security group and pass it to
  `-PrincipalsAllowedToRetrieveManagedPassword`.
- `-ManagedPasswordIntervalInDays` can only be set at creation; to change it you must create a new gMSA.
- `-KerberosEncryptionType` accepts None, DES, RC4, AES128 and AES256. Failover clusters do not support gMSAs
  (services running on top of a cluster can still use them, per Microsoft's overview).

## Install on each host
On each host (needs the AD PowerShell module):
```powershell
Install-ADServiceAccount -Identity gmsaSqlProd
Test-ADServiceAccount -Identity gmsaSqlProd   # True means the host can retrieve the password
```
Then configure the service to log on as `AD\gmsaSqlProd$` with no password. The host must already be in the group
that may retrieve the password when you run these.

## Troubleshoot Test-ADServiceAccount = False
- Host not in the allowed group (Microsoft: membership in the group, or delegated permission, is needed for the test
  to succeed).
- KDS root key missing or not yet effective (see KDS skill).
- Host cannot reach a suitable DC.

## Verify
- [ ] `Test-ADServiceAccount` True on every host in the group.
- [ ] `Get-ADServiceAccount gmsaSqlProd -Properties PrincipalsAllowedToRetrieveManagedPassword,ServicePrincipalNames`
  shows the intended group and SPNs.

## Checked

Documentation: Microsoft Learn "Manage group Managed Service Accounts" and gMSA overview (both updated 2025), and the
New-ADServiceAccount, Install-ADServiceAccount and Test-ADServiceAccount references, from MicrosoftDocs/windowsserverdocs and MicrosoftDocs/windows-powershell-docs, main branch (latest commits 2026-10-23).
Confirmed: New-ADServiceAccount parameters used (`-DNSHostName`, `-PrincipalsAllowedToRetrieveManagedPassword`,
`-KerberosEncryptionType` values, `-ServicePrincipalNames`, `-ManagedPasswordIntervalInDays` at creation only),
Install-/Test-ADServiceAccount usage, functional-level recommendation, no failover cluster support. Removed unconfirmed:
the 240-character and 30-day figures, the 15-character name limit, ticket purge/reboot, Log on as a service,
`sc.exe` and RSAT feature commands, and the msDS-SupportedEncryptionTypes note.

Method: documentation only; no commands were run.
