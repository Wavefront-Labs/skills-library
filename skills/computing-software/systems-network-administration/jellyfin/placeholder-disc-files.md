---
id: computing-software.systems-network-administration.jellyfin.placeholder-disc-files
name: placeholder-disc-files
category: computing-software
field: systems-network-administration
product: jellyfin
tags: [jellyfin, placeholders, disc-file, dvd, bluray, vhs, metadata]
level: practitioner
status: docs-checked
description: "Add library entries without a playable file by creating empty .disc files, optionally typed as dvd, bluray, vhs or tv."
sources: ["https://jellyfin.org/docs/general/server/media/placeholders/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Media placeholders

Placeholders add video items to a library without a playable video file, for media that is unavailable, absent or should simply be listed. Create an empty file using the normal naming convention with `.disc` as the extension:

```txt
Movies
└── Blade Runner (1982)
    └── Blade Runner (1982).disc
```

The contents of the `.disc` file are not used.

**Optional type.** Put a keyword directly before `.disc`:

| Keyword | Type |
| --- | --- |
| `dvd` | DVD |
| `hddvd` | HD DVD |
| `bluray`, `brrip`, `bd25`, `bd50` | Blu-ray |
| `vhs` | VHS |
| `hdtv`, `pdtv`, `dsr` | TV |

`MyMovie.bluray.disc` is a Blu-ray placeholder, while `MyMovie.bluray.custom.disc` is still a placeholder with no recognised type. Other naming information can be combined provided the type stays directly before `.disc`, for example `Movie (2020).3D.MVC.bluray.disc`.

**Episodes** follow normal show naming: `Example Show S01E01.dvd.disc` inside `Season 01`.

**Behaviour.** Jellyfin treats the file as a real media file, so the item can have metadata, artwork and `.nfo` files, but clients mark it as a placeholder rather than playable.

## Checked

2026-11-03. Confirmed against the Jellyfin Placeholders page: .disc extension, unused contents, type keywords table, recognition rules, 3D example, episodes, metadata behaviour. Removed: invented check step.

Method: documentation only; no commands were run.
