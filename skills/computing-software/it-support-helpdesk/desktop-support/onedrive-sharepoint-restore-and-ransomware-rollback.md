---
id: computing-software.it-support-helpdesk.desktop-support.onedrive-sharepoint-restore-and-ransomware-rollback
name: onedrive-sharepoint-restore-and-ransomware-rollback
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, backup, data-recovery, onedrive-restore, sharepoint-restore, recycle-bin, restore-your-onedrive, ransomware-recovery, ransomware-response]
level: practitioner
status: docs-checked
description: "Recover OneDrive and SharePoint data: site and second-stage recycle bins (93 days), Restore your OneDrive point-in-time rollback within 30 days, and what to do after ransomware."
sources:
  - "https://support.microsoft.com/en-us/office/restore-your-onedrive-fa231298-759d-41cf-bcd0-25ac53eb8a15"
  - "https://support.microsoft.com/en-us/office/restore-items-in-the-recycle-bin-of-a-sharepoint-site-6df466b6-55f2-4898-8d6e-c0dff851a0be"
  - "https://learn.microsoft.com/en-us/sharepoint/retention-and-deletion"
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# onedrive-sharepoint-restore-and-ransomware-rollback

Goal: put files back the way they were, from one document to a whole encrypted OneDrive, using Microsoft 365's built-in retention.

## Single files and folders
- **SharePoint/Teams recycle bin**: deleted items go to the site recycle bin, not immediately removed. Open the site
  (in a Teams channel: Files tab > More > Open in SharePoint), Quick Launch > Recycle bin, tick items, Restore. In
  Microsoft 365 you can restore items deleted by others if you have edit permissions. This applies to OneDrive for
  work or school files too.
- **Retention**: 93 days from deletion from the original location. Deleting from the site recycle bin moves it to the
  **site collection recycle bin** for the rest of the 93 days, then it is permanently deleted. A site collection
  administrator restores from there.
- Items restore to their original location. You cannot restore a file version if the file itself is deleted, or a
  file if its library is deleted (restore the library first; that restores its files). An existing path gets the
  restored item with a number appended to the name.
- Files you sync and delete can also be in the PC's Windows recycle bin.
- Teams chat files cannot be deleted from a chat's Files tab, and there is no Open in SharePoint option in a chat.

## Restore your OneDrive (point in time)
- Undoes all actions on files and folders within the last 30 days; needs Microsoft 365. Permanently deleted items
  from the OneDrive recycle bin cannot be recovered.
- Work or school account: onedrive.com > Settings > Restore OneDrive. Personal: Settings > Options > Restore your OneDrive.
- Pick a date (such as Yesterday) or Custom date and time. After automatic ransomware detection a suggested restore
  date is filled in. The daily activity chart (30 days) and activity feed show what happened.
- Selecting an activity selects everything after it. Scroll to the top of the feed to review all selected activities
  before pressing Restore.
- Files created after the restore point go to the OneDrive Recycle Bin. Albums are not restored. You can undo a
  restore by running Restore again and selecting that restore action.
- For SharePoint or Teams files, restore a document library instead; versioning is configured per list or library.

## Ransomware / mass encryption or deletion
1. Contain first: isolate the infected PC and reset the user's credentials so sync does not re-encrypt restored files.
2. Use the activity chart to find the first bad activity.
3. Restore OneDrive to just before it.
4. Reimage the endpoint before the user re-syncs.
5. Escalate to the security incident process: this is not just a restore ticket.

## Departed users
A deleted user's OneDrive is retained 30 days by default (configurable), then moves to the site collection recycle
bin for 93 days and is restored with PowerShell. Retention policies, labels and eDiscovery holds take precedence over
this process. Unlicensed OneDrive accounts are archived on their 93rd unlicensed day.

## Gotchas
- Restore rolls back legitimate edits made after the chosen point; tell the user.
- Pause sync during a large restore.

## Verify
Files open with expected content and the endpoint is clean.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Confirmed on the Restore your OneDrive, SharePoint recycle bin and OneDrive retention articles. Removed because not
stated on them: version-count figures, the Restore this library menu path, plan wording for Files Restore, Defender
isolation, Purview preservation hold library detail, and the claim that the user's OneDrive recycle bin retention
differs from 93 days.
