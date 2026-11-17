---
id: computing-software.systems-network-administration.jellyfin.local-artwork-file-names
name: local-artwork-file-names
category: computing-software
field: systems-network-administration
product: jellyfin
tags: [jellyfin, artwork, cover-jpg, backdrop, logo, thumb, poster, folder-jpg, metadata-images]
level: practitioner
status: docs-checked
description: "Use the right local image file names (cover, backdrop, logo, thumb, banner) so Jellyfin shows your artwork before online sources."
sources: ["https://jellyfin.org/docs/general/server/media/movies/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Local artwork file names

Images can be external files beside the media or embedded in media files. External images win over other sources.

```txt
Series Name B (2018)
├── cover.jpg
├── thumbnail.jpg
└── Season 01
    ├── backdrop.webp
    ├── logo.png
    ├── Series Name B S01E01.mkv
    └── Series Name B S01E01-thumb.jpg
```

Music works the same: `cover.jpg`, `backdrop.webp`, `logo.png` in the album folder, and `folder.jpg` in the artist folder root. With no images, Jellyfin takes the cover from the first track with embedded art.

**Image types**

| Type | Use |
| --- | --- |
| Primary | cover or artist image |
| Backdrop | background on the media page |
| Banner | banner browsing mode, video only |
| Logo | shown at the top of an item |
| Thumb | home page and thumb mode, video only |

**File names.** Standalone or as a suffix such as `movie-logo.png`:
- Primary: `poster`, `folder`, `cover`, `default`, plus `movie`, `show`, `jacket`.
- Backdrop: `backdrop`, `fanart`, `background`, `art`, or an `extrafanart` folder.
- Banner: `banner`. Logo: `logo`, `clearlogo`. Thumb: `landscape`, `thumb`.
- Episodes use the suffix form `S01E01 Some Episode-thumb.jpg`.

Several backdrops cycle if you append a number: `backdrop-1.jpg`, `backdrop2.jpg`.

Movie file names such as `cover` can also be embedded in containers like mkv, used when the `Embedded Image Extractor` source is enabled for movies.

## Checked

2026-11-08. Confirmed against the Jellyfin Movies page: image types, accepted file names per type, suffix form for episodes, numbered backdrops, music cover and folder.jpg, embedded-art fallback, Embedded Image Extractor note. Page read in full.

Method: documentation only; no commands were run.
