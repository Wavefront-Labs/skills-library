---
id: computing-software.systems-network-administration.frigate.frigate-troubleshooting-missing-recordings
name: frigate-troubleshooting-missing-recordings
category: computing-software
field: systems-network-administration
product: frigate
tags: [recording-troubleshooting, audio-codec-mp4, segment-validation, storage-mount-check, no-new-recording-segments, debug-logging]
level: practitioner
status: docs-checked
description: "Diagnose Frigate recordings that are empty or missing, from retention settings and G.711 audio to stream failures, mounts and discarded segments."
sources: ["https://docs.frigate.video/troubleshooting/recordings/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Troubleshooting missing recordings

Start by enabling debug logging with `logger.logs.frigate.record.maintainer: debug`. A healthy camera logs lines such as `Copied /media/frigate/recordings/... in 0.2 seconds`; if you never see them, no segments reach disk.

Retention causes:
- `record.enabled: True` alone keeps nothing; continuous recording is off by default. Add `record.continuous.days` (for example 3).
- With only motion, alert or detection retention, the mode matters: `motion` (the default) keeps only segments with motion, so over-large motion masks or low sensitivity keep nothing; `active_objects` keeps segments where a tracked object moved; `all` keeps everything.
- Alert and detection retention need working object detection: if `detect.enabled` is False they keep nothing, and objects your model does not support are never recorded.

Camera and stream causes:
- G.711 audio (`pcm_alaw`, `pcm_mulaw`) cannot be stored in MP4, so segments silently fail while live view works. Set `output_args.record: preset-record-generic-audio-aac` or `preset-record-generic` for no audio.
- `No new recording segments were created for <camera> in the last 120s` means ffmpeg cannot read the `record` stream. Check a stream really has the `record` role, open go2rtc on port 1984 to test each stream (errors like `wrong response on DESCRIBE` mean the camera connection failed), try the URL in VLC or `ffplay`, and make sure a restream path uses the right stream name after copying configs.

Storage causes: compare `df -h` with the Storage page in the UI; a mismatch means the bind mount of `/media/frigate` resolves to the wrong filesystem, and Frigate may write to the boot drive and purge aggressively. Check the host path is writable; `chattr +i` on the empty mount point makes writes fail loudly if the mount is missing; check `dmesg`.

Discarded segments: Frigate validates every `.mp4` in `/tmp/cache`; messages such as `Invalid or missing video stream in segment ... Discarding` or `Discarding a corrupt recording segment` mean the stream was interrupted, usually a camera reboot, night-mode switch, connection limit, WiFi or bad cable, or a bitrate too high for the camera. Smart Codec or H.264+ modes with changing parameters cause corrupt timestamps and the "too many unprocessed segments" warning.

## Checked

2026-11-04. Confirmed against the Troubleshooting Recordings page: debug logger and the Copied log line, continuous retention off by default, retention mode meanings, detection dependency for alerts and detections, G.711 audio in MP4 and the AAC and generic presets, the 120s message, go2rtc port 1984 checks, storage mount checks (df, chattr +i, dmesg), discarded segment messages and Smart Codec causes. Nothing removed.
Method: documentation only; no commands were run.
