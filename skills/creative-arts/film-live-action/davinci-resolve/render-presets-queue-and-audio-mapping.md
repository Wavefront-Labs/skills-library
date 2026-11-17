---
id: creative-arts.film-live-action.davinci-resolve.render-presets-queue-and-audio-mapping
name: render-presets-queue-and-audio-mapping
category: creative-arts
field: film-live-action
product: davinci-resolve
tags: [davinci-resolve, resolve, film-live-action, custom-render-preset, platform-presets, preset-saving, remote-render, render-queue-management, render-jobs, deliver-audio-settings, channel-mapping-deliver, audio-export-deliver]
level: practitioner
status: draft
description: "Set up Resolve deliveries: custom and platform render presets, render queue and remote rendering across machines, and audio export settings with channel mapping for masters."
sources:
  - "https://documents.blackmagicdesign.com/UserManuals/DaVinci_Resolve_Reference_Manual.pdf (Resolve Reference Manual - Deliver page: render settings, render queue, remote rendering, audio)"
  - "The Definitive Guide to DaVinci Resolve (Blackmagic official training) - Deliver page"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Render presets, queue and audio mapping

**Goal:** every deliverable rendered with saved, verified settings - queued, rendered
on whichever machine is free, with the audio channels where the spec says.

## 1. Presets
- Built-in presets: YouTube, Vimeo, TikTok, H.264/H.265 master, ProRes, IMF, DCP etc.
- **Custom**: set format/codec, resolution, frame rate, data levels, colour space tags
  (*Advanced Settings*: Rec.709 Gamma 2.4 vs Rec.709-A tags), audio, subtitles, file
  naming - then the three-dot menu > **Save As New Preset**. Export/import presets
  (`.xml`) to share across suites.
- Name presets by deliverable: `NETFLIX_ProRes4444XQ_UHD_2398_5.1+ST`.
- Direct upload to platforms (YouTube/Vimeo/ Frame.io) via *Internet accounts* in
  preferences, where useful.

## 2. Render queue
- **Add to Render Queue** for each job (one per deliverable/timeline); jobs keep their
  settings. Render all or selected; reorder.
- Use **in/out** range or entire timeline; **Single clip** vs **Individual clips** (see
  VFX handoff skill).
- Check the queue job's details (filename, path) before starting - easy to overwrite.

## 3. Remote rendering
Multiple Resolve Studio machines sharing a **PostgreSQL** project database and the
same media/LUT/plugin paths:
- Render machines run Resolve set to **Remote Rendering** (*Workspace > Remote
  Rendering*), waiting for jobs.
- On the grading suite, in each queue job choose the **render machine** (*Render on:*)
  then start - the remote machine renders while you keep working.
- Path mapping must resolve identically on both machines.

## 4. Audio settings and channel mapping
In the render settings **Audio** tab:
- Codec (Linear PCM 24-bit for masters, AAC for web), sample rate 48 kHz.
- **Output track** mapping: choose number of output tracks and map each to a bus or
  track - e.g. for a broadcast/streaming master: Ch1-6 = 5.1 main (L R C LFE Ls Rs),
  Ch7-8 = stereo main, Ch9-14 = 5.1 M&E, Ch15-16 = stereo M&E (per spec).
- *Render one track per channel* where specs need discrete mono tracks.
- Verify with a channel ID test or by inspecting the file (MediaInfo).

## Gotchas
- Presets saved without the right colour space tags; platforms show gamma shifts.
- Overwriting previous renders with the same filename.
- Remote render with different LUT/OFX versions - different output.
- Channel order (L R C LFE vs L C R) wrong in the master.

## Verify
- [ ] Named custom presets per deliverable, shared across suites.
- [ ] Queue jobs checked for range, path and filenames.
- [ ] Remote render machines share database and paths.
- [ ] Audio mapping matches the spec; verified with MediaInfo.
