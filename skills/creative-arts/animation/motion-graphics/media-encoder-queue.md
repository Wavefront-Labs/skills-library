---
id: creative-arts.animation.motion-graphics.media-encoder-queue
name: media-encoder-queue
category: creative-arts
field: animation
product: motion-graphics
tags: [media-encoder, render-queue, adobe-media-encoder, presets, watch-folders, h264-export, after-effects, premiere-pro, batch-encode]
level: practitioner
status: draft
description: "Use Adobe Media Encoder for AE and Premiere exports: sending comps to the queue, custom presets, watch folders for automatic transcodes, and preset sharing."
sources:
  - https://helpx.adobe.com/media-encoder/user-guide.html
  - https://helpx.adobe.com/media-encoder/using/watch-folders.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Adobe Media Encoder queue

**Goal:** offload encodes from AE/Premiere and standardise deliverable formats with shared presets and
watch folders.

## From After Effects

- Composition - Add to Adobe Media Encoder Queue (Ctrl/Cmd+Alt+M), or from the Render Queue's "Queue
  in AME" button. AME renders the comp using AE's engine in the background (Dynamic Link): AE stays
  usable.
- For heavy comps, rendering a ProRes master from AE's Render Queue and then encoding that in AME is
  more reliable than Dynamic Link for long comps.

## Presets

- Create presets in AME's Preset Browser: format (H.264, HEVC, ProRes), resolution, frame rate
  (Match Source), bitrate mode, audio. Name them by purpose: `SHOW_review_h264_1080`,
  `SHOW_social_916`.
- Export presets (`.epr`) and keep them in the show's shared folder; import on each workstation.
- Use "Match Source" for frame rate and size where possible to avoid accidental resampling.

## Watch folders

File - Add Watch Folder, assign one or more presets. Any file dropped in is encoded automatically
to an Output folder. Useful for: renders landing from the farm becoming review H.264s; editors dropping
masters for social versions.

## Queue management

- Auto-start queue after idle (Preferences) for unattended encoding.
- Duplicate a queued item to add multiple outputs, or assign multiple presets to one source.
- Logs: AME keeps an encoding log (Window - Encoding Log path) useful for proving what was exported.

## Gotchas

- AME's H.264 "VBR 1 pass" defaults may be low bitrate for animation; set target and max bitrate or use
  quality-based settings explicitly.
- Version mismatch: AME must be the same release year as AE/Premiere for Dynamic Link.
- Colour: AME follows the source's colour management; check output tagging with ffprobe
  (`creative-arts.animation.encode-delivery.colour-metadata-tags`).

## Verify

Drop a test file into a watch folder and confirm an output appears with the preset's codec, size and
bitrate (MediaInfo/ffprobe), and that the encoding log records it.
