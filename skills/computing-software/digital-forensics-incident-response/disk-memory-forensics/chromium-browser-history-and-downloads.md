---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.chromium-browser-history-and-downloads
name: chromium-browser-history-and-downloads
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [chrome-forensics, chromium-history, edge-forensics, browser-forensics, sqlite-forensics, dfir]
level: practitioner
status: draft
description: "Analyse Chrome and Edge (Chromium) artefacts: History database visits and downloads, timestamps, Top Sites, cache, sessions and profiles, with SQL and tools."
sources: ["https://www.sans.org/posters/windows-forensic-analysis/", "https://github.com/obsidianforensics/hindsight", "https://chromium.googlesource.com/chromium/src/+/HEAD/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Chromium browser history and downloads

**Goal:** reconstruct web activity and downloads from Chrome, Edge, Brave and other
Chromium browsers.

## Locations (per profile)
- Chrome: `Users\<u>\AppData\Local\Google\Chrome\User Data\<Profile>\` (`Default`,
  `Profile 1`...)
- Edge: `...\Local\Microsoft\Edge\User Data\<Profile>\`
- macOS: `~/Library/Application Support/Google/Chrome/<Profile>/`; Linux `~/.config/google-chrome/`.
Key files: `History` (SQLite), `Cookies` (now under `Network\Cookies`), `Web Data`
(autofill), `Login Data`, `Bookmarks` (JSON), `Preferences` (JSON), `Top Sites`,
`Sessions\Session_*`/`Tabs_*`, `Cache\Cache_Data\`, `Extensions\`.

## History queries
Timestamps are **WebKit time**: microseconds since 1601-01-01 UTC.
```sql
SELECT datetime(v.visit_time/1000000-11644473600,'unixepoch') AS visit_utc, u.url, u.title,
       v.transition & 0xFF AS core_transition, u.visit_count
FROM visits v JOIN urls u ON v.url = u.id ORDER BY v.visit_time;

SELECT datetime(start_time/1000000-11644473600,'unixepoch') AS start_utc, target_path,
       tab_url, referrer, total_bytes, state, danger_type, opened
FROM downloads ORDER BY start_time;
```
`downloads_url_chains` gives the full redirect chain of each download. Transition types:
0 link, 1 typed, 2 auto bookmark, 8 reload etc.

## Tools
Hindsight (Chromium-specific, timeline output), DB Browser for SQLite, KAPE targets
`Chrome`/`Edge` + modules, BrowsingHistoryView, Plaso (`chrome_history` parser).

## Gotchas
- Copy the DB **with** `-wal` and `-journal` files before opening; opening can checkpoint and
  lose deleted records.
- History retention is about 90 days for visits; older URLs may remain in `urls` with no visits.
- Sync: entries may originate from another device of the same account (check `visit_source`
  table: 1 = synced).

## Verify
Downloaded file in `downloads.target_path` matches a file on disk with a Zone.Identifier ADS
whose `HostUrl` equals the download URL.
