---
id: creative-arts.animation.encode-delivery.mpeg-dash-packaging
name: mpeg-dash-packaging
category: creative-arts
field: animation
product: encode-delivery
tags: [mpeg-dash, adaptive-streaming, mpd, dash-js, shaka-packager, ffmpeg, segment-template, cmaf, streaming]
level: advanced
status: verified
description: "Package renditions as MPEG-DASH (MPD + segments) with ffmpeg or Shaka Packager, sharing CMAF segments with HLS, and validate playback in dash.js."
sources:
  - https://ffmpeg.org/ffmpeg-formats.html#dash-2
  - https://shaka-project.github.io/shaka-packager/html/documentation.html
  - https://reference.dashif.org/dash.js/
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# MPEG-DASH packaging

**Goal:** a DASH manifest (`.mpd`) and segments that play in dash.js, Shaka Player, Android
ExoPlayer and smart TVs. HLS is Apple's format and DASH is MPEG-DASH; with fMP4 segments, one set of media files can be referenced by both manifests.

## Option A: encode renditions, then package with Shaka Packager (recommended)

Encode each rung as an MP4 with aligned keyframes (fixed GOP, same frame rate), then:
```bash
packager \
  in=v1080.mp4,stream=video,output=dash/v1080.mp4 \
  in=v720.mp4,stream=video,output=dash/v720.mp4 \
  in=v480.mp4,stream=video,output=dash/v480.mp4 \
  in=v1080.mp4,stream=audio,output=dash/audio.mp4 \
  --mpd_output dash/manifest.mpd \
  --hls_master_playlist_output dash/master.m3u8 --segment_duration 6
```
This writes a DASH manifest (`--mpd_output`) and an HLS master playlist (`--hls_master_playlist_output`) over the same media files.

## Option B: ffmpeg's dash muxer in one go

```bash
ffmpeg -i ep_master.mov \
  -map 0:v -map 0:v -map 0:a \
  -c:v libx264 -b:v:0 5M -s:v:0 1920x1080 -b:v:1 2.5M -s:v:1 1280x720 \
  -g 48 -keyint_min 48 -sc_threshold 0 -pix_fmt yuv420p -c:a aac -b:a 128k \
  -f dash -seg_duration 6 -use_template 1 -use_timeline 0 \
  -adaptation_sets "id=0,streams=v id=1,streams=a" dash/manifest.mpd
```

`-use_template 1` uses SegmentTemplate instead of SegmentList in the manifest; `-hls_playlist 1` additionally writes HLS playlists (ffmpeg dash muxer options).

## Hosting

- Serve the manifest and segments with the MIME types your player and packager documentation specify; enable CORS for cross-origin players.

## Gotchas

- Unaligned keyframes across renditions cause visible jumps or stalls at switches.
- Ship HLS as well where Apple devices matter (option A writes both from one encode).
- DRM needs encryption at packaging time; see the Shaka Packager documentation for its encryption options.

## Verify

Open the manifest in the dash.js reference player, check the bitrate list matches the ladder,
switch renditions manually and play through a segment boundary. Validate the MPD against your target's requirements (see the DASH-IF guidelines).

## Checked

2026-10-28. Confirmed: ffmpeg dash muxer options `seg_duration`, `use_template`, `use_timeline`, `adaptation_sets` (`id=0,streams=v` form), `hls_playlist`; Shaka Packager `--segment_duration`, `--mpd_output`, `--hls_master_playlist_output`; dash.js reference player page is readable. Removed: the `application/dash+xml` MIME claim (not found in the fetched pages), byte-range and Safari statements, the ISO wording, the on-demand profile claim, the named DRM systems, the conformance tool name.

Run 2026-11-01 with ffmpeg and ffprobe 8.0.1 on Windows (Git Bash), scripts in a scratch folder: option B (the ffmpeg dash muxer command wrote `manifest.mpd`, per-stream init and chunk `.m4s` files; `-hls_playlist 1` added `master.m3u8` and `media_*.m3u8`; `ffmpeg -h muxer=dash` shows `use_template` and `use_timeline` default true). Not run: option A (Shaka Packager is not installed; its flags stay as documented), dash.js playback and DASH-IF validation.

Method: documentation plus commands run (ffmpeg 8.0.1).
