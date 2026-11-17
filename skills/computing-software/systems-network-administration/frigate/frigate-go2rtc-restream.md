---
id: computing-software.systems-network-administration.frigate.frigate-go2rtc-restream
name: frigate-go2rtc-restream
category: computing-software
field: systems-network-administration
product: frigate
tags: [go2rtc, rtsp-restream, restream-credentials, single-camera-connection, birdseye-restream, exec-source, audio-transcode]
level: advanced
status: docs-checked
description: "Use Frigate's built-in go2rtc to restream cameras over RTSP, reduce camera connections, transcode audio and keep exec sources off."
sources: ["https://docs.frigate.video/configuration/restream/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# go2rtc restream in Frigate

Frigate embeds go2rtc to provide an RTSP restream at `rtsp://<frigate_host>:8554/<camera_name>` (port 8554 must be open) and the MSE and WebRTC live view. Stream details for debugging are at `/api/go2rtc/streams`. Configuration lives under the `go2rtc:` key.

Secure the restream with `go2rtc.rtsp.username` and `password`; this does not apply to localhost, so Frigate's own cameras need no credentials.

Reduce connections to the camera (for cameras that allow one session): define `go2rtc.streams.<name>` with the camera URL, then point the camera's ffmpeg input at `rtsp://127.0.0.1:8554/<name>` with `input_args: preset-rtsp-restream` and roles `record`, `detect` and `audio`. With a sub stream, define a second go2rtc stream for it; two connections are made, one per stream. For HTTP sources the docs use ffmpeg-based entries. To add a missing audio codec, add a second entry `ffmpeg:<name>#audio=opus` (and set `output_args.record: preset-record-generic-audio-copy`).

Birdseye restream: `birdseye.restream: True` serves `rtsp://<frigate_host>:8554/birdseye` but makes Birdseye run 24/7, raising CPU. A low `birdseye.idle_heartbeat_fps` (1 or 2) pushes the last frame when idle to speed up connections.

Security: `exec:`, `echo:` and `expr:` sources are disabled by default because they allow arbitrary command execution; streams using them are removed and an error is logged. Enable only with `GO2RTC_ALLOW_ARBITRARY_EXEC=true` (or `go2rtc_allow_arbitrary_exec` for Home Assistant App users) when you trust everyone who edits the config. RTSP output from exec uses `{{output}}`; pipe output has no braces.

## Checked

Method: docs-checked 2026-11-09 against docs.frigate.video/configuration/restream (read as raw markdown from the blakeblackshear/frigate docs folder); documentation only, no commands were run.

Confirmed against those pages: the settings, topics, defaults and procedures described above.

Removed or corrected: Nothing removed.
