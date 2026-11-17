---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.thumbcache-and-windows-search-database
name: thumbcache-and-windows-search-database
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [thumbcache, windows-search-db, windows-search-index, esedb, file-access-evidence, dfir]
level: advanced
status: draft
description: "Examine thumbcache databases and the Windows Search index (Windows.edb / Windows.db) to show files and images existed, and recover indexed content and metadata."
sources: ["https://github.com/thumbcacheviewer/thumbcacheviewer", "https://github.com/strozfriedberg/sidr", "https://www.sans.org/posters/windows-forensic-analysis/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Thumbcache and Windows Search database

**Goal:** prove the existence and viewing of files (especially images and documents) that
may since have been deleted, using thumbnail caches and the search index.

## Thumbcache
`Users\<user>\AppData\Local\Microsoft\Windows\Explorer\thumbcache_<size>.db`
(16, 32, 48, 96, 256, 768, 1280, 1920, 2560, sr, wide, exif, idx).
- Contains thumbnails generated when a folder was viewed in thumbnail mode in Explorer;
  per-user, so attributes viewing to a profile.
- Entries keyed by a **cache entry hash**; the original filename is not stored. Link to file
  via `thumbcache_idx.db` and the Windows Search index (`System_ThumbnailCacheId`).
- Tools: Thumbcache Viewer (exports images, hashes), and for linking: search index parsers.

## Windows Search index
- Windows 10: `ProgramData\Microsoft\Search\Data\Applications\Windows\Windows.edb`
  (ESE database). Windows 11: `Windows.db` (SQLite), `Windows-gather.db`, `Windows-usn.db`.
- Contains file paths, metadata (size, dates, owner, author), **partial content** of indexed
  documents and emails (Outlook items), and the thumbnail cache IDs.
- Tools: SIDR (Search Index DB Reporter) for both formats, `esedbexport` (libesedb) for EDB,
  sqlite3 for the Windows 11 DB, WinSearchDBAnalyzer.
- Copy with raw access (the service holds locks) or from an image; ESE may need
  `esentutl /r` / `/p` on a *copy* if dirty.

## Use
Insider cases (files present before wiping), CSAM investigations (law enforcement only),
email content from OST indexing, deleted file metadata.

## Gotchas
- Indexing scope defaults to user folders and Start menu; not all drives.
- The index updates and purges entries; capture early.

## Verify
Link at least one thumbnail to a file path via the index and corroborate the path with
$MFT or LNK evidence.
