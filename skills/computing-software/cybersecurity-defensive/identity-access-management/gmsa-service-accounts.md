---
id: computing-software.cybersecurity-defensive.identity-access-management.gmsa-service-accounts
name: gmsa-service-accounts
category: computing-software
field: cybersecurity-defensive
product: identity-access-management
tags: [pam, gmsa, group-managed-service-accounts, service-accounts, kerberoasting, kds-root-key, active-directory]
level: practitioner
status: gated
description: "Replace static service account passwords with group managed service accounts (gMSA): KDS root key, creation, host permissions, installing on services and tasks, and limits."
sources: ["https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/group-managed-service-accounts/group-managed-service-accounts/group-managed-service-accounts-overview", "https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/group-managed-service-accounts/group-managed-service-accounts/getting-started-with-group-managed-service-accounts", "https://attack.mitre.org/techniques/T1558/003/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Group managed service accounts (gMSA)

**Goal:** Windows services, scheduled tasks and IIS app pools run as accounts whose
passwords are long random values managed and rotated automatically by AD, so no human knows them
and password rotation is not a manual task.

## One-time: KDS root key
```powershell
Add-KdsRootKey -EffectiveImmediately   # (gated: unconfirmed, source is paywalled or blocked) replication delay applies before use
# see the KDS root key article for lab-only options
```

## Create a gMSA
```powershell
New-ADGroup -Name "gMSA-SQL-Hosts" -GroupScope Global
Add-ADGroupMember "gMSA-SQL-Hosts" -Members "SQL01$","SQL02$"
New-ADServiceAccount -Name svc-sql -DNSHostName svc-sql.example.com `
  -PrincipalsAllowedToRetrieveManagedPassword "gMSA-SQL-Hosts" `
  -ServicePrincipalNames "MSSQLSvc/sql01.example.com:1433" `
  -KerberosEncryptionType AES128,AES256 -ManagedPasswordIntervalInDays 30
```
Hosts must reboot after being added to the group to get the
new group membership in their tickets.

## Install and use
On each host:
```powershell
Install-ADServiceAccount svc-sql      # needs RSAT AD PowerShell
Test-ADServiceAccount svc-sql         # must return True
```
- Services: set Log On As `EXAMPLE\svc-sql$` with an empty password (`sc.exe config <svc> obj= EXAMPLE\svc-sql$`).
- Scheduled tasks: `New-ScheduledTaskPrincipal -UserId "EXAMPLE\svc-sql$" -LogonType Password`.
- IIS app pools: identity `EXAMPLE\svc-sql$`, password blank.
Grant rights on resources to the gMSA like any account (least privilege; *Log on as a service*
via GPO if restricted).

## What gMSA cannot do
- Interactive logons, or apps that need the password typed into a config file.
- Non-Windows systems (treat as exceptions).
- Cross-forest use without trusts configured.
For these, use vaulted accounts with rotation (PAM) and long random passwords.

## Security considerations
- `PrincipalsAllowedToRetrieveManagedPassword` is the crown: anyone controlling a host in that
  group can read the password. Keep the group small; do not add
  low-tier machines for tier-0 gMSAs.
- Audit who can modify the gMSA object and the retrieval group.

## Verify
`Test-ADServiceAccount` True on all hosts; services running under `$` accounts; inventory of
remaining user-based service accounts with SPNs trending to zero.

## Checked

2026-10-28. Confirmed against the gMSA overview and getting-started pages: PrincipalsAllowedToRetrieveManagedPassword, ManagedPasswordIntervalInDays, KDS root key required. Gated: the Add-KdsRootKey command and effective time. Removed: 240-byte figure, 10-hour wait, lab EffectiveTime trick, klist purge, msDS-ManagedPassword and ReadGMSAPassword names, SQL Server claim.

Method: documentation only; no commands were run.
