---
id: computing-software.systems-network-administration.jellyfin.music-videos-library
name: music-videos-library
category: computing-software
field: systems-network-administration
product: jellyfin
tags: [jellyfin, music-videos, library, nfo, no-metadata-provider, folder-structure]
level: intro
status: docs-checked
description: "Set up a Music Videos library where names are used as-is, folders can nest, and nfo files supply metadata."
sources: ["https://jellyfin.org/docs/general/server/media/music-videos/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Music Videos library

Use the "Music Videos" library type. Layout is mostly like movies with two differences: no external metadata providers are available by default, and multi-level folders are supported.

```txt
MusicVideos
├── Folder 1
│   ├── Folder 1.1
│   │   └── Song 1
│   │       ├── Song 1 Version 1.mp4
│   │       └── Song 1 Version 2.mp4
│   └── Song 3
│       ├── Song 3.mkv
│       └── Song 3.nfo
└── Song 4
    └── Song 4.avi
```

**Naming.** Folders and files can be named however you like, because no metadata is fetched; the folder and file names become the item names in Jellyfin. Local `.nfo` files can add metadata.

The video format notes match movies: common containers work, `VIDEO_TS` and `BDMV` folders are supported without versions, parts or external tracks, and `<`, `>`, `:`, `"`, `/`, `\`, `|`, `?`, `*` should be avoided.

Multiple versions, 3D flags, multiple parts, extras, external streams and local images follow the same rules as movies; see `computing-software.systems-network-administration.jellyfin.multiple-versions-and-parts` and `computing-software.systems-network-administration.jellyfin.extras-folders-and-suffixes`.

Self-check: scan and confirm each folder or file appears under its own name.

## Checked

2026-11-08. Confirmed against the Jellyfin Music Videos page: library type, no default metadata provider, multi-level folders, free naming, VIDEO_TS and BDMV limits, reserved characters, section headings for versions, 3D, parts, extras and images. Partial read: lines 1-90 in full plus the section headings after that; the later sections repeat the movies page.

Method: documentation only; no commands were run.
