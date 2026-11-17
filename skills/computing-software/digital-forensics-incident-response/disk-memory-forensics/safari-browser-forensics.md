---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.safari-browser-forensics
name: safari-browser-forensics
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [safari-forensics, browser-forensics, macos-forensics, sqlite-forensics, dfir]
level: practitioner
status: draft
description: "Examine Safari on macOS and iOS: History.db visits and redirects, Downloads.plist, tabs and sessions, cache and LocalStorage, with Mac absolute time conversion."
sources: ["https://developer.apple.com/documentation/foundation/nsdate", "https://github.com/abrignoni/iLEAPP", "https://github.com/ydkhatri/mac_apt"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Safari browser forensics

**Goal:** reconstruct browsing on macOS (and iOS via FFS/backups) from Safari's databases.

## macOS locations (`~/Library/Safari/` - needs Full Disk Access on live systems)
| File | Content |
|---|---|
| `History.db` | `history_items` (url, visit_count, domain_expansion), `history_visits` (visit_time, title, `redirect_source`/`redirect_destination`, `origin` 0 local / 1 iCloud-synced) |
| `Downloads.plist` | Download URL, local path, size, `DownloadEntryDateAddedKey`, `DownloadEntryDateFinishedKey` |
| `LastSession.plist`, `BrowserState.db`, `CloudTabs.db` | Open tabs, recently closed, tabs from other iCloud devices |
| `Bookmarks.plist`, `TopSites.plist` | Bookmarks, frequently visited |
| `~/Library/Containers/com.apple.Safari/Data/Library/Caches/` | Cache.db, WebKit caches |
| `~/Library/Containers/com.apple.Safari/Data/Library/WebKit/WebsiteData/` | LocalStorage, IndexedDB per origin |

## Query
```sql
SELECT datetime(v.visit_time + 978307200, 'unixepoch') AS visit_utc, i.url, v.title, v.origin,
       v.redirect_source, v.redirect_destination
FROM history_visits v JOIN history_items i ON i.id = v.history_item ORDER BY v.visit_time;
```
Mac absolute time = seconds since 2001-01-01 UTC (add 978307200 for Unix epoch).

## iOS
- `/private/var/mobile/Library/Safari/History.db` (FFS) or in backups; iLEAPP parses history, tabs, and Safari "Favorites".
- Private browsing leaves little; check `BrowserState.db` / tab snapshots in FFS.

## Gotchas
- `origin = 1` visits were synced from another device via iCloud - do not attribute them to this Mac without corroboration.
- Copy `History.db-wal` with the database; recent visits often live only in the WAL.
- Quarantine events (`QuarantineEventsV2`) corroborate downloads with origin URLs.

## Verify
Each relied-on visit or download is confirmed in the raw database with its time conversion shown.
