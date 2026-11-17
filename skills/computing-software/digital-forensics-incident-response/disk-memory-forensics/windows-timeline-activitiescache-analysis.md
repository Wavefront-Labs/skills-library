---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.windows-timeline-activitiescache-analysis
name: windows-timeline-activitiescache-analysis
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [activitiescache, user-activity-artefacts, windows-timeline, sqlite-forensics, dfir]
level: practitioner
status: docs-checked
description: "Parse ActivitiesCache.db (Windows Timeline): Activity, Activity_PackageId and ActivityOperation tables, activity types, clipboard entries, device IDs and sync caveats."
sources: ["https://ericzimmerman.github.io/", "https://www.sans.org/posters/windows-forensic-analysis/", "https://kacos2000.github.io/WindowsTimeline/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Windows Timeline ActivitiesCache.db analysis

**Goal:** Windows 10 (version 1803 and later) recorded application, file and web activity in `ActivitiesCache.db`, a SQLite database, giving user-activity evidence beyond LNK files and jump lists.

## Tables and fields (from the kacos2000 documentation)
- `Activity` (processed as "Activities" by the published SQL): the activity records; `AppId` and other JSON blobs need the SQLite JSON1 extension to decode.
- `Activity_PackageId`: package and executable mapping; the project provides a timeline query built on its expiry dates.
- `ActivityOperation`: the third table processed by the queries.
- The database also contains a `Smartlookup` view.
- Queries differ between 1803, 1809 and 1903: later versions have more fields, so use a query matching the OS build.

## ActivityType values observed
5 = open application, file or webpage; 6 = application in use (focus); 10 = clipboard text (shown for exactly 43200 seconds, 12 hours); 16 = copy/paste operation (Copy or Paste appears in the Group field); 2 = notification; 11, 12 and 15 = Windows system operations; others not yet understood. In 1903 clipboard text is Base64 encoded.

## Parsing options
- Eric Zimmerman's `WxTCmd` is listed as the Windows 10/11 Timeline database parser (a .NET 10 only command-line tool in the current tool list).
- kacos2000's `WindowsTimeline.exe` decodes clipboard text, joins device information from the registry (HKCU or an offline NTUSER.DAT) and can export "|" delimited CSV; `Clippy` carves current and deleted clipboard entries from the db or db-wal file.
- SQLite queries (`WindowsTimeline.sql`) export to CSV for log2timeline, Timeline Explorer or Excel.

## Caveats
- Platform device IDs identify a specific device but change over time; check them against the registry device entries. Per the PowerShell notes, type 8 looks like smartphones, 9 full-size PCs and 15 laptops.
- Records synced from another device of the same account must not be attributed to this host without checking device ID.
- Since July 2021, for accounts synced through a Microsoft account, new activity is no longer uploaded to Timeline; AAD-connected accounts were not affected. Activity history still shows on the local device.
- Copy the `-wal` file along with the database; Clippy reads clipboard text from the db-wal file as well.

## Verify
Records relied on carry the local device ID and are corroborated with other file access artefacts. Where the SANS Windows Forensic Analysis poster applies, use it for artefact locations and timestamp interpretation.

## Checked
2026-11-08. Confirmed against the kacos2000 WindowsTimeline page and the Eric Zimmerman tool list; the SANS poster page describes itself only generally. Removed as unconfirmed: the profile path under ConnectedDevicesPlatform, `L.<username>` naming, field list for Payload and ExpirationTime, WxTCmd command line, the 30-day retention and Windows 11 deprecation statements.
Method: documentation only; no commands were run.
