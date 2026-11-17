---
id: computing-software.systems-network-administration.immich.transcode-policy-settings
name: transcode-policy-settings
category: computing-software
field: systems-network-administration
product: immich
tags: [ffmpeg, transcode-policy, target-resolution, accepted-containers, preset]
level: practitioner
status: docs-checked
description: "Immich video transcoding settings and defaults: transcode policy values, accepted codecs and containers, preset, target resolution and codecs."
sources:
  - https://docs.immich.app/administration/system-settings
  - https://docs.immich.app/install/config-file
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: decide what Immich transcodes and at what quality. Settings are in Administration, Settings, Video Transcoding Settings; config file keys sit under `ffmpeg`.

Streams are judged independently, so video may be transcoded while audio is left untouched.

Transcode policy (`ffmpeg.transcode`, default `required`):

- `all`: always transcode, giving consistent playback.
- `disabled`: never transcode. Saves resources but may break playback on browsers and devices, or cause high bandwidth.
- `required`: transcode video when it is HDR, not `yuv420p`, or its codec is not in `acceptedVideoCodecs`. Audio is transcoded if its codec is not in `acceptedAudioCodecs`.
- `bitrate`: `required` plus any video over `maxBitrate`.
- `optimal`: `required` plus any video whose horizontal and vertical dimensions are higher than `targetResolution`.

Defaults from the default config:

- `acceptedVideoCodecs`: `h264`; `acceptedAudioCodecs`: `aac`, `mp3`, `opus`.
- `acceptedContainers`: `mov`, `ogg`, `webm`. Videos in other containers are remuxed to MP4 even if no stream is transcoded.
- `targetVideoCodec`: `h264` (options `h264`, `hevc`, `vp9`, `av1`).
- `targetAudioCodec`: `aac` (options `mp3`, `aac`, `opus`).
- `targetResolution`: `720`; the largest dimension is scaled down, never up.
- `preset`: `ultrafast`; it sets the compute effort of transcoding, using h264 preset names.
- `crf`: 23; `tonemap`: `hable`; `twoPass`: false.

See the FFmpeg documentation for the meaning of each option.

## Checked

2026-11-09. Confirmed against the Immich docs (https://docs.immich.app/) by reading administration/system-settings (Video Transcoding Settings, all policy values) and the default `ffmpeg` block in install/config-file.
Reworded: the `optimal` and `preset` entries. Removed: the speed-versus-compression remark, which the page does not state.
Method: documentation only; no commands were run.
