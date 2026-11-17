---
id: computing-software.general-digital-literacy.file-management.video-and-audio-formats-and-codecs
name: video-and-audio-formats-and-codecs
category: computing-software
field: general-digital-literacy
product: file-management
tags: [file-management, file-formats, video-formats, codecs, hevc, audio-formats]
level: intro
status: draft
description: "Understand MP4, MOV, MKV, HEVC, H.264, MP3, AAC and WAV, fix video plays with no picture or no sound, and convert with HandBrake or VLC for sharing."
sources:
  - https://handbrake.fr/docs/
  - https://www.videolan.org/vlc/
  - https://support.microsoft.com/en-us/windows
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Video and audio formats and codecs

## Container vs codec
A file extension is the **container** (`.mp4`, `.mov`, `.mkv`, `.avi`); inside are **codecs** for video (H.264/AVC, H.265/HEVC, AV1, VP9) and audio (AAC, MP3, Opus, AC-3). "Won't play" usually means a missing codec, not a broken file.

| Need | Choose |
|---|---|
| Play anywhere, share, upload | MP4 with H.264 video + AAC audio |
| Smaller files, modern devices | MP4 with HEVC (iPhone default) or AV1 |
| Editing archive / lossless audio | ProRes MOV; WAV or FLAC |
| Music for everyone | MP3 or AAC (.m4a) |

## Common problems
- **Sound but black picture / "codec not supported" (0xc00d5212)**: HEVC on Windows needs the *HEVC Video Extensions* from Microsoft Store (small fee) or open it in **VLC** (plays nearly everything free).
- **iPhone videos too big or won't play on an old PC**: iPhone Settings › Camera › Formats › *Most Compatible* (H.264), or convert.
- **MKV won't open on TV/phone**: convert to MP4.
- **No sound**: audio track is AC-3/DTS the device lacks; convert audio to AAC.

## Convert
- **HandBrake** (free): open file › Preset *Fast 1080p30* (MP4, H.264, AAC) › Start. Lower *RF* number = higher quality, bigger file.
- **VLC**: Media › Convert/Save. Mac: open in QuickTime › File › Export As.
- Each lossy re-encode loses quality; convert from the original.

## Verify
- [ ] Converted file plays with picture and sound on the target device at an acceptable size.
