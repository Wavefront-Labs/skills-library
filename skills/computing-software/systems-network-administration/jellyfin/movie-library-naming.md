---
id: computing-software.systems-network-administration.jellyfin.movie-library-naming
name: movie-library-naming
category: computing-software
field: systems-network-administration
product: jellyfin
tags: [jellyfin, movies, library, naming, folder-structure, video-ts, bdmv]
level: intro
status: docs-checked
description: "Lay out a Jellyfin Movies library: one folder per movie named 'Movie Name (year) [provider id]', plus supported formats and forbidden characters."
sources: ["https://jellyfin.org/docs/general/server/media/movies/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Movie library naming and layout

Add movies with the "Movies" library type. Put each movie in its own folder, which may also hold extra files such as `.nfo`, subtitles, cover images and theme music.

Folder name format:

```txt
Movie Name (year) [metadata provider id]
```

`year` and the provider id are optional but identify media more reliably. The video file inside must share the folder's name, with any extension, optionally followed by tags (versions, 3D flags and so on).

```txt
Movies
├── Best_Movie_Ever (2019)
│   ├── Best_Movie_Ever (2019).mp4
│   ├── Best_Movie_Ever (2019).en_us.srt
│   └── cover.png
└── Movie (2021) [imdbid-tt12801262]
    └── VIDEO_TS
```

Examples: `Jellyfin Documentary (2030) [imdbid-tt00000000].mkv`. When you use multiple versions, the provider id must appear in both the folder and the file.

**Formats.** Most common formats such as `mp4` and `mkv` work. `VIDEO_TS` and `BDMV` folders are supported for movies and music videos, but not with multiple versions, multiple parts or external subtitle and audio tracks. `.iso` and other disc images should work but are unsupported; remux them into `mkv` or extract to `VIDEO_TS` or `BDMV`.

**Characters.** Match the provider's title where possible, but avoid characters Jellyfin reserves, which cause problems: `<`, `>`, `:`, `"`, `/`, `\`, `|`, `?`, `*`.

## Checked

2026-11-08. Confirmed against the Jellyfin Movies page: one folder per movie, name format with optional year and provider id, same-name video file, provider id in both folder and file for multiple versions, VIDEO_TS and BDMV support and limits, iso advice, reserved characters. Page read in full.

Method: documentation only; no commands were run.
