---
id: computing-software.systems-network-administration.audiobookshelf.audio-file-probe-and-repair
name: audio-file-probe-and-repair
category: computing-software
field: systems-network-administration
product: audiobookshelf
tags: [ffprobe, ffmpeg, corrupt-audio, transcoding, repair, codec]
level: advanced
status: docs-checked
description: "Probe a problem audio file in Audiobookshelf and repair headers with ffmpeg -c copy before re-encoding."
sources:
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/libraries/book-library/2.book-metadata.md
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/install/11.env-configuration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Open the audiobook, use **More Info** in the Audio Tracks table, then **Probe Audio File** for raw `ffprobe` output you can copy. Typical problems: wrong duration, wrong chapter titles. A file that will not play or seek is usually corrupted, malformed, or in a codec or container the device does not support.

Audiobookshelf transcodes when the client cannot direct-play the codec, but that fails if the file is corrupt.

Repair options: get a fresh copy (download or rip again), or re-encode.

```bash
ffmpeg -i input.mp3 -c copy output.mp3
ffmpeg -i "original file.m4b" -c copy "new file.m4b"
```

`-c copy` copies audio and rewrites metadata. It usually fixes corrupt metadata and header issues but not corrupt audio data or an unplayable codec. If still unplayable, re-encode with the same or a new codec: `ffmpeg -i input.mp3 output.mp3`. Quote names with spaces.

If ffmpeg is not on the path, set `FFMPEG_PATH` and `FFPROBE_PATH`.

## Checked

2026-11-04. Confirmed against the Audiobookshelf docs: Book Metadata page (Checking Audio Metadata) and Environment Configuration page.

Method: documentation only; no commands were run.
