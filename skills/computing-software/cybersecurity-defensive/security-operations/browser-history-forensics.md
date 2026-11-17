---
id: computing-software.cybersecurity-defensive.security-operations.browser-history-forensics
name: browser-history-forensics
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [digital-forensics, browser-forensics, chrome-history, edge, firefox-places, hindsight, sqlite, downloads, phishing-investigation]
level: practitioner
status: docs-checked
description: "Recover browser evidence for phishing and exfil cases: Chromium history and downloads tables, Firefox places.sqlite, time units, profile paths and Hindsight."
sources: ["https://github.com/obsidianforensics/hindsight", "https://raw.githubusercontent.com/obsidianforensics/hindsight/master/README.md", "https://kb.mozillazine.org/Profile_folder_-_Firefox", "https://raw.githubusercontent.com/chromium/chromium/main/components/history/core/browser/visit_database.cc", "https://raw.githubusercontent.com/chromium/chromium/main/components/history/core/browser/download_database.cc", "https://raw.githubusercontent.com/chromium/chromium/main/components/history/core/browser/url_database.cc", "https://raw.githubusercontent.com/chromium/chromium/main/components/history/core/browser/history_types.h", "https://raw.githubusercontent.com/mozilla-firefox/firefox/main/toolkit/components/places/nsPlacesTables.h"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Browser history forensics

Browsers record where a user went and what they downloaded: central to phishing (did they open
the link?), malware delivery and exfiltration cases.

## Locations (per user profile)
- Chrome default profile (from the Hindsight README): Windows `[userdir]\AppData\Local\Google\Chrome\User Data\Default`, macOS `[userdir]/Library/Application Support/Google/Chrome/Default`, Linux `[userdir]/.config/google-chrome/Default`.
- Firefox profiles (MozillaZine): Windows `%APPDATA%\Mozilla\Firefox\Profiles\<profile folder>`, macOS `~/Library/Application Support/Firefox/Profiles/<profile folder>`. `profiles.ini` in the folder above Profiles maps profiles; a profile in a custom location is listed there.
- Collect the whole profile folder, not single files.

## Key files
- Firefox: `places.sqlite` holds bookmarks and browsing and download history; `places.sqlite-journal` is the temporary store of updates while Firefox is open, so copy it with the database. `cookies.sqlite`, `formhistory.sqlite` (saved form data) and `sessionstore.js` (stored sessions) are separate files. Current Firefox keeps long-term download history in `places.sqlite`; `downloads.sqlite` was removed in Firefox 26.
- Firefox `places.sqlite` tables: `moz_places` (`url`, `title`, `visit_count`, `last_visit_date`, `typed`), `moz_historyvisits` (`from_visit`, `place_id`, `visit_date`, `visit_type`, `source`), `moz_annos`.
- Chromium `History` database tables: `urls` (`url`, `title`, `visit_count`, `typed_count`, `last_visit_time`), `visits` (`url` key to `urls`, `visit_time`, `from_visit`, `transition`, `visit_duration`), `visit_source`, `downloads` (`target_path`, `start_time`, `danger_type`, `referrer`, `tab_url`, `tab_referrer_url`) and `keyword_search_terms`.

## Tools
Hindsight parses Chrome, other Chromium browsers and Firefox. For Firefox it reads `places.sqlite`, `cookies.sqlite` and `formhistory.sqlite`.
- `-i` profile path (or a parent folder searched recursively), `-o` output name, `-f` format (XLSX default; SQLite and JSONL), `-b` force a browser (Chrome, Edge, Brave, Vivaldi, Firefox or Tor), `-t` display time zone, `-c` cache path if outside the input folder (Mac is set up this way by default).
- `--only` and `--skip` choose artifacts, for example `--only history,downloads` or `--skip cache`; `--list-artifacts` prints the names.
- For download and cache records it decodes ETags into the file's server-side last-modified time and size for several server types; treat that as corroboration, not a substitute for hashing a recovered file.

## Manual query (Chromium)
```sql
SELECT datetime(v.visit_time/1000000-11644473600,'unixepoch') AS visit_utc, u.url, u.title, v.transition
FROM visits v JOIN urls u ON u.id = v.url ORDER BY v.visit_time;
SELECT datetime(start_time/1000000-11644473600,'unixepoch'), target_path, tab_url, referrer, danger_type
FROM downloads;
```
Chromium stores times as microseconds since the Windows epoch (1601-01-01 UTC); 11644473600 is the number of seconds between 1601 and 1970. The Firefox column units are not stated in the sources read, so verify them against a known visit before converting `visit_date`.

## Phishing questions answered
- Was the URL visited, and from where? `visits.from_visit` points at the preceding visit; `downloads.referrer` and `tab_url` give the referring page for a download.
- Downloads: `target_path` (final location), `tab_url` and `danger_type`.

## Gotchas
- Work on copies, never originals, and copy the database together with any journal file.
- Sync: `visit_source` records where a visit came from; value 0 is "synchronized from somewhere else", 1 is "user browsed", 2 an extension and 3-5 imports from Firefox, IE or Safari. Firefox `moz_historyvisits` has its own `source` column.
- Hindsight reports `[ skipped ]` for filtered artifacts, so a missing artifact is distinguishable from an empty one.

## Verify
Cross-check a few visits with proxy or DNS logs at the same UTC time; they should align within seconds.

## Checked
2026-11-08. Confirmed against: the Hindsight README (options, default profile paths, artifacts, ETag decoding, Firefox files), the MozillaZine Firefox profile folder page, Chromium source `visit_database.cc`, `url_database.cc`, `download_database.cc` and `history_types.h` (table and column names, Windows-epoch microsecond time, `VisitSource` values) and Firefox source `nsPlacesTables.h` (`moz_places`, `moz_historyvisits`, `moz_annos`). The MozillaZine page is old, so Firefox file lists may lag current releases. Removed as unconfirmed: Edge profile paths, the Chromium file list beyond `History` (Web Data, Login Data, Network, Sessions, Cache_Data, Preferences, Extensions), the Firefox `cache2` and `sessionstore-backups` names, the PRTime statement for Firefox, KAPE `WebBrowsers` target mention here, SQLECmd/BrowsingHistoryView/DB Browser advice, the "POST is not stored" claim, the Zone.Identifier `HostUrl=` correlation, incognito residue claims, and the SANS poster source (a login-gated landing page). The `-wal` file advice was dropped because no readable page covers it.
Method: documentation only; no commands were run.
