---
id: computing-software.it-support-helpdesk.desktop-support.user-profile-shell-and-start-menu-repair
name: user-profile-shell-and-start-menu-repair
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, profile-cleanup, roaming-profiles-folder-redirection, shell-folders, start-menu-search, appx-reregister, delprof]
level: practitioner
status: draft
description: "Fix per-user Windows profile problems: profile cleanup, roaming profiles and folder redirection, broken shell folder paths, dead Start menu or search, AppX re-registration."
sources:
  - "https://learn.microsoft.com/en-us/windows-server/storage/folder-redirection/folder-redirection-rup-overview"
  - "https://learn.microsoft.com/en-us/troubleshoot/windows-client/shell-experience/troubleshoot-start-menu-errors"
  - "https://learn.microsoft.com/en-us/powershell/module/appx/add-appxpackage"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# user-profile-shell-and-start-menu-repair

## Profile disk usage cleanup
- Shared PCs collect dozens of profiles. Remove stale ones properly (System Properties
  > Advanced > User Profiles > Delete, or `Get-CimInstance Win32_UserProfile | Where
  {$_.LastUseTime -lt (Get-Date).AddDays(-90) -and -not $_.Special -and -not $_.Loaded} |
  Remove-CimInstance`). GPO "Delete user profiles older than N days" automates it.
- Large single profiles: OneDrive offline files, Teams/Outlook caches (OST), Downloads,
  browser caches. Use Storage Sense or WinDirStat-type tools to find the bulk.
- Never delete `%SystemDrive%\Users\<name>` folders by hand; the ProfileList entry remains and the
  user gets a temporary profile.

## Roaming profiles and folder redirection
- **Roaming profiles** copy the whole profile to/from a share at logon/logoff; slow,
  conflict-prone, and version-specific (`.V6` suffix). Replaced in most estates by
  FSLogix (VDI) or OneDrive KFM (physical).
- **Folder redirection** (GPO: User Configuration > Policies > Windows Settings >
  Folder Redirection) points Documents/Desktop to a share. Common faults: share
  permissions wrong (users need create-folder on the root, owner rights on their
  folder), offline files sync conflicts, slow logon over VPN.
- Migrating to KFM: turn off redirection with "redirect back to local profile", then
  enable KFM; doing both at once confuses OneDrive.

## Broken shell folder paths
- Symptom: Desktop or Documents points to a missing share or an old OneDrive path;
  "location is not available".
- Check `HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders`
  (expandable values like `%USERPROFILE%\Documents`). Restore defaults via the folder's
  Properties > Location > **Restore Default**, or fix the registry and sign out/in.

## Start menu or search not working
1. Restart Explorer and the `StartMenuExperienceHost` / `SearchHost` processes.
2. Check Windows Search service; rebuild the index (Indexing Options > Advanced >
   Rebuild).
3. Run `sfc /scannow` and `DISM /Online /Cleanup-Image /RestoreHealth`.
4. Test with a new local user: if Start works there, it's profile-specific.
5. Re-register built-in apps for the current user:
```powershell
Get-AppxPackage Microsoft.Windows.StartMenuExperienceHost, Microsoft.Windows.ShellExperienceHost, MicrosoftWindows.Client.CBS |
  ForEach-Object { Add-AppxPackage -DisableDevelopmentMode -Register "$($_.InstallLocation)\AppxManifest.xml" }
```
- Re-registering **all** packages for all users is a blunt tool that can break Store
  apps; target the broken package.
- Last resort: new profile with data migration.

## Verify
Profiles older than the policy are gone with no orphaned ProfileList keys; shell folders
point to valid paths; Start and search open and find apps for the affected user.
