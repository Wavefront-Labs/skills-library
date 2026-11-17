---
id: computing-software.general-digital-literacy.file-management.restoring-deleted-cloud-files
name: restoring-deleted-cloud-files
category: computing-software
field: general-digital-literacy
product: file-management
tags: [file-management, file-cloud-storage, restore-cloud-files, onedrive-recycle-bin, files-restore]
level: intro
status: docs-checked
description: "Get back files deleted from OneDrive, Google Drive, Dropbox or iCloud Drive from the online recycle bin, and roll back a whole OneDrive after mass deletion or ransomware."
sources:
  - https://support.microsoft.com/en-us/office/restore-deleted-files-or-folders-in-onedrive-949ada80-0026-4db3-a953-c99083e6a84f
  - https://help.dropbox.com/delete-restore/recover-deleted-files-folders
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Restore deleted cloud files

Deleting a synced file on your PC deletes it in the cloud too, but the cloud keeps it for a while. Act quickly:
once a file is permanently deleted from the online bin it cannot be restored.

| Service | Where | Kept for |
|---|---|---|
| OneDrive personal | OneDrive website, **Recycle bin** | 30 days |
| OneDrive work or school | Recycle bin (and any second-stage bin your admin keeps) | 93 days, unless the administrator changed it |
| Dropbox | dropbox.com, **Deleted files** | depends on plan: 30 days (Basic, Plus, Family), 180 days (Professional, Essentials, Standard, Business), 365 days (Advanced, Business Plus, Enterprise, Education) |
| Google Drive | drive.google.com, the bin/trash | see Google's Drive help for the current period |
| iCloud Drive | icloud.com, Drive or Data Recovery | see Apple's iCloud help for the current period |

Select the item, then **Restore**; it returns to its original place and syncs to your devices.
Also check your own computer's Recycle Bin (Windows) or Trash (Mac): files deleted from the cloud, including online-only
files, do not appear there, but files deleted from a local copy might.

## Mass deletion or ransomware
- **OneDrive (Microsoft 365 subscribers):** the "restore your OneDrive" feature rolls everything back to a point in the last 30 days.
- **Dropbox:** Dropbox Rewind can return a folder, or your account, to an earlier point; use it for large-scale changes and the ordinary restore for a few files.
- Before rolling back, stop the infection source (scan and disconnect the infected computer) or it will re-encrypt the restored files.

## Not in the bin?
- Past the retention period or permanently deleted: it cannot be recovered through these steps.
- Shared files you don't own: the owner deleted them; ask them to restore.
- Check search and your sharing filters before assuming a file is deleted.

## Verify
- [ ] Restored file opens on the web and reappears on your devices after sync.

## Checked
2026-10-28. Confirmed against Microsoft Support (restore deleted files in OneDrive): 30 days personal, 93 days work or school
(unless admin changed), cannot restore after permanent deletion, Microsoft 365 subscribers can roll back the whole OneDrive to
any point in the last 30 days, local Recycle Bin/Trash behaviour; and Dropbox Help: plan-based recovery periods and Rewind.
Corrected: Dropbox periods (180 days applies to more plans than "Professional/Business", and a 365-day tier exists); Rewind
"Plus and above" removed. Removed: Google Drive 30 days, iCloud Drive path and 30 days (the cited Apple page was about Time
Machine restore, not iCloud), "Second-stage" bin days, Google "25 days" recovery and "Manage versions" claims, menu paths
not shown on fetched pages.
Method: documentation only; no commands were run.
