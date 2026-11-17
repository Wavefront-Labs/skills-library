---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.onedrive-and-cloud-sync-artefacts
name: onedrive-and-cloud-sync-artefacts
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [user-activity-artefacts, onedrive-forensics, cloud-sync, dropbox-forensics, google-drive-forensics, file-access-evidence, dfir]
level: advanced
status: draft
description: "Analyse OneDrive, Dropbox and Google Drive sync client artefacts: synced file lists, settings databases, logs, and Files On-Demand placeholders, plus server audit."
sources: ["https://www.sans.org/posters/windows-forensic-analysis/", "https://github.com/Beercow/OneDriveExplorer", "https://learn.microsoft.com/en-us/purview/audit-log-activities"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# OneDrive and cloud sync artefacts

**Goal:** determine which files were synchronised to or from cloud storage, by which
account, including files no longer present locally.

## OneDrive (Windows)
- Settings: `Users\<u>\AppData\Local\Microsoft\OneDrive\settings\Personal\` and
  `Business1\`: `<cid>.dat`/`SyncEngineDatabase.db` (newer, SQLite) listing synced items
  with names, parent folders, sizes, hashes (quickXor); `.ini` files with account info.
- Logs: `AppData\Local\Microsoft\OneDrive\logs\` `.odl`/`.odlgz` binary logs (parse with
  `odl.py` / OneDriveExplorer) showing sync operations and sometimes file names.
- Registry: `NTUSER\Software\Microsoft\OneDrive\Accounts\Personal|Business1` (UserEmail,
  `UserFolder`, `cid`), `SyncEngines\Providers`.
- **Files On-Demand** placeholders: NTFS reparse points; files appear in $MFT with cloud
  attributes even when content is not local.
- Distinguish **personal** vs business accounts: personal sync to a corporate machine is a
  common insider exfil path.

## Dropbox
`AppData\Local\Dropbox\instance1\` (`sync_history.db`, `aggregation.dbx` encrypted on newer
versions), `info.json` (account and path).

## Google Drive for desktop
`AppData\Local\Google\DriveFS\<account id>\metadata_sqlite_db` (items, parents, names),
`content_cache`, logs in `DriveFS\Logs`.

## Server side
OneDrive/SharePoint audit (`FileUploaded`, `FileDownloaded`, `FileSyncUploadedFull`,
`FileSyncDownloadedFull`), sharing events; Google Drive audit in Admin console.

## Gotchas
- Encrypted or binary-format databases change between versions; use current parsers.
- A file present in the sync DB proves it was in the synced folder, not when uploaded;
  combine with logs and audit.

## Verify
Key files appear in both the client database and server audit logs with consistent names
and times.
