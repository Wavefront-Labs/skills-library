---
id: computing-software.it-support-helpdesk.desktop-support.migrating-user-data-to-a-new-pc
name: migrating-user-data-to-a-new-pc
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, user-data-migration, usmt, pc-refresh, onedrive, scanstate, loadstate]
level: practitioner
status: draft
description: "Move a user to a new PC without losing anything: pre-migration checklist, OneDrive-first approach, USMT scanstate/loadstate for domain PCs, and the handover sign-off."
sources:
  - "https://learn.microsoft.com/en-us/windows/deployment/usmt/usmt-overview"
  - "https://learn.microsoft.com/en-us/windows/deployment/usmt/usmt-scanstate-syntax"
  - "https://learn.microsoft.com/en-us/windows/deployment/usmt/usmt-loadstate-syntax"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# migrating-user-data-to-a-new-pc

## Before the swap (ask, then check)
- Files outside OneDrive: local folders on other drives, `%SystemDrive%` root folders,
  PSTs, scans folder.
- Browser: is Edge/Chrome sync on? If not, export bookmarks and passwords policy-permitting.
- Outlook signatures, Sticky Notes, Teams custom backgrounds, desktop shortcuts.
- Apps with licence keys or local data (accounting, CAD, dongles); printers and mapped
  drives that are not policy-deployed.
- Anything on the old PC running for others (shared folder, scheduled task).

## Modern approach (Entra-joined, OneDrive KFM)
1. Confirm KFM covers Desktop/Documents/Pictures and sync is complete (no pending items).
2. New device via Autopilot; user signs in, OneDrive restores.
3. Copy the small leftovers (signatures, notes) by hand or a script.

## USMT (domain-joined, lots of local data)
```cmd
scanstate \\mig\store\%COMPUTERNAME% /i:migdocs.xml /i:migapp.xml /ue:*\* /ui:CONTOSO\jsmith /o /c /v:13 /l:%TEMP%\scan.log
loadstate \\mig\store\OLDPC01 /i:migdocs.xml /i:migapp.xml /ue:*\* /ui:CONTOSO\jsmith /c /lac /v:13 /l:%TEMP%\load.log
```
- Run both elevated with the same USMT version and XML files.
- `/encrypt /key:` protects the store; `/hardlink` is for same-machine refreshes only.
- Install apps on the new PC before `loadstate` so app settings land.

## Handover
Sit with the user (or call) and check: files present, email and signatures, printers,
browser favourites, key apps open. Keep the old PC untouched for an agreed period (e.g. 14
days) before wiping it.

## Gotchas
- `/ue:*\*` excludes everyone; `/ui:` must then include the user or nothing migrates.
- USMT does not migrate apps, only settings for supported apps.
- Hidden local data (e.g. `AppData\Local` app databases) needs explicit custom XML.

## Verify
User signs off the checklist, the migration log shows no errors, and the old PC is tagged
with its wipe date in the asset register.
