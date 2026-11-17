---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.browser-cache-analysis
name: browser-cache-analysis
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [browser-cache, browser-forensics, chrome-forensics, firefox-forensics, dfir]
level: practitioner
status: docs-checked
description: "Recover page content and files from Chromium caches (blockfile and Simple Cache) and see which Plaso parsers and tools read Chromium and Firefox caches."
sources: ["https://www.chromium.org/developers/design-documents/network-stack/disk-cache/", "https://www.nirsoft.net/utils/chrome_cache_view.html", "https://github.com/obsidianforensics/hindsight", "https://plaso.readthedocs.io/en/latest/sources/user/Parsers-and-plugins.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Browser cache analysis

**Goal:** history shows that a URL was visited; the cache can show what was actually delivered, with the
HTTP headers that came with it.

## Chromium (Chrome, Edge, Brave)
- The cache is a single folder and every file in it belongs to the cache (Chromium may delete any of it).
  ChromeCacheView notes that new Chrome versions use a `Cache_Data` subfolder.
- **Blockfile format** (the format the Chromium design document describes): at least five files, one `index`
  file (the hash table used to find entries) and four `data_n` block-files. Block-files hold fixed-size blocks
  (examples: 256 bytes, 1 KB, 4 KB) and store HTTP headers, keys and small bodies. Data larger than
  `kMaxBlockSize` (16 KB) goes to a separate file named `f_xx` (hexadecimal number) with no special header.
- Each entry is identified by a key (the resource name, for example a URL) and has separate data streams:
  one for the HTTP headers and one for the resource data.
- Addresses inside the cache are 32-bit "cache addresses"; for example 0xA0010003 is block-file `data_1`,
  initial block 3, one block, and 0x8000002A is external file `f_00002A`. Check the magic number and version
  in the index and block-file headers before parsing.
- **Simple Cache** is a newer on-disk format (Chromium uses it on Android; ChromeCacheView added support
  for "Simple Cache for HTTP" in v1.80). The design document's entry description is only valid for version 2.x
  files, so expect differences in current browsers.
- Newer Chrome partitions the cache: the URL key can carry a `_dk_` prefix, and ChromeCacheView v2.25 shows
  the 'Web Site' and 'Frame' that requested the item.
- Incognito mode uses an in-memory cache implementation, so expect no disk cache for private browsing.
- Tools: ChromeCacheView (NirSoft) shows URL, content type, size, last accessed, expiration, server name
  and response, extracts files (`/copycache`), decompresses Brotli (`Content-Encoding: br`, since v1.90) and
  its Deleted File column marks deleted entries; Hindsight parses cache records among its artefacts and takes
  `-c`/`--cache` for a cache directory outside the profile folder (`--skip cache` leaves it out);
  Plaso has a `chrome_cache` parser ("Google Chrome or Chromium Cache files").

## Firefox
- Plaso lists `firefox_cache` for cache version 1 (Firefox 31 or earlier) and `firefox_cache2` for cache version 2
  (Firefox 32 or later). NirSoft lists MZCacheView as its Firefox cache viewer.
- Hindsight also parses Firefox profiles, though its README names `places.sqlite`, `cookies.sqlite` and
  `formhistory.sqlite` for Firefox, not the cache.

## Workflow
1. Export cache entries with URL, times and content type (for example ChromeCacheView's `/scomma` with `/Columns`).
2. Filter by domain and time window from the browsing history.
3. Decompress bodies and render HTML only in an isolated, offline analysis machine.
4. Hash extracted files, and note ChromeCacheView's Deleted File column ('Yes' when the cache file is deleted).

## Gotchas
- The cache must not grow unbounded and old entries are evicted, so presence is meaningful and absence is not.
- Hindsight decodes ETags in cache and download records into a server last-modified time and size, but the
  README says that is what the server claimed, not a substitute for hashing a recovered file.

## Checked
Date: 2026-11-07.
Read in full: Chromium "Disk Cache" design document (overview, disk structure, cache address, index, block files, entry, implementation notes, eviction, data integrity); NirSoft ChromeCacheView page including the full version history and command-line options; Hindsight GitHub README (options, artifact filters, ETags, default paths); Plaso "Parsers and plugins" page (cache parser rows).
Confirmed: blockfile layout, 16 KB external-file rule, `f_xx`/`data_n` naming, example addresses, key/header/data streams, Simple Cache on Android, `Cache_Data`, `_dk_` prefix, Brotli support, Deleted File column, `chrome_cache`/`firefox_cache`/`firefox_cache2` rows, Hindsight `-c`/`--skip cache`.
Trimmed: `cache2\entries\<SHA1>` layout and metadata fields, Firefox cache location, `<hash>_0`/`index-dir` Simple Cache file names, "Hindsight --cache parsing", "evicts quickly", prefetch/preconnect and beacon claims, and the Verify step (none are on the pages).
Method: documentation only; no commands were run.
