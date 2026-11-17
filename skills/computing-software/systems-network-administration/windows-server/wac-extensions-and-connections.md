---
id: computing-software.systems-network-administration.windows-server.wac-extensions-and-connections
name: wac-extensions-and-connections
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, windows-admin-center, wac, wac-extensions, wac-connections, extension-feed, tags, shared-connections, import-connections, offline-feed]
level: intro
status: docs-checked
description: "Manage Windows Admin Center extensions and connections: approved feeds, offline feeds, shared connection lists with tags, bulk import from CSV and credential handling."
sources:
  - https://learn.microsoft.com/en-us/windows-server/manage/windows-admin-center/configure/using-extensions
  - https://learn.microsoft.com/en-us/windows-server/manage/windows-admin-center/configure/use-powershell
  - https://learn.microsoft.com/en-us/windows-server/manage/windows-admin-center/configure/shared-connections
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WAC extensions and connections

## Extensions
Settings > Extensions shows Available/Installed from configured **feeds** (the Microsoft official NuGet feed by default,
which hosts Microsoft and other developers' extensions). You can add any NuGet V2 feed or a file share.
- Extensions run code in the gateway and on targets, so approve them like software.
- Disconnected networks: download the `.nupkg` files on a connected machine, put them on a file share and add it as a
  feed. Packages on a file share must be signed unless the operation mode is Development.
- Not every extension works on the modernized gateway (2410+); check the known issues page before upgrading.

## Connections
- Add individually: All connections > Add > Servers / Windows PCs / Server clusters / Azure VMs.
- **Bulk import** with the PowerShell module on the gateway (modernized gateway module shown; the access key is on
  the Advanced tab of WAC settings and is required for import, not export):
```powershell
Import-Module "$env:ProgramFiles\WindowsAdminCenter\PowerShellModules\Microsoft.WindowsAdminCenter.ConnectionTools"
Export-WACConnection "https://wac.ad.example.com" -fileName "WAC-connections.csv"
Import-WACConnection "https://wac.ad.example.com" -fileName "WAC-connections.csv" -AccessKey "<key string>"   # -prune removes connections not in the file
```
- CSV columns: `name` (FQDN), `type` (`msft.sme.connection-type.server` or `msft.sme.connection-type.cluster`), `tags`
  (pipe-separated) and `groupId` (`global` makes a shared connection). The CSV is case-sensitive.
- **Tags** (e.g. `prod`, `sql`, `site-lon`) let you filter and group.
- Shared connections can be changed only by gateway administrators; any user can change their own list.

## Credentials
Use **Manage as** when the passed-through Windows credential lacks admin rights on the target. Prefer
SSO via Kerberos delegation (see the Kerberos delegation skill) to avoid entering admin credentials.

## Verify
- [ ] Imported list shows all servers with tags; status "Online".
- [ ] Only approved extensions are installed (Settings > Extensions > Installed).

## Checked
Checked 2026-10-26 against Microsoft windowsserverdocs main, Windows Admin Center pages (ms.date 2025 for access, install, certificate, HA and troubleshooting; WAC 2410+ modernized gateway).
Confirmed from configure/using-extensions (feeds, NuGet V2 or file share, signed packages, offline .nupkg download), known-issues (extensions not working on 2410), includes/ps-connections (ms.date 2025-12-29:
module path, Export-/Import-WACConnection, -AccessKey, -prune, CSV columns and connection type strings, global shared connections) and configure/shared-connections.
Replaced the legacy Import-Connection/Export-Connection example and the three-column CSV with the documented cmdlets; removed the partner-vendor list and the remember-credentials claim.
Method: documentation only; no commands were run.
