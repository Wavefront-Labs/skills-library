---
id: computing-software.systems-network-administration.frigate.frigate-live-view-and-webrtc
name: frigate-live-view-and-webrtc
category: computing-software
field: systems-network-administration
product: frigate
tags: [live-view, smart-streaming, jsmpeg, mse, webrtc, live-stream-names, transcoded-streams, webrtc-candidates]
level: practitioner
status: docs-checked
description: "Frigate's jsmpeg, MSE and WebRTC live view modes: expose go2rtc streams in the UI, add transcoded streams and open the WebRTC port."
sources: ["https://docs.frigate.video/configuration/live/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Live view, MSE and WebRTC

By default Frigate uses smart streaming: when there is no detectable activity a camera image updates once per minute to save bandwidth, then switches to a live stream.

Technologies:
- jsmpeg: frame rate equals `detect.fps` capped at 10, 720p, no audio, no go2rtc needed; it is the default without go2rtc and uses more browser GPU.
- MSE: native frame rate and resolution, audio depending on codec, requires go2rtc and is the default when go2rtc is configured. iPhone needs iOS 17.1 or newer and Firefox is H.264 only.
- WebRTC: native quality, requires extra setup, used when MSE fails or for two-way talk. It may use an external STUN server; MSE and HLS need no internet.
In a camera's single-view settings you can pick Stream, a "Force low-bandwidth mode" switch (plays the detect stream via jsmpeg), and MSE or WebRTC. Choices are saved per device and camera in browser local storage. WebRTC is disabled in the menu with a reason shown if it is not configured, cannot connect (port 8555 or STUN/TURN problem) or the codecs are unsupported.

Multiple live streams: under `cameras.<name>.live.streams` map a friendly name to a go2rtc stream name, for example `Main Stream: test_cam` and `Sub Stream: test_cam_sub`. Only go2rtc stream names are allowed, not paths. The default All Cameras dashboard uses the first entry.

Transcoded streams: `live.transcode` with `enabled`, an optional `source` and `qualities` (each `height` and `bitrate` in kbps) adds go2rtc streams named `<camera>_transcode_<height>p`, encoded to H.264 only while watched; this costs CPU per viewer.

WebRTC needs port 8555 (TCP and UDP). For internet access forward it on the router; for local access outside the Home Assistant App set `go2rtc.webrtc.candidates` such as `192.168.1.10:8555` and `stun:8555`. The web UI uses `ice_servers` and falls back to Google's public STUN server.

## Checked

Method: docs-checked 2026-11-09 against docs.frigate.video/configuration/live (read as raw markdown from the blakeblackshear/frigate docs folder); documentation only, no commands were run.

Confirmed against those pages: the settings, topics, defaults and procedures described above.

Removed or corrected: Nothing removed.
