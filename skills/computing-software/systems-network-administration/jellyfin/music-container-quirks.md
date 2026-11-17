---
id: computing-software.systems-network-administration.jellyfin.music-container-quirks
name: music-container-quirks
category: computing-software
field: systems-network-administration
product: jellyfin
tags: [jellyfin, music, flac, m4a, mka, id3, remux, ffmpeg]
level: advanced
status: docs-checked
description: "Rename or remux audio-only mp4, mkv and weba files, and handle FLAC tag problems and ID3v1 truncation in Jellyfin."
sources: ["https://jellyfin.org/docs/general/server/media/music/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Music file container quirks

Jellyfin supports most common music formats, with these exceptions from the docs:

- **Audio-only `.mp4`** is not recognised as music. Rename it to `.m4a`.
- **Audio-only `.mkv` or `.webm`** is not recognised. Rename to `.mka`.
- **`.weba`** is unsupported. Rename to `.mka`.
- **`.flac` with embedded WebP images or ID3 tags** may fail to play in Chromium-based browsers (Chrome, Edge, Opera, Brave) or Firefox. Turn on `Always remux FLAC audio files` in the client settings.
- **ID3v1 tags** limit most fields to 30 bytes and longer values are truncated. Upgrade to ID3v2.4.

Problem files can be remuxed into `.mka` with ffmpeg:

```sh
ffmpeg -i <Input File> -c:a copy <Output File>.mka
```

The docs warn metadata may be damaged and images may not carry over, so restore tags manually or with another program.

Workflow: find the failing files from the playback error, apply the rename or remux, rescan, and play one file in the browser that failed. Keep the original files until the new ones have correct tags and artwork.

## Checked

2026-11-08. Confirmed against the Jellyfin Music page: mp4, mkv, webm and weba renames, FLAC with WebP or ID3 and the Always remux FLAC audio files setting, ID3v1 30-byte limit, ffmpeg mka command and metadata warning. Removed: the sentence about audiobooks, which this page does not state. Page read in full.

Method: documentation only; no commands were run.
