---
id: creative-arts.animation.encode-delivery.ffmpeg-stream-selection-and-map
name: ffmpeg-stream-selection-and-map
category: creative-arts
field: animation
product: encode-delivery
tags: [stream-mapping, ffmpeg-map, map, stream-selection, audio-tracks, metadata, ffmpeg]
level: practitioner
status: verified
description: "Choose streams explicitly with ffmpeg -map: default selection rules, stream specifiers, optional and negative maps, stream copy, language and disposition tags."
sources:
  - https://ffmpeg.org/ffmpeg.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Stream selection and -map

By default FFmpeg picks **one stream per type** (the best video, the best audio, one subtitle) from the inputs. Any multi-track delivery (stems, languages, alternate tracks) needs `-map`.

## Specifiers
- `-map 0` selects all streams of input 0. `-map 0:v` all video, `-map 0:a` all audio, `-map 0:a:1` the second audio stream, `-map 1:v:0` the first video of input 1, `-map 0:3` stream index 3.
- A **trailing `?`** makes the map optional: `-map 0:s?` does not fail if no subtitle exists.
- A **negative map** removes streams: `-map 0 -map -0:s` copies everything except subtitles.
- Mapping a **filtergraph output** uses its label: `-map "[v]"` (`ffmpeg-filtergraphs-and-filter-complex.md`).

## Examples
```bash
# Video from file A, audio from file B, copy both
ffmpeg -i video.mov -i audio.wav -map 0:v:0 -map 1:a:0 -c copy out.mov

# Keep all audio tracks and tag languages
ffmpeg -i in.mov -map 0:v -map 0:a -c:v libx264 -crf 18 -c:a aac \
  -metadata:s:a:0 language=eng -metadata:s:a:1 language=fra out.mp4

# Drop everything except video and the first audio
ffmpeg -i in.mxf -map 0:v:0 -map 0:a:0 -c copy out.mov
```

## Related options
- `-c copy` / `-c:v copy` copies without re-encoding.
- `-metadata:s:a:0 title=...` sets per-stream metadata; `-disposition:a:0 default` marks the default track.
- `-map_metadata 0` copies global metadata from input 0; `-map_chapters` for chapters.
- `-shortest` ends output with the shortest mapped stream.

## Gotchas
- With any `-map`, the automatic selection is **off** for that output: forgetting to map audio gives silent output.
- Maps are per output file: put `-map` options before the output filename they apply to.
- Some containers do not accept every codec (for example PCM in MP4 is limited); pick the container accordingly.
- Verify the result with `ffprobe -show_streams` (`probe.md`).

## Checked
Run with FFmpeg 8.0.1 on 2026-10-18: `-map 0 -map -0:s` and `-map 0:s?` succeed on a file with no subtitles while `-map 0:s` fails with `Stream map '' matches no streams`; mapping only `0:v` gives output with no audio; `-map 0:v:0 -map 0:a:0 -c copy`, `-map "[v]"` from a filtergraph and `-disposition`, `-map_metadata`, `-map_chapters`, `-shortest` are all accepted. PCM audio in an MP4 muxed here as `pcm_s16le` (tag `ipcm`), so the container note means availability varies by player and spec, not that FFmpeg refuses it.

## Verify
- [ ] Stream list and languages match the delivery spec.
- [ ] No unintended streams (commentary, data tracks) are carried over.
