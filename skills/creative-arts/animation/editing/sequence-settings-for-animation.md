---
id: creative-arts.animation.editing.sequence-settings-for-animation
name: sequence-settings-for-animation
category: creative-arts
field: animation
product: editing
tags: [sequence-settings, nle-project-setup, nle, timeline-settings, frame-rate, timebase, raster, audio-sample-rate, premiere-pro, resolve, avid]
level: practitioner
status: draft
description: "Set NLE sequence/timeline settings for an animation show: frame rate, raster, pixel aspect, audio rate and start timecode, and which settings lock later."
sources:
  - https://helpx.adobe.com/premiere-pro/using/creating-changing-sequences.html
  - https://documents.blackmagicdesign.com/UserManuals/DaVinci_Resolve_19_Reference_Manual.pdf
  - https://kb.avid.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Sequence settings for an animation show

**Goal:** every editor's timeline matches the show's delivery format, so frame counts in the cut equal frame counts
in production and nothing is resampled on export.

## Decide once, in the show bible

| Setting | Typical animation value | Why |
|---|---|---|
| Frame rate | 23.976 for broadcast/streaming, 24 for theatrical/web-only, 25 for PAL territories | must equal the animation scene frame rate; animating on twos means 12 drawings/s on a 24 base |
| Raster | 1920x1080 or 3840x2160, square pixels | layout and render resolution match |
| Fields | progressive (none) | animation is never interlaced at source |
| Audio | 48 kHz, 24-bit | broadcast and streaming standard; never 44.1 kHz in a picture cut |
| Start timecode | 00:59:50:00 with a 10 s leader, or 01:00:00:00 at first frame of programme | matches online and mix conform |
| Working colour | Rec.709 SDR unless the show is HDR | see `creative-arts.animation.color.rec709-bt1886-sdr` |

## Per NLE

- **Premiere Pro:** File > New > Sequence > Settings tab, Editing Mode *Custom*, Timebase, Frame Size, Pixel
  Aspect *Square Pixels (1.0)*, Fields *No Fields*, Audio Sample Rate 48000. Save the preset and share the
  `.sqpreset`. Sequence > Sequence Settings can change most values later, but a frame size change does not rescale
  existing clips.
- **DaVinci Resolve:** File > Project Settings > Master Settings sets *Timeline frame rate*, which locks as soon as
  the project has a timeline. For a mixed-rate project, untick *Use Project Settings* when creating each timeline
  and set its rate at creation; it cannot be changed afterwards.
- **Avid Media Composer:** project format (frame rate, raster) is chosen when the project is created and fixed for
  the life of the project; a 23.976 project cannot become 25.

## Gotchas

- Dropping the first clip on an empty Premiere timeline offers *Change sequence settings* to match the clip; a
  29.97 temp clip can silently convert the sequence. Answer *Keep existing settings*.
- 23.976 vs 24 confusion causes a 0.1% drift: a 22-minute episode drifts about 1.3 s against the mix. See
  `creative-arts.animation.sound-design.pull-up-pull-down`.
- Drop-frame timecode applies only to 29.97/59.94; 23.976 timecode is always non-drop
  (see `creative-arts.animation.sound-design.timecode-drop-frame`).

## Verify

Export a 10-second test from the timeline and run
`ffprobe -v error -show_entries stream=r_frame_rate,width,height,sample_rate <file>`
(see `creative-arts.animation.encode-delivery.probe`): the values equal the show bible exactly.
