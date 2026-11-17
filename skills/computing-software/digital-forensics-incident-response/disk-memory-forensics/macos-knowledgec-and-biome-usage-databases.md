---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.macos-knowledgec-and-biome-usage-databases
name: macos-knowledgec-and-biome-usage-databases
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [knowledgec, biome, macos, ios, app-usage, screen-time, apollo, dfir]
level: advanced
status: draft
description: "Extract application usage, focus, device lock and media activity from macOS/iOS knowledgeC.db and Biome SEGB streams with SQL queries and APOLLO-style tools."
sources: ["https://github.com/mac4n6/APOLLO", "https://github.com/abrignoni/iLEAPP", "https://www.mac4n6.com/blog"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# KnowledgeC and Biome usage databases

**Goal:** show what a user was actively doing (app in focus, device locked/unlocked,
web usage, media played) with precise timestamps.

## Locations
- `knowledgeC.db` (CoreDuet): system `/private/var/db/CoreDuet/Knowledge/knowledgeC.db`,
  per-user `~/Library/Application Support/Knowledge/knowledgeC.db` (macOS); iOS
  `/private/var/mobile/Library/CoreDuet/Knowledge/knowledgeC.db`.
- **Biome** (replacing much of knowledgeC from macOS 13 / iOS 16): `~/Library/Biome/streams/`
  and `/private/var/db/biome/streams/` (macOS), `/private/var/mobile/Library/Biome/` (iOS);
  SEGB-format files per stream (`App.InFocus`, `Device.Locked`, `Safari.History`, etc.).

## Querying knowledgeC
```sql
SELECT ZOBJECT.ZSTREAMNAME AS stream,
       ZOBJECT.ZVALUESTRING AS value,
       datetime(ZOBJECT.ZSTARTDATE + 978307200, 'unixepoch') AS start_utc,
       datetime(ZOBJECT.ZENDDATE   + 978307200, 'unixepoch') AS end_utc,
       (ZOBJECT.ZENDDATE - ZOBJECT.ZSTARTDATE) AS seconds
FROM ZOBJECT
WHERE ZSTREAMNAME IN ('/app/inFocus','/app/usage','/display/isBacklit','/device/isLocked','/safari/history','/app/webUsage')
ORDER BY ZSTARTDATE;
```
Timestamps are **Mac absolute time** (seconds since 2001-01-01 UTC): add 978307200. Copy the
`-wal` and `-shm` files with the database so recent records are included.

## Biome
- SEGB files contain protobuf records; parse with iLEAPP/mac_apt Biome modules or community
  SEGB parsers. Streams of interest: `App.InFocus`, `Device.Display.Backlight`,
  `Notification`, `Safari.History`, `Media.NowPlaying`.

## APOLLO
`python apollo.py extract -o sql_csv -p apple -v yolo modules/ data/` correlates knowledgeC,
interactionC, netusage and other pattern-of-life databases into one timeline using
prebuilt SQL modules.

## Uses
- Was the user at the keyboard (backlit/unlocked + app in focus) when the malicious action
  happened? Strong for insider and attribution questions.
- Which apps were used to open or exfiltrate data, and for how long.

## Gotchas
- Retention: roughly 4 weeks in knowledgeC; Biome varies by stream.
- Database layout changes across OS versions; test queries against a reference image.
- System-level streams require root/FDA to collect live.

## Self-check
Times are converted from Mac absolute time, WAL files were included, and usage claims are
backed by start and end times per record.
