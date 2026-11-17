---
id: computing-software.web-development.webassembly.media-codecs-wasm
name: media-codecs-wasm
category: computing-software
field: web-development
product: webassembly
tags: [webassembly, ffmpeg-wasm, image-codecs-wasm, squoosh, wasm]
level: practitioner
status: docs-checked
description: "Media tools"
sources: ["https://raw.githubusercontent.com/ffmpegwasm/ffmpeg.wasm/main/README.md", "https://raw.githubusercontent.com/GoogleChromeLabs/squoosh/dev/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Codecs and media processing

Goal: process media client-side.
- ffmpeg.wasm is a pure WebAssembly and JavaScript port of FFmpeg for recording, converting and streaming audio and video in the browser; its README carries an "experimental" stability badge. Measure speed and download size yourself rather than assuming.
- Squoosh is an image compression web app that processes images locally in the browser (nothing is sent to a server) across many formats; see its repository for the codecs it ships.
- Offload heavy work to workers and stream results (design advice, not from these pages).
- Check codec licences for your use case; neither README is a licensing guide.
Verify: the processed output plays and its size is reasonable.

## Checked

2026-11-08. Confirmed in the ffmpeg.wasm README and the Squoosh README (both read in full).
Removed as unconfirmed: "slow vs native", "large download" and the specific AVIF, JXL and MozJPEG codec list.
Method: documentation only; no commands were run.
