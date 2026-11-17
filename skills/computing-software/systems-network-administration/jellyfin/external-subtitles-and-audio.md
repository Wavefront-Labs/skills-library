---
id: computing-software.systems-network-administration.jellyfin.external-subtitles-and-audio
name: external-subtitles-and-audio
category: computing-software
field: systems-network-administration
product: jellyfin
tags: [jellyfin, subtitles, external-audio, srt, forced, sdh, default-flag, naming]
level: practitioner
status: docs-checked
description: "Name external subtitle and audio files so Jellyfin reads their language, default/forced/SDH flags and title."
sources: ["https://jellyfin.org/docs/general/server/media/movies/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# External subtitles and audio tracks

Jellyfin picks up external subtitle and audio files by suffix, placed beside the video and starting with the video's base name.

```txt
Film (1986)
├── Film.mkv
├── Film.default.srt
├── Film.default.en.forced.ass
├── Film.forced.en.dts
├── Film.en.sdh.srt
└── Film.English Commentary.en.mp3
```

Each field after the base name is a title or a flag; separate fields with `.`. Special flags:

| Type | Flag |
| --- | --- |
| Default | `default` |
| Forced | `forced`, `foreign` |
| Hearing impaired | `sdh`, `cc`, `hi` |

`hi` collides with the Hindi language code: on its own it resolves as a Hindi track, but alongside another language (`title.en.hi.srt`) it marks hearing impaired for that language.

Flags are ignored on containers with more than one stream.

Text that is neither a language nor a flag is joined into the stream title, if the file has no embedded title. In the example the last file is an English mp3 audio stream titled `English Commentary`. Episodes work the same, such as `Series Name A (2021) S01E01 Title.ja.ass`.

Disc folders do not support external tracks. After a scan, check the track list in the player for the right language and flag.

## Checked

2026-11-08. Confirmed against the Jellyfin Movies page: suffix examples, default/forced/foreign/sdh/cc/hi flags, hi versus Hindi, flags ignored on multi-stream containers, title from leftover text, disc folders unsupported. Page read in full.

Method: documentation only; no commands were run.
