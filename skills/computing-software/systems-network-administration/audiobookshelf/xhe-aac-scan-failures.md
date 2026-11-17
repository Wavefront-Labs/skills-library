---
id: computing-software.systems-network-administration.audiobookshelf.xhe-aac-scan-failures
name: xhe-aac-scan-failures
category: computing-software
field: systems-network-administration
product: audiobookshelf
tags: [codec, xhe-aac, ffmpeg, m4b, fdk-aac, scan-error]
level: sme
status: docs-checked
description: "Diagnose Audiobookshelf scan failures on xHE-AAC m4b files and fix them by re-encoding or supplying custom ffmpeg builds."
sources:
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/faq/server.md
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/install/11.env-configuration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Some M4B files use the **xHE-AAC** codec, which FFmpeg 7 or lower does not support. Audiobookshelf relies on FFmpeg and FFprobe, so scanning fails. On FFmpeg 7 or lower the log shows:

```text
[AudioFileScanner] SyntaxError: Expected property name or '}' in JSON at position 2 ...
```

Only the Docker image includes FFmpeg 8, but its default xHE-AAC decoder is weak, so transcoded playback may sound distorted.

Fixes:

1. Easiest: re-encode with a tool that supports xHE-AAC, such as foobar2000 or FFmpeg with `fdk-aac`, to AAC or Opus before adding it.
2. Advanced: build `ffmpeg` and `ffprobe` yourself with `fdk-aac` and point Audiobookshelf at them with `FFMPEG_PATH` and `FFPROBE_PATH`, plus `SKIP_BINARIES_CHECK=1`.

Pre-built ffmpeg with `fdk-aac` cannot be distributed because of licensing, so you must compile it.

## Checked

2026-11-04. Confirmed against the Audiobookshelf docs: FAQ server page (xHE-AAC) and Environment Configuration page (external tools).

Method: documentation only; no commands were run.
