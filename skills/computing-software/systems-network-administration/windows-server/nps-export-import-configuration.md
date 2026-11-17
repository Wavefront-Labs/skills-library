---
id: computing-software.systems-network-administration.windows-server.nps-export-import-configuration
name: nps-export-import-configuration
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, nps, export-npsconfiguration, import-npsconfiguration, radius, backup]
level: practitioner
status: docs-checked
description: "Back up and replicate NPS settings with Export-NpsConfiguration and Import-NpsConfiguration (or netsh nps), keeping RADIUS clients, policies and secrets in sync."
sources:
  - https://learn.microsoft.com/en-us/windows-server/networking/technologies/nps/nps-manage-export
  - https://learn.microsoft.com/en-us/windows-server/networking/technologies/nps/nps-best-practices
  - https://learn.microsoft.com/en-us/windows-server/networking/technologies/nps/nps-manage-register
  - https://learn.microsoft.com/en-us/powershell/module/nps/export-npsconfiguration
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Export and import NPS configuration

Microsoft documents exporting the whole NPS configuration (RADIUS clients and servers, network policy, connection request
policy, registry and logging configuration) from one NPS for import on another.

## Export
```powershell
Export-NpsConfiguration -Path '<SHARE>\nps\nps-primary.xml'
```
```cmd
netsh nps export filename="<SHARE>\nps\nps-primary.xml" exportPSK=YES
```
`netsh nps export` requires `exportPSK=YES` to acknowledge that shared secrets are written to the file. The XML is not
encrypted: move it over the network inside an encrypted archive and store it in a secure location.

## Import on secondary
```powershell
Import-NpsConfiguration -Path '<SHARE>\nps\nps-primary.xml'
```
```cmd
netsh nps import filename="<SHARE>\nps\nps-primary.xml"
```
Import overwrites the existing configuration; you cannot add settings to it by importing. Do not import when the source NPS
database version is higher than the destination's (see `netsh nps show config`).

## What does not move
- SQL Server logging settings are not exported; configure SQL Server logging manually on the destination.
- Registering NPS in AD (membership of the RAS and IAS Servers group) is per server: `netsh nps add registeredserver <domain> <server>`.

## Verify
- [ ] `Get-NpsRadiusClient` lists the same clients on both servers after import.
- [ ] A test authentication succeeds against each NPS server.

## Checked

2026-10-25, against the MicrosoftDocs/windowsserverdocs repository (main, last commit 2026-10-23), the windows-powershell-docs NPS cmdlet pages and the MicrosoftDocs/entra-docs repository. Confirmed what is exported, Export-NpsConfiguration -Path, netsh nps export with exportPSK=YES, unencrypted XML, that import overwrites the configuration, the database-version restriction, that SQL Server logging settings are not exported, and netsh nps add registeredserver. Removed the unconfirmed claims about clustering, scheduled automation, certificate handling and SQL connection strings.

Method: documentation only; no commands were run.
