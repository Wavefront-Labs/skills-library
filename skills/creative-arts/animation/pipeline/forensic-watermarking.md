---
id: creative-arts.animation.pipeline.forensic-watermarking
name: forensic-watermarking
category: creative-arts
field: animation
product: pipeline
tags: [watermarking, content-security, visible-watermark, forensic-watermark, screener, per-recipient, drawtext, leak-tracing, tpn]
level: practitioner
status: draft
description: "Protect review copies and screeners: per-recipient visible watermarks with ffmpeg, forensic watermark services for distribution, and logging who received what."
sources:
  - https://www.ttp.org/
  - https://ffmpeg.org/ffmpeg-filters.html#drawtext-1
  - https://www.motionpictures.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Watermarking review copies and screeners

**Goal:** if unreleased footage leaks, you can tell whose copy it was, and casual sharing is discouraged in
the first place.

## Visible, per-recipient watermarks

Every review link or file carries the recipient's name/ID, burned into the picture:
```bash
ffmpeg -i ep104_cut_v012.mp4 -vf "drawtext=fontfile=<FONT>.ttf:text='CONFIDENTIAL  %{eif\:n\:d}  J.SMITH-ACME':\
fontcolor=white@0.25:fontsize=h/18:x=(w-tw)/2:y=h*0.45,\
drawtext=fontfile=<FONT>.ttf:text='J.SMITH-ACME':fontcolor=white@0.15:fontsize=h/30:x=w*0.05:y=h*0.9" \
  -c:v libx264 -crf 22 -c:a copy ep104_cut_v012_JSMITH.mp4
```
- Place it over picture centre (not just the corner, which crops off), semi-transparent.
- Moving or repositioning the mark every few seconds defeats cropping/blur cover-ups:
  `x='mod(t*40,w)'` or switch positions with `enable='between(t,0,10)'` segments.

Review platforms (Frame.io, ftrack Review, ShotGrid, Moxion) add per-viewer watermarks automatically on
playback and downloads; enable them for external reviewers.

## Forensic (invisible) watermarks

For screeners to press, festivals, distributors, and high-value pre-release material, use a forensic
watermarking service (e.g. vendors offering session-based or A/B segment watermarking). These survive
re-encoding and camcording and identify the recipient from a leaked copy. They are commercial services, not
something to build in-house.

## Log distribution

Record: file/version, recipient, date, method (link, download, physical), expiry. Without the log the
watermark is only half useful.

## Gotchas

- A single shared "CONFIDENTIAL" watermark identifies nobody.
- Watermarked files must never re-enter the pipeline as sources; keep them in a separate delivery area.
- Fonts on the render machine: specify a font file explicitly or drawtext fails on headless nodes.

## Verify

Generate copies for two recipients, compare: names differ and remain visible after a 50% scale and re-encode;
the distribution log lists both.
