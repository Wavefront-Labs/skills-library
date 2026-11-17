---
id: computing-software.it-support-helpdesk.desktop-support.onedrive-sync-troubleshooting
name: onedrive-sync-troubleshooting
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, microsoft-365, m365-support, onedrive-sync, onedrive-reset, files-on-demand, sharepoint-library-sync, sync-conflicts, invalid-characters, path-length, cloud-storage-sync]
level: practitioner
status: docs-checked
description: "Fix OneDrive and SharePoint sync: invalid names, size and item limits, duplicate-name conflicts, unsupported setups and the OneDrive reset, from Microsoft's support pages."
sources:
  - "https://support.microsoft.com/en-us/office/fix-onedrive-sync-problems-0899b115-05f7-45ec-95b2-e4cc8c4670b2"
  - "https://support.microsoft.com/en-us/office/reset-onedrive-34701e00-bf7b-42db-b960-84905399050c"
  - "https://support.microsoft.com/en-us/office/restrictions-and-limitations-in-onedrive-and-sharepoint-64883a5d-228e-48f5-b3d2-eb39e07630fa"
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# onedrive-sync-troubleshooting

Goal: every file the user cares about is in the cloud and current, and the
sync error goes away without data loss.

## Start from the icon
Microsoft's "Fix OneDrive sync problems" page is a router: pick the icon the
user sees (personal or work/school sync error, processing changes, file
locked, paused, account nearly full or full/locked/frozen, not signed in) and
follow that article. If no OneDrive icon is visible, OneDrive may not be
running (see the startup troubleshooting article). Exceeding Microsoft storage
stops upload, edit and sync of new files. If nothing matches, try
unlinking/relinking the account.

## Names and file types that block sync
- Characters not allowed in file or folder names: `" * : < > ? / \`.
  Leading and trailing spaces are not allowed either. Rename the item (F2 in
  Windows, Return on a Mac). Some organisations do not yet support `#` and `%`;
  a global or SharePoint admin can enable them.
- Names not allowed: `.lock`, `CON`, `PRN`, `AUX`, `NUL`, `COM0`-`COM9`,
  `LPT0`-`LPT9`, `_vti_` (anywhere in the name), `desktop.ini`, and anything
  starting with `~$`.
- Temporary TMP files do not sync. Outlook PST files are supported but sync
  less often than other types; the page links to an article on moving a PST
  out of OneDrive.
- For work or school accounts an admin can block specific file types.

## Limits and unsupported setups
- Maximum file size for upload and download: 250 GB. Use the sync app rather
  than the website for anything over a few GB.
- Recommended maximum: 300,000 items across your cloud storage; performance
  issues can occur above that even if not all items are synced. A public
  preview supports up to 1,000,000 items per sync instance on qualifying
  Windows 11, Windows Server 2025 or macOS devices (8 GB RAM minimum, SSD
  required, Insider program); it does not support VDI.
- A network or mapped drive cannot be the sync location; symbolic links and
  junction points are not supported.
- Running OneDrive with elevated privileges is not supported.
- Authenticated proxies are not supported (error "Your proxy settings require
  authentication", code 0x8004de42).
- Accounts per device: one OneDrive for home account and up to nine work or
  school accounts; on macOS only one business account from the same
  organisation at a time.
- Libraries with Checkout or Validation columns, or Draft Item Security set to
  edit/approve-only, sync read-only (SharePoint) or cannot sync (OneDrive
  libraries show a lock icon). Do not change library settings without the
  library owner's approval.
- Windows: roaming, mandatory and temporary profiles are not supported;
  folders with `SetCaseSensitiveInfo` enabled are not supported. macOS: case-
  sensitive volumes are not supported.
- OneNote notebooks have their own sync mechanism; moving an existing notebook
  into a synced folder without the OneNote app is not supported.

## Conflicts and stuck syncs
- Duplicate-name conflicts arise from uploading many files at once on the web,
  from another PC syncing the same folder, or from offline edits. Rename the
  edited item to something unique and save again.
- "Processing 0KB of xMB" for a long time may mean too many files; check the
  local folder's Properties for the file count, pause and resume sync, or
  choose which folders to sync. Files On-Demand reduces local disk use.

## Reset
Resetting disconnects all sync connections (personal and work/school) and
then does a full sync; the page states files and data are not lost.
1. Win+R, run `wsreset.exe` (a blank Command Prompt flashes, then the Store
   opens; ignore both).
2. Win+R, run `%localappdata%\Microsoft\OneDrive\onedrive.exe /reset`.
3. If Windows cannot find it, repeat with `onedrive.exe /reset` from the
   `Microsoft OneDrive` folder under Program Files, then under
   Program Files (x86). If none work, the sync app is not installed.
4. Restart OneDrive from the Start menu.
- If you chose to sync only some folders, choose them again after the sync
  completes.
- The reset deletes the DAT file and OneDrive rebuilds it on restart.
- Store app: Start, type `apps:onedrive`, App settings, Reset.
- Mac: quit OneDrive, show package contents of the app, run
  `ResetOneDriveApp.command` (or `ResetOneDriveAppStandalone.command`) in
  Contents > Resources, then reopen and pick the previous sync location so
  unchanged files are not downloaded again.

## Verify
The sync client shows no error, the problem file opens from the web with its
latest edits, and the error does not return after a restart.

## Checked

Date 2026-11-08. Pages read in full: Fix OneDrive sync problems, Reset OneDrive, and Restrictions and limitations in OneDrive and SharePoint (Microsoft Support). Confirmed: invalid characters, invalid names, TMP and PST behaviour, 250 GB size, 300,000-item recommendation and the 1,000,000 preview requirements, account counts, proxy and elevated-privilege limits, reset steps and effects, library-column behaviour. Removed as not on the pages: icon colour meanings, the 400-character path limit, file-PCNAME conflict naming, the 1 TB quota, the admin sync-health report and EnableSyncAdminReports, the 93-day recycle bin, the unlink/re-link click path. Corrected: PSTs are supported (less often synced), not unsupported; `|` is not in the page's invalid-character list.

Method: docs-only read of cited pages, 2026-11-08
