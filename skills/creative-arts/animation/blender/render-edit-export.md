---
id: creative-arts.animation.blender.render-edit-export
name: render-edit-export
category: creative-arts
field: animation
product: blender
tags: [blender, vse, ffmpeg-output, render-edit-export, ffmpeg-presets, ffmpeg-encoding, h264-encoding, prores]
level: practitioner
status: docs-checked
description: "Export a finished Blender edit as video: Media Type Video, encoding presets, container and codec choice (H.264, ProRes, AV1), Output Quality, Encoding Speed, GOP and audio."
sources:
  - https://docs.blender.org/manual/en/latest/render/output/properties/output.html
  - https://docs.blender.org/manual/en/latest/files/media/video_formats.html
  - https://docs.blender.org/api/current/bpy.types.FFmpegSettings.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# render-edit-export

Goal: a video file that plays everywhere and looks like the timeline.

## Output Properties > Output: Media Type **Video**, then the Encoding panel

The Encoding panel header has presets that choose settings for a type of output; start from one, then adjust. Settings: **Container**, **Video Codec**, Color Depth (8, 10 or 12 bit where the codec allows it), **Output Quality**, **Encoding Speed**, **Keyframe Interval**, **Max B-frames**, and an **Audio** subpanel (codec, channels, sample rate, bitrate, volume).

## Common deliverables

| Use | Container | Codec | Settings |
|---|---|---|---|
| Review, web | MPEG-4 | H.264 | Output Quality High or Perceptually Lossless, Encoding Speed Good, audio AAC |
| Master for further editing | QuickTime | ProRes (profile 422 HQ, or 4444 for alpha) | Audio PCM |
| Smaller streaming files | MPEG-4 or WebM | AV1 (WebM also VP9) | Slower encode |
| Lossless archive | Matroska | FFV1 (lossless, alpha) | Large files |

- **Output Quality** choices: Constant Bitrate, Lossless, Perceptually Lossless, High, Medium, Low, Very Low, Lowest, Custom (CRF; a smaller CRF is better quality, range depends on the codec: 0-51 for H.264, H.265 and AV1, 0-63 for VP9, 1-31 for MPEG-4). Constant Bitrate exposes Bitrate, Minimum, Maximum and Buffer.
- **Encoding Speed**: Slowest, Good (default), Realtime; slower gives better compression.
- **Keyframe Interval** is the GOP size (the Python default is 25); 0 gives intra-only. A higher value usually means smaller files but harder playback.
- **Color**: RGBA only for codecs that support alpha (ProRes 4444, FFV1, VP9 per the manual).

## Gotchas

- Not every container and codec pair works, and some codecs do not accept arbitrary dimensions; stick to common sizes.
- The manual advises against rendering straight to a video file as the first step: a failed render can leave an unplayable file. Render an image sequence, then encode it (see image-sequence-to-video).
- Audio Codec defaults to No Audio, so a render with sound exports mute until you set one.
- Output over 2 GiB: enable Autosplit Output.

## Verify

Play the export in the target player. Check duration, frame rate, audio sync at the end, and colour against the Blender preview. A tool such as ffprobe can list codec, resolution and frame rate.

## Checked

Checked 2026-10-27 against the Blender 5.2 manual (blender-v5.2-release): render/output/properties/output.rst (Media Type, Encoding panel, ProRes profiles, Output Quality, CRF ranges, Encoding Speed, Keyframe Interval, Max B-frames, audio, Autosplit, render-images-first tip), files/media/video_formats.rst (containers, codecs, alpha support), and Python API FFmpegSettings (quality, speed, gopsize default 25, audio default none, container list). Removed: the named preset list, the colour-shift claim about players and H.264 Rec.709, and the even-dimension rule. Method: documentation only; no commands were run.
