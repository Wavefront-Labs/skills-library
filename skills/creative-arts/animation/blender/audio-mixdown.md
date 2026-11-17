---
id: creative-arts.animation.blender.audio-mixdown
name: audio-mixdown
category: creative-arts
field: animation
product: blender
tags: [blender, vse, sound-strips, audio-mixdown, mixdown, audio-mixing]
level: practitioner
status: docs-checked
description: "Export audio from Blender: Render Audio mixdown options (container, format, channels, sample rate, split channels, accuracy) and Encoding > Audio settings for video exports."
sources:
  - https://docs.blender.org/manual/en/latest/render/output/audio/introduction.html
  - https://docs.blender.org/manual/en/latest/render/output/properties/output.html#audio
  - https://docs.blender.org/manual/en/latest/files/media/video_formats.html
  - https://docs.blender.org/manual/en/latest/scene_layout/scene/properties.html#audio
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# audio-mixdown

Goal: the edit's sound as a separate file (for mastering) or embedded in the video.

## Separate mixdown (Render menu > Render Audio)

Options:
- **Relative Path**.
- **Accuracy**: sample accuracy, important for animation data. The lower the value, the more accurate.
- **Container**: see the supported containers list in the manual's video formats page.
- **Format**: some containers let you choose a codec.
- **Channels**: Mono, Stereo, Stereo LFE, 4 Channels, 5.1 Surround, 6.1 Surround, 7.1 Surround.
- **Sample Rate**.
- **Split Channels**: render each audio channel into a separate file.

## Embedded in the video (Output Properties > Encoding > Audio)

- **Audio Codec**: the manual lists No Audio, AAC, AC3, FLAC, MP2, MP3, Opus, PCM and others. **No Audio** encodes video only.
- **Audio Channels**: Mono, Stereo, 4 Channels, 5.1 Surround, 7.1 Surround.
- **Sample Rate**, **Bitrate** (per codec), and output **Volume**.
- Not every container and codec combination is compatible; if there are errors check the pairing.

## Scene audio

Scene Properties > Audio has Volume, Distance Model, Doppler Speed and Doppler Factor, and Update Animation Cache (useful if you hear artifacts). Playback device settings are in Preferences > System > Sound.

## Handoff to a sound mixer

Export each group (dialogue, music, effects) separately by muting the other channels and running Render Audio for each, with the same frame range. Agree the delivery format, sample rate and bit depth with the mixer and give them a reference video.

## Verify

Play the exported file in an audio tool: its length equals the edit duration, levels do not clip, and sync matches the video at a clap at the start and end.

## Checked

- Date: 2026-10-27. Documentation: Blender 5.2 manual (blender-v5.2-release branch of blender-manual).
- Confirmed: Render Audio options (Relative Path, Accuracy, Container, Format, Channels list, Sample Rate, Split Channels), Encoding Audio fields (Audio Codec, Audio Channels, Sample Rate, Bitrate, Volume), the audio codec list including No Audio, container and codec compatibility note, scene Audio fields. Corrected Accuracy (lower is more accurate, not higher) and removed the specific container, sample-format, 48 kHz, bitrate and no-OMF/AAF claims, which the manual does not state.
- Method: documentation only; no commands were run.
