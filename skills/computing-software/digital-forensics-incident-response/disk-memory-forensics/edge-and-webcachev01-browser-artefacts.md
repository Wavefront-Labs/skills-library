---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.edge-and-webcachev01-browser-artefacts
name: edge-and-webcachev01-browser-artefacts
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [webcachev01, edge-forensics, browser-forensics, chromium-history, dfir]
level: practitioner
status: draft
description: "Examine Microsoft Edge: Chromium-based profile databases, IE mode and legacy WebCacheV01.dat ESE history including file:// access records."
sources: ["https://www.nirsoft.net/utils/ese_database_view.html", "https://github.com/libyal/libesedb"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Edge and WebCacheV01 browser artefacts

**Goal:** Edge today is Chromium-based, but the legacy ESE database WebCacheV01.dat still exists
and records IE/IE-mode and, crucially, local file access.

## Chromium Edge
- Profile: `%LOCALAPPDATA%\Microsoft\Edge\User Data\<Profile>\` - `History`, `Cookies`
  (`Network\Cookies`), `Login Data`, `Web Data`, `Bookmarks`, `Preferences`, `Sessions\`,
  `Collections` (`collectionsSQLite`), `Extensions\`.
- Same schemas as Chrome: parse with Hindsight, DB Browser for SQLite, or KAPE `EdgeChromium` target + `SQLECmd` maps.
- Edge-specific: `Edge Profile` sync data, `Workspaces`, sidebar apps; `Preferences` shows sync account (work/personal identity).

## WebCacheV01.dat (ESE)
- Location: `%LOCALAPPDATA%\Microsoft\Windows\WebCache\WebCacheV01.dat` (+ `V01.log`, `.chk`, `.jrs`).
- Copy the whole folder; if dirty, repair a **copy** with `esentutl /r V01 /d` (run in the folder) or let the parser handle logs.
- Tables: `Containers` maps container IDs to names (History, Content, Cookies, iedownload, DOMStore);
  `Container_N` tables hold URLs, AccessCount, SyncTime, AccessedTime, ModifiedTime, ExpiryTime.
- **`file:///` entries** in History containers record local and network files opened via
  Explorer-integrated components - evidence of file access even when the browser was not used.

## Tools
```cmd
ESEDatabaseView.exe /table WebCacheV01.dat Container_1 /scomma c1.csv
:: or: esedbexport -t out WebCacheV01.dat  (libesedb)
```
KAPE module `BrowsingHistoryView` / `NirSoft_WebBrowserPassView` (only with authorisation) and Plaso `esedb/msie_webcache` parser.

## Gotchas
- WebCacheV01 is locked while `taskhostw`/`dllhost` runs; collect via raw copy.
- Times in ESE are FILETIME UTC; Chromium uses WebKit epoch (microseconds since 1601).

## Verify
Cross-check file:// entries against LNK/jump lists and MFT for the same files.
