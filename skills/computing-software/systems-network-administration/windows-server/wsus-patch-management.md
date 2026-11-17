---
id: computing-software.systems-network-administration.windows-server.wsus-patch-management
name: wsus-patch-management
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, wsus, windows-server-update-services, updatesservices-module, susdb, windows-internal-database, wid, wsuspool, iis, wsusutil, postinstall, computer-groups, client-side-targeting, auto-approval-rules, superseded-updates, decline-updates, server-cleanup-wizard, invoke-wsusservercleanup, get-windowsupdatelog, usoclient, windows-update, group-policy, patching, upstream-downstream, replica, configmgr, deprecation]
level: practitioner
status: docs-checked
description: "Run WSUS without it rotting: WID vs SQL, products/classifications, client-side targeting groups by GPO, approval rules, declining superseded updates, cleanup, WsusPool and SUSDB upkeep, client logs."
sources:
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-server-update-services/get-started/windows-server-update-services-wsus
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-server-update-services/deploy/1-install-the-wsus-server-role
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-server-update-services/deploy/deploy-windows-server-update-services
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-server-update-services/manage/running-wsus-replica-mode
  - https://learn.microsoft.com/en-us/troubleshoot/mem/configmgr/update-management/wsus-maintenance-guide
  - https://learn.microsoft.com/en-us/powershell/module/updateservices/invoke-wsusservercleanup
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WSUS patch management: approve on purpose, decline aggressively, keep the DB small

**Goal:** operate WSUS as the update source for Windows servers and clients: targeted
groups, deliberate approvals, and the maintenance that stops WSUS from timing out.
Ring design, cadence and risk prioritisation are tool-agnostic and live in
`computing-software.systems-network-administration.patch-management.patch-cycle-and-maintenance-windows`.

**Status note:** Microsoft documents WSUS as deprecated and no longer adding new features, but still supported for
production deployments and receiving security and quality updates per the product lifecycle. Check the current support
position before building new WSUS infrastructure.

## 1. Install
```powershell
Install-WindowsFeature -Name UpdateServices -IncludeManagementTools
```
Then run the post-installation configuration and the WSUS Configuration Wizard as described in the install and configure
articles. Choose the database deliberately: Windows Internal Database (WID) is the simple default; a shared SUSDB design
needs SQL Server (WID is not supported for it).
- Downstream servers: a **replica** server inherits update approvals and computer groups from the administration server and
  allows only limited administration; an **autonomous** server is administered locally.
- WSUS needs two ports: HTTPS for metadata, by default 8531, and HTTP for content, by default 8530. If you change them they
  must be adjacent numbers, with the HTTP port exactly one less than the HTTPS port.

## 2. Sync only what you run
Select only the products and classifications you actually deploy (`Set-WsusProduct`, `Set-WsusClassification`,
`Get-WsusProduct`, `Get-WsusClassification`). Every extra product increases the size of the update catalogue that SUSDB
and clients process.

## 3. Groups by GPO (client-side targeting)
In the WSUS options choose *Use Group Policy or registry settings* for computer membership; create the computer groups in the
WSUS console first. Then set the Windows Update policies (Computer Configuration > Administrative Templates > Windows
Components > Windows Update):
- *Specify intranet Microsoft update service location*: use the HTTPS port in the URL (for example `https://wsus01:8531`).
- *Enable client-side targeting*: the target group name; it is ignored until a group with that name exists in WSUS, and it only
  works when the intranet update service location policy is enabled.
Clients using client-side targeting appear in All Computers and in the group you selected.

## 4. Approvals
- Approve to **pilot groups first** (`Approve-WsusUpdate`), then widen after the soak period.
- **Decline superseded and expired updates** (`Deny-WsusUpdate`, or the cleanup switches below): leaving expired definition
  updates undeclined is a documented cause of very long client update scans.
- A replica server cannot decline updates or run cleanup; do it on the administration server.

## 5. Maintenance
```powershell
Invoke-WsusServerCleanup -CleanupObsoleteComputers -CleanupObsoleteUpdates `
  -CleanupUnneededContentFiles -CompressUpdates -DeclineExpiredUpdates -DeclineSupersededUpdates
```
- If you have never run the cleanup, the unused updates and update revisions option may need a few passes and can time
  out; rerun it until it completes, then run each other option one at a time.
- Back up SUSDB, then re-index it (Microsoft publishes a re-index T-SQL script). Where SUSDB runs (SQL Server or WID) is
  shown by the `SQLServerName` registry value of WSUS; for WID on Windows Server 2012 or later connect to
  `\\.\pipe\MICROSOFT##WID\tsql\query`, running the management tool as administrator. Scheduled re-indexing
  needs full SQL Server or a SQLCMD scheduled task for WID.

## 6. Verify
- [ ] Only deployed products and classifications sync.
- [ ] Clients land in the GPO-defined groups and report.
- [ ] Pilot group gets approvals before production.
- [ ] Expired and superseded updates are declined and the cleanup completes without timeout.
- [ ] SUSDB is backed up and re-indexed.

## Checked

Checked 2026-10-26 against learn.microsoft.com / MicrosoftDocs/windowsserverdocs, windows-powershell-docs and SupportArticles-docs main branches, last commits 2026-10-23. Confirmed: the deprecation statement (deprecated, no new features, still supported), Install-WindowsFeature UpdateServices, replica versus autonomous server behaviour, the 8530 and 8531 port defaults and the adjacent-port rule, WID not supported for the shared SUSDB design, the client-side targeting and Specify intranet Microsoft update service location policies (HTTPS port in the URL, target group ignored until created), Invoke-WsusServerCleanup switches, the cleanup multi-pass and one-option-at-a-time guidance, the WID named pipe path for Windows Server 2012 and later, SUSDB re-index guidance, and the expired definition updates cause of slow scans. Removed as unconfirmed: the 2024 date of the deprecation announcement, wsusutil postinstall options, the UpdateServices-DB feature, express installation and driver classification advice, the classification list, auto-approval rule advice, WsusPool memory and queue settings and the associated error codes, HTTP spoofing remark, and the client troubleshooting commands (Get-WindowsUpdateLog, UsoClient, SusClientId), whose behaviour is not covered by the public documentation read.

Method: documentation only; no commands were run.
