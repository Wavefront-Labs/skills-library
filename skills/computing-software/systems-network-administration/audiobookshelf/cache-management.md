---
id: computing-software.systems-network-administration.audiobookshelf.cache-management
name: cache-management
category: computing-software
field: systems-network-administration
product: audiobookshelf
tags: [cache, file-cache, api-cache, purge-cache, metadata-cache]
level: practitioner
status: docs-checked
description: "Understand Audiobookshelf's file cache and in-memory API cache, and when to use Purge Items Cache versus Purge All Cache."
sources:
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/server-management/server-settings.md
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/libraries/book-library/2.book-metadata.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Two caches exist.

**File cache** lives in `/metadata/cache` and can be cleared from server settings or by deleting files on disk.

- Items cache (`/metadata/cache/items`): temporary media backups made by the Encoder or Metadata Embed tools, only if you choose Backup. Not for long-term storage and not included in database backups.
- Image cache: resized cover and author images for faster loading.

`Purge Items Cache` clears only `/metadata/cache/items`. `Purge All Cache` clears the entire file cache.

**API cache** is in memory only. It speeds navigation by caching data for recently visited pages, and auto-clears after a short time or when the database updates. `API Cache Miss` in debug logs is common and only useful for performance debugging.

Important: the embed tool's backup copies are not cleaned up automatically. The metadata page tells you to clean them from `/metadata/cache/items` periodically, so purging the items cache is the routine way to reclaim that space. Check that an embed result is correct before purging, because the backup is your only copy of the original audio file.

## Checked

Method: docs-checked 2026-11-09 against the Server Settings page (Caching section) and the Book Metadata page (Embedding Metadata) of the Audiobookshelf docs repo, both read from raw markdown.
