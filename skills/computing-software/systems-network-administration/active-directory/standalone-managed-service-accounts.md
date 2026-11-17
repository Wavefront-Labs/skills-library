---
id: computing-software.systems-network-administration.active-directory.standalone-managed-service-accounts
name: standalone-managed-service-accounts
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, gmsa, standalone-managed-service-account, smsa, new-adserviceaccount, install-adserviceaccount]
level: practitioner
status: docs-checked
description: "Use standalone MSAs (sMSA) vs gMSAs, create and install an sMSA on one server, and replace user accounts running services without stored passwords."
sources:
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/group-managed-service-accounts/group-managed-service-accounts/group-managed-service-accounts-overview
  - https://learn.microsoft.com/en-us/powershell/module/activedirectory/new-adserviceaccount
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/delegated-managed-service-accounts/delegated-managed-service-accounts-overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Standalone managed service accounts

## sMSA vs gMSA vs dMSA
| | sMSA | gMSA | dMSA (2025) |
|---|---|---|---|
| Hosts | one computer | many | machine identities mapped in AD; migrates from a user account |
| Needs KDS root key | not stated in the docs | yes | yes |
| Password | managed by the computer | managed by the domain controller, retrieved by hosts | secret held on the domain controller, machine-bound |
| Use for | a single-server service | farms and multi-server services | replacing legacy service users |
Prefer gMSA for new work, even on one server: same management, ready to scale. Create a KDS root key if the domain has none.

## Create and install an sMSA
```powershell
New-ADServiceAccount -Name svc-app01 -RestrictToSingleComputer -Enabled $true
Add-ADComputerServiceAccount -Identity APP01 -ServiceAccount svc-app01
# on APP01 (needs RSAT AD PowerShell)
Install-ADServiceAccount svc-app01
Test-ADServiceAccount svc-app01        # True
```
Then set the service to log on as `AD\svc-app01$` with a blank password (services.msc or
`sc.exe config MySvc obj= "AD\svc-app01$"`).

## Replace a user-account service
1. Inventory: `Get-CimInstance Win32_Service | ? StartName -like 'AD\*' | ft Name,StartName`.
2. Grant the MSA what the user had: file ACLs, SQL logins, and SPNs (move them: `setspn -D`, then `setspn -S` on the MSA).
3. Swap the logon, restart, test, disable the old user after a soak period.

## Gotchas
- Not every app supports MSAs (some need the password typed into the app). Check vendor support.
- An sMSA is limited to one domain-joined server; use a gMSA for a farm or load-balanced service.

## Verify
- [ ] Service runs as the MSA; `Test-ADServiceAccount` True; old user disabled with no logon failures.

## Checked
Checked 2026-10-27 against Microsoft Learn (gMSA overview and manage articles 07/2025; delegated MSA overview and setup 05/2025; New-ADServiceAccount, Add-ADComputerServiceAccount, Install-ADServiceAccount references; sc config).
- Confirmed: -RestrictToSingleComputer; Add-ADComputerServiceAccount, Install-ADServiceAccount and Test-ADServiceAccount; sMSA is limited to one domain-joined server and was introduced in Windows Server 2008 R2; dMSA is a Windows Server 2025 feature that needs a KDS root key, migrates from existing service accounts (not from MSAs or gMSAs); sc.exe config obj= sets the logon account; Win32_Service exposes StartName.
- Removed: 240-character and 30-day password figures and the KDS-free sMSA claim as stated facts; the Log on as a service remark.

Method: documentation only; no commands were run.
