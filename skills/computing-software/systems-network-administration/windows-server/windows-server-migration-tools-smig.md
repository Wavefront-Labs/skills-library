---
id: computing-software.systems-network-administration.windows-server.windows-server-migration-tools-smig
name: windows-server-migration-tools-smig
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, workload-migration, windows-server-migration-tools, smig, export-smigserversetting, role-migration]
level: advanced
status: draft
description: "Migrate roles and settings (local users and groups, DHCP, IP config, file shares) between servers with Windows Server Migration Tools Export/Import-SmigServerSetting."
sources:
  - https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2012-r2-and-2012/jj134202(v=ws.11)
  - https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2012-r2-and-2012/dn486809(v=ws.11)
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Windows Server Migration Tools (SMIG)

A feature that exports settings from a source server and imports them on a destination. Older but still useful
for local users/groups and role configurations where no better tool exists. (File data moves better with SMS or
robocopy.)

## Install
Destination:
```powershell
Install-WindowsFeature Migration
```
Create the deployment folder for the source OS and copy it to the source:
```cmd
"%windir%\System32\ServerMigrationTools\SmigDeploy.exe" /package /architecture amd64 /os WS16 /path <SHARE>\smig
```
On the source, run `SmigDeploy.exe` from that folder to register the cmdlets, then in PowerShell
`Add-PSSnapin Microsoft.Windows.ServerManager.Migration`.

## Export and import
```powershell
# source
Get-SmigServerFeature
Export-SmigServerSetting -User All -Group -Path <SHARE>\smig-store -Verbose
Export-SmigServerSetting -FeatureID DHCP -Path <SHARE>\smig-dhcp
# destination
Import-SmigServerSetting -User All -Group -Path <SHARE>\smig-store -Verbose
Import-SmigServerSetting -FeatureID DHCP -Path <SHARE>\smig-dhcp -Force
```
Both prompt for a password protecting the store. `Send-SmigServerData`/`Receive-SmigServerData` move file data and
shares with permissions between the two servers directly.

## Gotchas
- Supported OS combinations are limited; check the matrix (newer source than destination is not supported).
- DHCP migration is usually easier with `Export-DhcpServer`/`Import-DhcpServer` (see dhcp-backup-and-migration).
- Local user passwords migrate only if specified; otherwise accounts are disabled or get a temporary password.

## Verify
- [ ] Imported users/groups and role settings match the source export log; services start on the destination.
