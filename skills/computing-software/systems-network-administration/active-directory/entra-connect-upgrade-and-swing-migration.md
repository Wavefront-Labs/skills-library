---
id: computing-software.systems-network-administration.active-directory.entra-connect-upgrade-and-swing-migration
name: entra-connect-upgrade-and-swing-migration
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, entra-connect, entra-connect-upgrade, entra-connect-swing-migration, staging-mode]
level: advanced
status: docs-checked
description: "Upgrade Entra Connect in place or by swing migration to a new server in staging mode, export and import config, compare and switch active roles."
sources:
  - https://learn.microsoft.com/en-us/entra/identity/hybrid/connect/how-to-upgrade-previous-version
  - https://learn.microsoft.com/en-us/entra/identity/hybrid/connect/how-to-connect-import-export-config
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Entra Connect upgrade and swing migration

> Mandatory upgrade notice (Microsoft prerequisites page): upgrade Entra Connect Sync to 2.6.84.0 or later and configure
> application-based authentication by 2027-04-07; after that date synchronization stops if these are not met. The .msi is
> available only from the Entra admin center; requirements include .NET Framework 4.7.2 and TLS 1.2.

Versions older than Connect V2 are deprecated. You can upgrade from any version to the current one.

## Choose a method
| Method | Use for |
|---|---|
| Automatic upgrade | express installs; on by default for express installs, may lag the latest release |
| In-place upgrade | one server, fewer than about 100,000 objects, no major change; a full import and sync follows if out-of-box rules changed |
| Swing migration | recommended for large tenants, substantial configuration changes, and Windows OS upgrades; sync is not interrupted |

Check automatic upgrade with `Get-ADSyncAutoUpgrade` (states Enabled, Disabled, or Suspended; Suspended is set by the system
only). Change between Enabled and Disabled with `Set-ADSyncAutoUpgrade`. An in-place OS upgrade is not recommended:
build a new server and swing.

## Swing migration
1. On the current server: Connect wizard > **View or Export Current Configuration** > export. Settings also auto-export
   to `%ProgramData%\AADConnect` as `Applied-SynchronizationPolicy-*.JSON` when changed by the wizard; changes made with
   PowerShell, Synchronization Service Manager or the Rules Editor must be exported on demand.
2. Build the new server (Microsoft recommends Windows Server 2025 or 2022), install the new Connect version, choose
   **Customize** > **Import synchronization settings** and select the JSON file, and enable **staging mode**.
3. Reapply what the export does not carry. Documented gaps: device writeback, synchronized object-type and selected
   attribute constraints made in Synchronization Service Manager (including directory extension attributes), custom run
   profiles, provisioning hierarchy, and federation parameters. Custom rule precedence must be in 0 to 99. SQL Server
   choice and service account are not imported. Credentials for each AD forest are requested again.
4. Let staging run a full import and sync, then compare what would be exported:
```cmd
"%ProgramFiles%\Microsoft Azure AD Sync\bin\csexport.exe" "<Connector name>" %temp%\export.xml /f:x
CSExportAnalyzer %temp%\export.xml > %temp%\export.csv
```
   The staging server page also provides the CSAnalyzer script; investigate unexpected deletes or updates.
5. Cutover ("switch active server"): put the old server in staging mode (wizard > Configure staging mode), then take the
   new server out of staging mode. Never run two active servers. Password writeback only works on one active server at a
   time.
6. Keep the old server in staging as a rollback until you are confident, then decommission it.
Do not roll back to DirSync or Azure AD Sync once the new Connect server has exported.

## Verify
- [ ] New server: `Get-ADSyncScheduler` shows `StagingModeEnabled` False, cycles succeed.
- [ ] Old server: staging mode on; no exports in its run history after cutover.

## Checked
Checked 2026-10-27 against Microsoft Learn (entra-docs): Connect upgrade, import and export configuration, staging server,
automatic upgrade and prerequisites pages. Confirmed methods, `Get-ADSyncAutoUpgrade` states, the 100,000-object guidance,
import limitations and `csexport` usage. Added the 2027-04-07 mandatory-upgrade notice and the exact list of settings the
export does not carry; removed the unsourced "two weeks rollback" and "reuse connector account and note its password" advice.
Method: documentation only; no commands were run.
