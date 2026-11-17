---
id: computing-software.systems-network-administration.jellyfin.chapter-image-extraction
name: chapter-image-extraction
category: computing-software
field: systems-network-administration
product: jellyfin
tags: [jellyfin, chapter-images, trickplay, library-settings, extraction, dummy-chapters]
level: practitioner
status: docs-checked
description: "Enable chapter image extraction per library and tune the dummy chapter interval and image resolution."
sources: ["https://jellyfin.org/docs/general/server/metadata/chapter-images/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Chapter images

Chapter images are preview images for the chapters of a video file, stored in the metadata directory inside the server's config directory. Do not confuse them with chapters (the ticks on the timeline): chapters display even when chapter images are disabled, but chapter images must be enabled to show.

**Enable per library**
1. Add a library with a video content type and open "Chapter Images", or use the three dots of an existing library, then "Chapter Images".
2. Turn on chapter image extraction.
3. Optionally extract during the library scan. This moves extraction from the "Extract Chapter Images" task into the "Scan Media Library" task. It can be computationally intensive and slow scans, especially on large libraries.

**Dashboard settings** (Libraries, then Metadata):
- **Interval:** creates dummy chapters every N seconds if the file has no chapters; 0 disables dummy chapters. Small values are not recommended because the web player renders every chapter on the timeline and playback can slow.
- **Resolution:** size of extracted images. They appear in a small preview window, so high resolution is unnecessary.

Cloud-mounted libraries should not extract images because it requires downloading whole files (see `computing-software.systems-network-administration.jellyfin.storage-sizing-and-cloud`).

## Checked

2026-11-03. Confirmed against the Jellyfin Chapter Images page (per-library enable, extract during scan, Interval and Resolution settings, warnings) and the Storage page (cloud image extraction). Removed: invented verification.

Method: documentation only; no commands were run.
