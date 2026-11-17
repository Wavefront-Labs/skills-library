---
id: computing-software.it-support-helpdesk.desktop-support.disk-cleanup-and-storage-sense
name: disk-cleanup-and-storage-sense
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, disk-cleanup, storage-sense, cleanmgr, low-disk-space, windows]
level: practitioner
status: docs-checked
description: "Free disk space on Windows safely: Storage Sense policies, Disk Cleanup with system files, component store cleanup, finding big folders, and what never to delete."
sources:
  - "https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/cleanmgr"
  - "https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/clean-up-the-winsxs-folder"
  - "https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-storage"
  - "https://support.microsoft.com/en-us/windows/experience/storage-filemanagement/manage-drive-space-with-storage-sense"
  - "https://support.microsoft.com/en-us/windows/deployment/install-upgrade/delete-your-previous-version-of-windows"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Disk Cleanup and Storage Sense

**Symptom:** "low disk space" warnings, updates failing, profile not loading, slow PC on a nearly full drive.

## Quick assessment
- Settings > System > Storage shows categories (apps, temporary files, other).
- Find large folders with a disk-usage tool or PowerShell:
  `Get-ChildItem $env:USERPROFILE -Directory | % { [pscustomobject]@{Name=$_.Name; GB=[math]::Round((gci $_.FullName -Recurse -File -EA 0 | measure Length -Sum).Sum/1GB,2)} } | sort GB -desc`

## Storage Sense
Settings > System > Storage > Storage Sense. Off by default; if a PC runs low
on space Windows may turn it on to manage selected temporary files. With the
defaults it runs when space is low and cleans temporary files; the Recycle Bin
is cleaned after a set time; the Downloads folder and cloud content are not
touched unless you configure them. From Windows 11 22H2 the default for
OneDrive files is to become online-only if not opened for 30 days.
Manage centrally with the Storage policy CSP (Intune Settings Catalog), for
example `AllowStorageSenseGlobal`, `ConfigStorageSenseRecycleBinCleanupThreshold`
and `ConfigStorageSenseCloudContentDehydrationThreshold`.

## Disk Cleanup (cleanmgr)
- Run `cleanmgr`, choose the drive, then **Clean up system files** for items
  such as Windows Update cleanup and the previous Windows installation.
- Scripted: `cleanmgr /sageset:1` (choose categories once), then
  `cleanmgr /sagerun:1`. `/sagerun` runs the chosen tasks against every drive.
- Ten days after an upgrade the previous Windows version is deleted
  automatically. Deleting it sooner removes the option to go back and cannot
  be undone, so confirm the user does not need it first.

## Component store
`Dism /Online /Cleanup-Image /StartComponentCleanup` is the supported way to
clean up superseded components (the scheduled task waits at least 30 days
after an update before removing the previous version). Do not delete files
from WinSxS by hand.

## Other big consumers
- Old user profiles: remove through System Properties > User Profiles, never
  by deleting folders.
- Cloud-synced folders: use the sync client's free-up-space option.

## Verify
Free space has increased, Windows Update installs, and the Storage Sense
policy shows applied in your management console.


## Checked

Date 2026-10-27. Documentation release: Microsoft Learn cleanmgr, WinSxS clean-up and Storage policy CSP pages, Microsoft Support Storage Sense and delete-previous-Windows pages, as published October 2026 (Windows 10/11). Confirmed: cleanmgr /sageset and /sagerun behaviour, Storage Sense defaults, Windows 11 22H2 30-day OneDrive default, the three CSP setting names, 10-day removal of the previous Windows version and the cannot-go-back warning, StartComponentCleanup and its 30-day wait. Removed: powercfg hibernation advice, Outlook OST and free-space percentage guidance, the AnalyzeComponentStore step, and the never-delete list that no page covers.

Method: documentation only; no commands were run.
