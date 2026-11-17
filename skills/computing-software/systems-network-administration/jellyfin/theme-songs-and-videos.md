---
id: computing-software.systems-network-administration.jellyfin.theme-songs-and-videos
name: theme-songs-and-videos
category: computing-software
field: systems-network-administration
product: jellyfin
tags: [jellyfin, theme-media, theme-songs, theme-videos, backdrops, webm]
level: intro
status: docs-checked
description: "Add theme songs and theme videos to movies and shows and enable them in clients."
sources: ["https://jellyfin.org/docs/general/server/media/movies/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Theme songs and theme videos

Theme media plays in the background while a user browses a title, giving the library an audio-visual touch.

**Where Jellyfin looks**
- Theme songs: `theme.ext` in the title's folder, or files in a `theme-music` subfolder.
- Theme videos: files in a `backdrops` subfolder.

```txt
Series Name (2010)
├── backdrops
│   └── S1Intro.ext
├── Season 01
│   └── theme-music
│       └── S1Intro.ext
├── theme.ext
└── theme-music
    └── intro-song.ext
```

Series, and individual season folders, can each have their own theme media.

**Enable it per user.** Clients must opt in. In the web UI this is user settings, Display, Libraries, then Theme songs and Theme videos. Third-party clients may differ.

**Behaviour**
- If both songs and videos are found and enabled, theme videos are preferred and songs do not play.
- In web-based clients multiple theme files are shuffled on opening a listing; this cannot be changed.
- Theme media is transcoded like other media when needed. Because transcoding delays start, web-standard formats such as WebM (VP9/Opus) are recommended since they generally direct play.

Check by enabling the user setting and opening the title page.

## Checked

2026-11-08. Confirmed against the Jellyfin Movies page: theme.ext, theme-music and backdrops locations, per-user client option path, videos preferred over songs, shuffling, WebM recommendation. Page read in full.

Method: documentation only; no commands were run.
