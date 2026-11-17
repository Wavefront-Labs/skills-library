---
id: computing-software.systems-network-administration.jellyfin.music-lyrics-files
name: music-lyrics-files
category: computing-software
field: systems-network-administration
product: jellyfin
tags: [jellyfin, lyrics, lrc, elrc, synchronized-lyrics, music]
level: practitioner
status: docs-checked
description: "Add synchronised or plain lyrics to Jellyfin tracks with .lrc, .elrc or .txt files that share the track's file name."
sources: ["https://jellyfin.org/docs/general/server/media/music/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Lyrics files for music

Lyrics must sit in the same folder as the track and have the same base name. For `01 Death Eternal.mp3` the lyric file is `01 Death Eternal.lrc`, `01 Death Eternal.elrc` or `01 Death Eternal.txt`.

```txt
Music
└── Some Artist
    └── Album A
        ├── Song 1.flac
        ├── Song 1.lrc
        └── Song 2.flac
```

**Synchronised lyrics** are interactive: a user can click any line to jump to that timestamp in the song. You can synchronise manually, which is slow and may be inaccurate, or use lyrics software such as MiniLyrics. A synchronised file looks like:

```txt
[ar: Some Artist]
[ti: Song 1]
[al: Album 1]
[length: 2:57]
[00:10.89]Line 1
[00:14.58]Line 2
```

The file may carry extra metadata tags; the client does not show them.

**Unsynchronised lyrics** are plain lines, easier to produce but harder to sing along to:

```txt
Line 1
Line 2
```

Choose `.lrc` when you have timestamps and `.txt` when you do not. Rescan the library, then open the track in a client and check the lyrics view; timestamps should jump playback when a line is clicked.

## Checked

2026-11-08. Confirmed against the Jellyfin Music page: same-folder same-name rule, lrc, elrc and txt extensions, synchronised and unsynchronised examples, MiniLyrics mention, extra metadata not shown. Page read in full.

Method: documentation only; no commands were run.
