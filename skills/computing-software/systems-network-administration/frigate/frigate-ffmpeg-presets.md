---
id: computing-software.systems-network-administration.frigate.frigate-ffmpeg-presets
name: frigate-ffmpeg-presets
category: computing-software
field: systems-network-administration
product: frigate
tags: [ffmpeg-presets, input-args, output-args, record-audio-presets, rtsp-restream-preset, reolink-http-flv]
level: advanced
status: docs-checked
description: "Pick Frigate ffmpeg hwaccel, input and output argument presets, and avoid mixing HTTP, RTMP and RTSP presets when restreaming."
sources: ["https://docs.frigate.video/configuration/ffmpeg_presets/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# FFmpeg presets

Presets expand at runtime into long lists of FFmpeg arguments, keeping config short. In YAML you write the name (`preset-vaapi`); the UI shows a friendly label (VAAPI (Intel/AMD GPU)).

Hwaccel presets (`ffmpeg.hwaccel_args`, global or per camera): `preset-rpi-64-h264` and `-h265`, `preset-apple-silicon-h264` and `-h265` (under lighter, needs the `lighter.sh/video` device), `preset-vaapi`, `preset-intel-qsv-h264` and `-h265` (use VAAPI if QSV causes issues), `preset-nvidia`, `preset-jetson-h264` and `-h265`, and `preset-rkmpp` (image with the `-rk` suffix, privileged mode).

Input args presets (`input_args` on an input):
- `preset-rtsp-generic`: the default when none given
- `preset-rtsp-restream`: source is a go2rtc restream; `preset-rtsp-restream-low-latency` lowers latency but may break some cameras
- `preset-rtsp-udp` for UDP-only cameras; `preset-rtsp-blue-iris` for Blue Iris
- `preset-rtmp-generic`
- `preset-http-jpeg-generic` and `preset-http-mjpeg-generic` (restreaming is recommended instead)
- `preset-http-reolink` for Reolink HTTP-FLV, only when not restreaming as RTSP.
Watch for mixed protocols: the `http` and `rtmp` presets cannot be used with `rtsp` streams. The Reolink example uses the HTTP-FLV substream with `preset-http-reolink` for `detect` and the go2rtc RTSP restream with `preset-rtsp-generic` for `record`.

Output args presets (`output_args.record`): `preset-record-generic` (no audio), `preset-record-generic-audio-copy` (keep original audio without re-encoding) and `preset-record-generic-audio-aac` (transcode audio to AAC; the default when none are specified). Choose audio-copy when the camera already produces AAC.

## Checked

Method: docs-checked 2026-11-09 against docs.frigate.video/configuration/ffmpeg_presets (read as raw markdown from the blakeblackshear/frigate docs folder); documentation only, no commands were run.

Confirmed against those pages: the settings, topics, defaults and procedures described above.

Removed or corrected: Nothing removed.
