---
id: computing-software.systems-network-administration.jellyfin.show-library-naming
name: show-library-naming
category: computing-software
field: systems-network-administration
product: jellyfin
tags: [jellyfin, shows, library, naming, season-folders, episodes, mkvtoolnix]
level: intro
status: docs-checked
description: "Structure a Jellyfin Shows library with series folders, zero-padded Season folders and SxxExx episode names."
sources: ["https://jellyfin.org/docs/general/server/media/shows/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# TV show library naming and layout

Use the "Shows" library type. Organise into series folders, then season folders inside each series.

```txt
Shows
└── Series Name A (2010)
    ├── Season 00
    │   └── Series Name A S00E01.mkv
    ├── Season 01
    │   ├── Series Name A S01E01-E02.mkv
    │   └── Series Name A S01E03.mkv
    └── Season 02
        ├── Series Name A S02E03 Part 1.mkv
        └── Series Name A S02E03 Part 2.mkv
```

**Series folder:** `Series Name (year) [metadata provider id]`; year and id are optional but help identification.

**Season folders:** name them `Season *` where `*` is a number. Do not abbreviate to `S01` or `SE01`. Pad the number so entries have equal digits, for example `Season 05`. Never mix season folders with loose episodes in the Shows folder.

**Multi-episode files.** One file can contain several episodes, but it appears as a single entry combining their metadata. The docs recommend splitting such files into individual episodes with a tool like MKVToolNix.

Video support, forbidden characters and disc image advice are the same as for movies (see `computing-software.systems-network-administration.jellyfin.movie-library-naming`). Seasons and episodes may also carry provider ids, for example `Season 01 [metadata provider id]` and `S01E01 [metadata provider id].mkv`.

Verify by scanning the library and checking that every episode lands under the right season in the series page.

## Checked

2026-11-08. Confirmed against the Jellyfin TV Shows page: series and season folder rules, Season * naming with zero padding, no S01 abbreviation, no loose episodes beside season folders, multi-episode file advice with MKVToolNix, provider ids on seasons and episodes, shared format and character notes. Partial read: through the Theme media example; the later Multiple Versions and image sections were not needed for these claims.

Method: documentation only; no commands were run.
