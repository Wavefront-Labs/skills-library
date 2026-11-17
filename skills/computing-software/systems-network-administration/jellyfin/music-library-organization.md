---
id: computing-software.systems-network-administration.jellyfin.music-library-organization
name: music-library-organization
category: computing-software
field: systems-network-administration
product: jellyfin
tags: [jellyfin, music, albums, multi-disc, folder-structure, embedded-metadata]
level: intro
status: docs-checked
description: "Organise a Jellyfin music library with one folder per album, embedded tags and optional disc folders."
sources: ["https://jellyfin.org/docs/general/server/media/music/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Music library organisation

Each album lives in its own folder; one folder holds one and only one album. How albums are grouped above that does not matter. File names generally do not matter because Jellyfin reads embedded metadata, and uses file names as track titles only when no other metadata exists.

```txt
Music
├── Some Artist
│   ├── Album A
│   │   ├── Song 1.flac
│   │   └── Song 2.flac
│   └── Album B
└── Album X
    └── Whatever You.mp3
```

Characters known to cause problems in names: `<`, `>`, `:`, `"`, `/`, `\`, `|`, `?`, `*`.

**Multiple discs.** Jellyfin identifies them from the `disc number` and `total discs` tags. Put all tracks in one folder, or optionally separate `Disc 1`, `Disc 2` folders; embedded metadata takes priority over folder names.

```txt
Album 2
├── Disc 1
│   └── Disc 1 Track 1.aiff
└── Disc 2
    └── Disc 2 Track 1.aiff
```

Artwork rules are in `computing-software.systems-network-administration.jellyfin.local-artwork-file-names`.

Self-check: scan the library and confirm each album shows the right track count and disc numbering; if not, fix the tags rather than the folder names.

## Checked

2026-11-08. Confirmed against the Jellyfin Music page: one album per folder, file names mostly irrelevant, reserved characters, disc number and total discs tags, optional disc folders, embedded metadata priority. Page read in full.

Method: documentation only; no commands were run.
