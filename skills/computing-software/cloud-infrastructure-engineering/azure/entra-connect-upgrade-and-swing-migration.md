---
id: computing-software.cloud-infrastructure-engineering.azure.entra-connect-upgrade-and-swing-migration
name: entra-connect-upgrade-and-swing-migration
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, entra-connect, connect-upgrade, swing-migration, connect-auto-upgrade, staging-mode, hybrid-identity]
level: advanced
status: docs-checked
description: "Keep Entra Connect Sync supported: auto-upgrade, in-place upgrade, and a swing migration to a new server via staging mode and exported settings."
sources: ["https://learn.microsoft.com/en-us/entra/identity/hybrid/connect/how-to-upgrade-previous-version", "https://learn.microsoft.com/en-us/entra/identity/hybrid/connect/how-to-connect-install-automatic-upgrade", "https://learn.microsoft.com/en-us/entra/identity/hybrid/connect/how-to-connect-import-export-config"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Entra Connect upgrade and swing migration

**Goal:** stay on a supported Connect version without a sync outage. Connect follows the Modern Lifecycle Policy: you must take the latest update to remain supported.

## Check version and auto-upgrade
```powershell
Get-ADSyncAutoUpgrade                 # Enabled / Disabled / Suspended
Get-ADSyncAutoUpgrade -Detail         # reason when Suspended
```
- Auto-upgrade is on by default for Express-settings installs and DirSync upgrades (SQL Express LocalDB, default `MSOL_` account).
  A non-LocalDB database or a non-Express install makes it ineligible (`Suspended`, set by the system only).
  Custom sync rules stopped blocking it after version 2.2.1.0.
- You can switch between Enabled and Disabled with `Set-ADSyncAutoUpgrade`. Upgrade is also held while the
  Synchronization Service Manager UI is open.
- Reasons are logged in the Application event log, source Microsoft Entra Connect Upgrade, event IDs 300-399.

## In-place upgrade (simple installs)
1. Export config first (wizard > View or export current configuration).
2. Run the new installer and watch Synchronization Service Manager for export errors before declaring done.
- In-place upgrades of DirSync or ADSync are not supported; use a swing migration.

## Swing migration (Microsoft recommends it for substantial configuration changes or upgrades from older 1.x versions)
1. On the active server, export settings: wizard > *View or export current configuration* (JSON).
2. Build a new server; install Connect choosing *Customize* > *Import synchronization settings* with that JSON (exported files must not be hand-edited; import is not supported with the G-SQL or G-LDAP connector or an existing sync database). Finish with
   **staging mode** enabled. Provide directory credentials again; the SQL/service account overrides on the page are not imported.
3. Let the staging server run full import and full synchronization, and review its pending exports against expectations. Pending deletes = stop and investigate.
4. Cutover: switch the **old** server to staging mode, then promote the new one to active (never two active servers).
5. Upgrade the old server while it is in staging, keep it as a spare, or decommission it.

## Gotchas
- Custom configuration on the active server must be moved to the staging server if the import did not carry it.
- Customers who have not upgraded in 12-18 months should prefer a swing upgrade.
- The staging server holds pending exports instead of exporting; they are your diff, not errors.

## Verify
- [ ] Entra admin center > Entra Connect shows the new server version and recent sync time.
- [ ] A test user change appears in the cloud within one sync cycle.

## Checked
2026-10-28. Confirmed on Microsoft Learn (upgrade from a previous version, automatic upgrade, import and export configuration pages): Modern Lifecycle Policy, `Get-ADSyncAutoUpgrade` states and `-Detail`, Express/LocalDB eligibility, custom rules no longer blocking after 2.2.1.0, event log source and ID range, swing migration recommendation and promote/demote sequence, import settings flow and its limits, 12-18 month guidance. Removed: server OS/.NET/TLS prerequisites, version-file one-liner, csexport procedure, password hash sync, Seamless SSO and Connect Health claims.
Method: documentation only; no commands were run.
