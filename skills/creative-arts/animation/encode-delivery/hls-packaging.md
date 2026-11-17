---
id: creative-arts.animation.encode-delivery.hls-packaging
name: hls-packaging
category: creative-arts
field: animation
product: encode-delivery
tags: [hls, adaptive-streaming, m3u8, master-playlist, fmp4, ffmpeg, var-stream-map, segments, streaming, web-player]
level: advanced
status: verified
description: "Package an episode as multi-rendition HLS with ffmpeg: var_stream_map, master playlist, fMP4 vs TS segments, segment length, keyframe alignment, validation."
sources:
  - https://ffmpeg.org/ffmpeg-formats.html#hls-2
  - https://developer.apple.com/documentation/http-live-streaming/hls-authoring-specification-for-apple-devices
  - https://datatracker.ietf.org/doc/html/rfc8216
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# HLS packaging

**Goal:** a self-hosted episode that streams adaptively in Safari, iOS, and hls.js players.
Output: one master playlist (`master.m3u8`) pointing at several variant playlists, each a list
of short segments.

## One-pass, three renditions

```bash
ffmpeg -i ep101_master.mov \
  -filter_complex "[0:v]split=3[v1][v2][v3];[v1]scale=-2:1080[v1o];[v2]scale=-2:720[v2o];[v3]scale=-2:480[v3o]" \
  -map "[v1o]" -c:v:0 libx264 -b:v:0 5M -maxrate:v:0 5.5M -bufsize:v:0 10M \
  -map "[v2o]" -c:v:1 libx264 -b:v:1 3M -maxrate:v:1 3.3M -bufsize:v:1 6M \
  -map "[v3o]" -c:v:2 libx264 -b:v:2 1.2M -maxrate:v:2 1.3M -bufsize:v:2 2.4M \
  -map a:0 -map a:0 -map a:0 -c:a aac -b:a 128k -ac 2 \
  -g 48 -keyint_min 48 -sc_threshold 0 -pix_fmt yuv420p \
  -f hls -hls_time 6 -hls_playlist_type vod -hls_segment_type fmp4 \
  -hls_segment_filename "v%v/seg_%03d.m4s" -master_pl_name master.m3u8 \
  -var_stream_map "v:0,a:0 v:1,a:1 v:2,a:2" "v%v/index.m3u8"
```

- Fixed GOP (`-g 48 -sc_threshold 0` at 24 fps = 2 s) and `-hls_time 6` make every segment
  start on a keyframe in every rendition, which ABR switching needs.
- `-hls_playlist_type vod` is for a complete video-on-demand playlist (hls muxer options).
- Apple's HLS authoring specification requires fMP4 as the container for HEVC video; `-hls_segment_type` selects `mpegts` or `fmp4`.

Ladder choices: see `creative-arts.animation.encode-delivery.abr-ladder-design`.

## Hosting

- Serve `.m3u8` as `application/vnd.apple.mpegurl` and fMP4 `.m4s` segments as `video/iso.segment` (Apple HLS authoring specification); enable CORS for players on another origin.
- Relative URIs in playlists keep the package relocatable.

## Gotchas

- Apple's authoring specification says target durations should be 6 seconds and segment durations nominally 6 seconds.
- ffmpeg documents `-maxrate` as requiring `-bufsize`; set both so peaks stay near the `BANDWIDTH` you advertise.
- Check the master playlist for correct `BANDWIDTH` and `CODECS` attributes.

## Verify

```bash
cat master.m3u8
ffprobe -v error -show_entries format=duration master.m3u8
```

Play in Safari and in an hls.js demo page; throttle the network in dev tools and watch the
rendition switch without a stall. Apple's `mediastreamvalidator` and `hlsreport` tools validate streams (Apple HLS authoring specification).

## Checked

2026-10-28. Confirmed: ffmpeg hls muxer options `hls_time`, `hls_playlist_type`, `hls_segment_type` (`mpegts`, `fmp4`), `hls_segment_filename`, `master_pl_name`, `var_stream_map` with `%v`; Apple HLS authoring specification (fMP4 required for HEVC, 6 second target and segment durations, `application/vnd.apple.mpegurl`, `video/iso.segment` for `m4s`, `mediastreamvalidator`, `hlsreport`); RFC 8216 `EXT-X-ENDLIST`. Removed: the CMAF compatibility and TS legacy-default claims, the player probing claim, the ENDLIST-and-keep-segments sentence.

Run 2026-11-01 with ffmpeg and ffprobe 8.0.1 on Windows (Git Bash), scripts in a scratch folder: the one-pass three-rendition command on a 14 s clip (all three renditions gave segment durations 6, 6, 2 with `EXT-X-TARGETDURATION:6`, `EXT-X-PLAYLIST-TYPE:VOD`, `EXT-X-ENDLIST`, fMP4 `init_*.mp4` and `.m4s` files), `master.m3u8` carrying `BANDWIDTH` and `CODECS`, and `ffprobe` duration of the master playlist. Default segment type without `-hls_segment_type` was mpegts. Not run: Safari, hls.js, Apple's `mediastreamvalidator` and `hlsreport` (not installed), MIME-type hosting; those lines stay as documented by the Apple authoring specification.

Method: documentation plus commands run (ffmpeg 8.0.1).
