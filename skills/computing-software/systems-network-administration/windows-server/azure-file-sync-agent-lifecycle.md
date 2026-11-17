---
id: computing-software.systems-network-administration.windows-server.azure-file-sync-agent-lifecycle
name: azure-file-sync-agent-lifecycle
category: computing-software
field: systems-network-administration
product: windows-server
tags: [azure-file-sync, afs-agent, server-endpoint, servicing, storage-sync-service]
level: practitioner
status: docs-checked
description: "Install, register, update and retire the Azure File Sync agent: supported Windows Server versions, expiry rules, auto-update policy, rebuilds and why cloning is unsupported."
sources:
  - https://learn.microsoft.com/en-us/azure/storage/file-sync/file-sync-server-registration
  - https://learn.microsoft.com/en-us/azure/storage/file-sync/file-sync-release-notes
  - https://learn.microsoft.com/en-us/azure/storage/file-sync/file-sync-planning
  - https://learn.microsoft.com/en-us/troubleshoot/azure/azure-storage/files/file-sync/file-sync-troubleshoot-server-cloning
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Azure File Sync agent lifecycle

## Install and register
1. Prereqs: Windows Server 2016, 2019, 2022 or 2025 (Full or Core); .NET Framework 4.7.2 or later (included from
   2019; verify it on 2016); outbound 443. Disable IE Enhanced Security Configuration only for the registration
   sign-in, then re-enable.
2. Install the MSI. Leave Microsoft Update enabled in the installer: agent feature updates and hotfixes arrive
   through it. The wizard launches `ServerRegistration.exe` (in the agent install folder) to register the server
   with a Storage Sync Service. A server registers to only one Storage Sync Service.
```powershell
Register-AzStorageSyncServer -ResourceGroupName rg-files -StorageSyncServiceName sss-corp
```

## Updates and expiry
- Update paths: the automatic update feature, Microsoft Update, `AfsUpdater.exe` in the agent folder, an .msp patch
  from the Microsoft Update Catalog, or the newest installer. Downgrading the agent is not supported.
- Major versions are supported for at least 12 months, with at least 3 months overlap between majors; warnings start
  at least 3 months before expiry; minor versions expire with their major (18.x.x.x expire together).
- Installing an expired version shows a warning and succeeds, but connecting with it is blocked.
- Check the release notes for the live table. On 2026-10-27 it listed v20.0 and v20.1 expiring on 29 Oct 2026 and v18
  and v19 already expired (19 June 2026).
- Auto-update policy (on the server, after importing `StorageSync.Management.ServerCmdlets.dll` from the agent folder):
```powershell
Get-StorageSyncAgentAutoUpdatePolicy
Set-StorageSyncAgentAutoUpdatePolicy -PolicyMode UpdateBeforeExpiration
Set-StorageSyncAgentAutoUpdatePolicy -PolicyMode InstallLatest -Day <day> -Hour <hour>
```
  `UpdateBeforeExpiration` (default) attempts one self-update a week in the maintenance window during the 21 days
  before expiry. `InstallLatest` updates as soon as a version has finished flighting and does not apply to clustered
  servers. Neither replaces regular Microsoft Update patching.

## Rebuilding a server
- Same server, new OS install: remove the server endpoints, unregister the old registration, reinstall the agent,
  register, recreate server endpoints. Unregistering deletes all server endpoints on that server, so recall tiered
  data first if the local copy matters.
- Never clone, image or restore an OS backup or checkpoint of a registered server: it duplicates the server identity
  and is unsupported. Sysprep after the agent is installed is also unsupported; install and register the agent after
  the image is deployed and mini-setup has finished. If a clone already exists, shut it down and follow the
  cloning troubleshooting page.

## Retire
Remove server endpoints first (recall tiered files if they are still needed), then unregister the server
(`Unregister-AzStorageSyncServer` or portal "Unregister server").

## Verify
- [ ] Portal Registered servers shows the server online, with a supported agent version and no expiry warning.
- [ ] Agent version is checked against the release notes table after every major release.

## Checked
Date 2026-10-27. Documentation: Azure File Sync release notes (v23.1 listed as newest), planning guide (supported
Windows Server versions, sysprep), agent update policy include, server registration and cloning troubleshooting
pages. Confirmed: supported OS list (no 2012 R2), .NET 4.7.2, expiry rules, auto-update cmdlets and 21-day window,
unregister cascade, clone and sysprep restrictions.
Method: documentation only; no commands were run.
