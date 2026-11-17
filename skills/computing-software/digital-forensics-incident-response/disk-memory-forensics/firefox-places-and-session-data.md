---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.firefox-places-and-session-data
name: firefox-places-and-session-data
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [firefox-forensics, browser-forensics, places-sqlite, sqlite-forensics, sessionstore, dfir]
level: practitioner
status: draft
description: "Analyse Firefox artefacts: places.sqlite visits and bookmarks, downloads annotations, sessionstore jsonlz4, cookies, form history and cache, with timestamp conversion."
sources: ["https://www.sans.org/posters/windows-forensic-analysis/", "https://firefox-source-docs.mozilla.org/browser/places/index.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Firefox places and session data

**Goal:** reconstruct browsing, downloads and open tabs from Firefox profiles.

## Locations
- Windows: `Users\<u>\AppData\Roaming\Mozilla\Firefox\Profiles\<random>.default-release\`
  (cache under `AppData\Local\Mozilla\Firefox\Profiles\...\cache2`).
- macOS: `~/Library/Application Support/Firefox/Profiles/`; Linux `~/.mozilla/firefox/`.
Files: `places.sqlite` (history, bookmarks, downloads), `cookies.sqlite`, `formhistory.sqlite`,
`sessionstore.jsonlz4` and `sessionstore-backups/recovery.jsonlz4`, `logins.json` +
`key4.db`, `extensions.json`, `favicons.sqlite`.

## Queries
Timestamps are **PRTime**: microseconds since 1970-01-01 UTC.
```sql
SELECT datetime(v.visit_date/1000000,'unixepoch') AS visit_utc, p.url, p.title, v.visit_type
FROM moz_historyvisits v JOIN moz_places p ON v.place_id = p.id ORDER BY v.visit_date;
-- Downloads (Firefox 26+): annotations on places
SELECT p.url, a.content, datetime(a.dateAdded/1000000,'unixepoch')
FROM moz_annos a JOIN moz_places p ON a.place_id = p.id
WHERE a.anno_attribute_id IN (SELECT id FROM moz_anno_attributes WHERE name LIKE 'downloads/%');
```
visit_type: 1 link, 2 typed, 3 bookmark, 7 download, 8 framed link.

## Sessions
`jsonlz4` is Mozilla LZ4 with a magic header `mozLz40\0`; decompress with `lz4jsoncat`,
dejsonlz4, or Python `lz4.block.decompress(data[8:])`. Shows open windows/tabs, form data
and closed tabs at last save, sometimes including **private window** state while open.

## Tools
Plaso (`firefox_history`), Hindsight does not cover Firefox; use MZHistoryView,
KAPE `Firefox` target, DB Browser for SQLite.

## Gotchas
- Copy with `-wal` files. `places.sqlite` expiry trims old visits based on disk/memory.
- Multiple profiles; check `profiles.ini`.

## Verify
Cross-check a key visit against proxy/DNS logs or cache entries with matching time.
