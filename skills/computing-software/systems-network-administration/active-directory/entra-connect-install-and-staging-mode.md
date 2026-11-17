---
id: computing-software.systems-network-administration.active-directory.entra-connect-install-and-staging-mode
name: entra-connect-install-and-staging-mode
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, entra-connect, entra-connect-sync, entra-connect-install, staging-mode, ou-filtering, adsync, hybrid-identity, tier-0, upn-suffix]
level: practitioner
status: docs-checked
description: "Install Entra Connect Sync with custom settings: prep UPN suffixes, OU filtering, a staging-mode second server for upgrades/DR, and treating the box as Tier 0."
sources:
  - https://learn.microsoft.com/en-us/entra/identity/hybrid/connect/how-to-connect-install-custom
  - https://learn.microsoft.com/en-us/entra/identity/hybrid/connect/how-to-connect-sync-staging-server
  - https://learn.microsoft.com/en-us/entra/identity/hybrid/connect/how-to-connect-install-prerequisites
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Install Entra Connect Sync (custom) and use staging mode

> Microsoft's prerequisites page carries a mandatory-upgrade notice: upgrade Entra Connect Sync to 2.6.84.0 or later and
> configure application-based authentication by 2027-04-07, or synchronization stops. Download the .msi from the Entra
> admin center, and meet .NET Framework 4.7.2 and TLS 1.2.

## Before installing
1. **UPN suffixes:** users' on-premises UPN should be a routable domain you verify in Entra. If AD uses
   `ad.example.local`, add a routable suffix (`Get-ADForest | Set-ADForest -UPNSuffixes @{Add='example.com'}`) and update
   user UPNs.
2. **Clean data:** run IdFix to find duplicates and formatting problems before syncing.
3. **Server:** domain-joined Windows Server (Microsoft recommends 2025 or 2022; older versions need paid extended support).
   Connect uses TLS 1.2 to Entra. Do not use a read-only DC: the DC Connect talks to must be writable. Treat the server
   as Tier 0 (it holds credentials that can read hashes or set passwords with writeback); administer it from PAWs.

## Custom install highlights
- Sign-in method: password hash sync, pass-through authentication or federation (see the hybrid authentication skill).
- Connect directories: let the wizard create the AD DS account, or supply a pre-created one (the ADSyncConfig
  `Set-ADSync*Permissions` cmdlets, see the connector account skill).
- **Domain/OU filtering:** sync only OUs with real users, groups and devices.
- Source anchor: the wizard can let Entra pick; it uses `ms-DS-ConsistencyGuid` for users when the attribute is unused.
  It can only be set at first installation and a second server must use the same attribute.
- Optional features: password writeback, group writeback, directory extension sync, app and attribute filtering.

## Staging mode
A server installed with **staging mode** imports and synchronizes but exports nothing to Entra or AD; password sync and
password writeback are disabled in staging mode. Only one server may export to a tenant.
- **DR:** if the active server is lost, run the wizard on the standby > **Configure staging mode** and clear the option.
  Ensure only one server is syncing at any time, and keep a failed active server from rejoining unexpectedly.
- **Changes and upgrades:** apply the change on the staging server, inspect what would be exported, then swap roles.
  From a command prompt in `%ProgramFiles%\Microsoft Azure AD Sync\bin`:
```cmd
csexport "<Connector name>" %temp%\export.xml /f:x
CSExportAnalyzer %temp%\export.xml > %temp%\export.csv
```
The staging page also provides a CSAnalyzer PowerShell script for large exports.

## Verify
- [ ] `Get-ADSyncScheduler` shows `StagingModeEnabled` False on the active server and True on the standby.
- [ ] Entra portal shows sync healthy and the expected object counts.

## Checked
Checked 2026-10-27 against Microsoft Learn (entra-docs): Connect prerequisites (with the mandatory upgrade notice), custom
installation, staging server and disaster recovery, source anchor design concepts and scheduler pages. Confirmed IdFix,
TLS 1.2, writable DC, staging-mode behaviour, `csexport` and `CSExportAnalyzer` usage and the source-anchor rules.
Replaced "Windows Server 2019+" with the current OS guidance and removed the unsourced "enable staging mode" phrasing
details.
Method: documentation only; no commands were run.
