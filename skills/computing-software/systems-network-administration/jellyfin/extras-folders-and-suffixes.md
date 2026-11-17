---
id: computing-software.systems-network-administration.jellyfin.extras-folders-and-suffixes
name: extras-folders-and-suffixes
category: computing-software
field: systems-network-administration
product: jellyfin
tags: [jellyfin, extras, trailers, featurettes, behind-the-scenes, deleted-scenes, file-suffix]
level: practitioner
status: docs-checked
description: "Attach trailers, featurettes and other extras to movies, series, seasons and music videos by subfolder, file name or suffix."
sources: ["https://jellyfin.org/docs/general/server/media/movies/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Adding extras

Extras attach to movies, series, seasons and music videos in three ways.

**Extras folders** (the cleanest). Create a subfolder with a supported name inside the media folder: `behind the scenes`, `deleted scenes`, `interviews`, `scenes`, `samples`, `shorts`, `featurettes`, `clips`, `trailers`, `theme-music`, `backdrops`, and the catch-alls `other` and `extras`.

```txt
Best_Movie_Ever (2019)
├── Best_Movie_Ever (2019).mp4
├── behind the scenes
│   └── Finding the right score.mp4
└── extras
    └── Home recreation.mp4
```

**Special file names.** For a single extra of a type, name the file `trailer` or `sample` in the same folder, such as `trailer.mp4`.

**File suffixes.** Keep everything in one folder and append a suffix. Apart from the noted exceptions they contain no spaces: `-trailer`, `.trailer`, `_trailer`, ` trailer` (space then the word), the same four forms for `sample`, and `-scene`, `-clip`, `-interview`, `-behindthescenes`, `-deleted`, `-deletedscene`, `-featurette`, `-short`, `-other`, `-extra`.

```txt
Best_Movie_Ever (2019)
├── Preview Trailer.trailer.mp4
└── Making of The Best Movie Ever-behindthescenes.mp4
```

For shows, folders can sit at series level or inside a season folder. Rescan and confirm extras appear on the item's page.

## Checked

2026-11-08. Confirmed against the Jellyfin Movies page: supported extras folder names, the trailer and sample file names, every suffix in the list, show-level and season-level placement. Page read in full.

Method: documentation only; no commands were run.
