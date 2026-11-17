---
id: creative-arts.animation.encode-delivery.ffmpeg-filtergraphs-and-filter-complex
name: ffmpeg-filtergraphs-and-filter-complex
category: creative-arts
field: animation
product: encode-delivery
tags: [filtergraph, filter-complex, ffmpeg, video-filters, labels, overlay, concat]
level: advanced
status: verified
description: "Build FFmpeg filtergraphs: simple -vf versus -filter_complex, chains and labels, mapping graph outputs, common filters, quoting, debugging with a graph script."
sources:
  - https://ffmpeg.org/ffmpeg.html
  - https://ffmpeg.org/documentation.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Filtergraphs and filter_complex

## Simple versus complex
- `-vf` / `-af` apply a **simple** filtergraph: one input stream and one output stream.
- `-filter_complex` (or `-lavfi`) builds graphs with multiple inputs and/or outputs.

## Syntax
- A **filter** is `name=arg1=val:arg2=val` (named options separated by colons).
- A **chain** is filters joined by commas: `scale=1920:1080,fps=24`.
- A **graph** is chains separated by semicolons.
- **Labels** in square brackets name streams: `[0:v]` is the video of input 0; `[a]`, `[out]` are your own labels. An output you want to keep needs to be named, then selected with `-map`.

```bash
# Overlay a logo on the bottom-right of a video, scale the logo first
ffmpeg -i in.mov -i logo.png -filter_complex \
 "[1:v]scale=200:-1[logo];[0:v][logo]overlay=W-w-40:H-h-40[v]" \
 -map "[v]" -map 0:a -c:v libx264 -crf 18 -c:a copy out.mp4

# Concatenate two clips (same size/rate), video and audio
ffmpeg -i a.mp4 -i b.mp4 -filter_complex \
 "[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1[v][a]" -map "[v]" -map "[a]" out.mp4
```

## Frequently used filters
`scale` (with `-2` to keep an even size), `crop`, `pad`, `fps`, `format` (e.g. `format=yuv420p`), `setpts`, `overlay`, `concat`, `split` (duplicate a stream), `drawtext`, `amix`, `aresample`, `loudnorm`, `colorspace` and `zscale` for colour conversions.

## Practical rules
1. Every unlabelled output of the graph is mapped automatically, but once you name outputs, **map them explicitly** (`stream-selection-and-map.md`).
2. Streams used twice need `split` / `asplit`.
3. Keep colour conversions explicit and in the right order (`colour-metadata-tags.md`).
4. Quote the graph: in shells use double quotes on Windows cmd/PowerShell with care, single quotes in POSIX shells; for long graphs use `-filter_complex_script file.txt`.
5. Debug with `-loglevel debug`, or print the parsed graph from the log, and test on a short clip with `-t 5`.

## Gotchas
- Filter order matters: scale before pad, crop before scale.
- `fps` and `setpts` change timing; audio does not follow unless you also change it.
- `concat` filter requires the same dimensions, sample rate and layout across inputs; the concat demuxer is different (stream copy).

## Checked
Run with FFmpeg 8.0.1 on 2026-10-18: the overlay example (logo scaled to 200 px, mapped `[v]` plus `0:a`) and the two-input `concat=n=2:v=1:a=1` example both produced valid output (concatenated duration equalled the sum of the inputs); all filters named in the list (scale, crop, pad, fps, format, setpts, overlay, concat, split, asplit, drawtext, amix, aresample, loudnorm, colorspace, zscale) exist in the build; `scale=301:-2` returned an even height (226); `concat` with inputs of different sizes fails with `parameters ... do not match`; `-filter_complex_script` and `-lavfi` are accepted options.

## Verify
- [ ] The output file has the expected streams (`probe.md`).
- [ ] Short-clip test matches expectation before the full run.
