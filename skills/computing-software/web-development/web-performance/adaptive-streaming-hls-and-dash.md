---
id: computing-software.web-development.web-performance.adaptive-streaming-hls-and-dash
name: adaptive-streaming-hls-and-dash
category: computing-software
field: web-development
product: web-performance
tags: [hls-streaming, adaptive-bitrate, mpeg-dash, video-streaming, hls-js]
level: advanced
status: docs-checked
description: "Delivering video with adaptive bitrate streaming: HLS and DASH basics, encoding ladders with ffmpeg, and playback via native HLS or hls.js."
sources:
  - https://developer.apple.com/documentation/http-live-streaming
  - https://github.com/video-dev/hls.js
  - https://ffmpeg.org/ffmpeg-formats.html#hls-2
  - https://web.dev/articles/media-streaming-basics
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Adaptive streaming (HLS / DASH)

A single MP4 forces every viewer to download one quality. Adaptive bitrate (ABR) streaming splits video into short segments at several bitrates; the player switches quality as bandwidth changes.

## 1. When to use it
- Long videos, live streams, large audiences on varied networks.
- Short loops or hero clips: a well-compressed MP4/WebM with `preload="none"` and a poster is simpler.

## 2. Encoding a ladder with ffmpeg
```bash
ffmpeg -i in.mp4 -filter_complex "[0:v]split=3[v1][v2][v3];[v1]scale=-2:1080[v1o];[v2]scale=-2:720[v2o];[v3]scale=-2:480[v3o]" \
  -map "[v1o]" -c:v:0 libx264 -b:v:0 5000k -maxrate:v:0 5350k -bufsize:v:0 7500k \
  -map "[v2o]" -c:v:1 libx264 -b:v:1 2800k -maxrate:v:1 3000k -bufsize:v:1 4200k \
  -map "[v3o]" -c:v:2 libx264 -b:v:2 1400k -maxrate:v:2 1500k -bufsize:v:2 2100k \
  -map a:0 -map a:0 -map a:0 -c:a aac -b:a 128k -ac 2 \
  -g 48 -keyint_min 48 -sc_threshold 0 \
  -f hls -hls_time 4 -hls_playlist_type vod -hls_segment_type fmp4 \
  -master_pl_name master.m3u8 -var_stream_map "v:0,a:0 v:1,a:1 v:2,a:2" out_%v/index.m3u8
```
- Fixed GOP aligned with segment length (`-g` must divide fps x segment seconds: `-g 48` at 24 fps is a 2 s GOP, two per 4 s segment; plus `-sc_threshold 0`) so renditions switch cleanly.
- fMP4 segments (CMAF) can be shared by HLS and DASH manifests.

## 3. Playback
```html
<video id="v" controls playsinline poster="/poster.jpg" preload="none"></video>
<script type="module">
  const v = document.getElementById("v"), src = "/video/master.m3u8";
  if (v.canPlayType("application/vnd.apple.mpegurl")) v.src = src;        // native HLS
  else { const { default: Hls } = await import("hls.js");                  // MSE elsewhere
         if (Hls.isSupported()) { const h = new Hls(); h.loadSource(src); h.attachMedia(v); } }
</script>
```

## 4. Delivery
- CORS: all HLS resources must be delivered with CORS headers permitting GET requests (hls.js README) if the player is on another domain.

## Verify
- [ ] Player switches renditions under DevTools throttling; browsers with native HLS use `src` directly and the rest use hls.js.

## Checked

2026-10-28. Confirmed from the FFmpeg formats documentation (`hls_time`, `hls_playlist_type`, `hls_segment_type`, `master_pl_name`, `var_stream_map` with `%v`, `-g` and `-sc_threshold` in the HLS and DASH examples), the hls.js README (`canPlayType` for native HLS, `Hls.isSupported()`, `loadSource`, `attachMedia`, MSE requirement, CORS headers for all HLS resources) and web.dev media streaming basics (fMP4 supported by both HLS and DASH). Removed (not found): the 30-60 s guidance, managed-service list, bitrate ladder rung advice, `capLevelToPlayerSize`, `startLevel`, DRM and caption claims, cache TTL advice, browser-specific playback claims. The ladder bitrates in the ffmpeg example are illustrative values.

Run 2026-11-01 with ffmpeg and ffprobe 8.0.1 on Windows (Git Bash), scripts in a scratch folder: the three-rung ladder command on a 14 s clip (all rungs gave segments of 4, 4, 4, 2 s, written as `out_N/index*.m4s` with `init_N.mp4`). Not run: the playback snippet in a browser, hls.js, CORS headers, so the skill stays docs-checked.

Method: documentation plus partial commands run (ffmpeg 8.0.1).
