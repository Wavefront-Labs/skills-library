---
id: computing-software.systems-network-administration.jellyfin.multiple-versions-and-parts
name: multiple-versions-and-parts
category: computing-software
field: systems-network-administration
product: jellyfin
tags: [jellyfin, multiple-versions, multi-part, stacking, cd1, resolution-sorting, movies]
level: practitioner
status: docs-checked
description: "Name files so Jellyfin groups several versions or multi-part files of the same movie or episode into one item."
sources: ["https://jellyfin.org/docs/general/server/media/movies/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Multiple versions and multiple parts

**Multiple versions (movies).** Files in one movie folder are grouped as versions by matching prefixes. Each file must begin exactly, character for character, with the parent folder name including year and provider id, then a label separated by a hyphen, dot, underscore, or in square brackets. Labels are free text.

```txt
Movie (2021) [imdbid-tt12801262]
├── Movie (2021) [imdbid-tt12801262] - 2160p.mp4
├── Movie (2021) [imdbid-tt12801262] - 1080p.mp4
└── Movie (2021) [imdbid-tt12801262] - Directors Cut.mp4
```

**Episodes.** Versions in the same season folder that parse as the same episode are grouped, for example `Series Name S01E01 - 1080p.mkv` and `Series Name S01E01 - Extended.mkv`.

**Ordering.** Versions sort alphabetically, except names ending in `p` or `i` are resolutions sorted high to low (`2160p`, `1080p`, `720p`). The first is the default.

**Multiple parts.** Name files `Movie Name-cd1.mkv`, `-cd2`, and so on. Supported part types: `cd`, `dvd`, `part`, `pt`, `disc`, `disk`. The number can be any number or the letters a to d. Separators may be space, `.`, `-` or `_`, and are optional between type and number.

When parts and versions combine, the version with the extra part is listed first in the selector.

Disc folders (`VIDEO_TS`, `BDMV`) do not support either feature. Check the item's version selector after scanning.

## Checked

2026-11-08. Confirmed against the Jellyfin Movies page: prefix matching and separators, episode grouping, sort order and the p or i resolution rule, part types, separators and numbers, parts combined with versions, disc folder limits. Page read in full.

Method: documentation only; no commands were run.
