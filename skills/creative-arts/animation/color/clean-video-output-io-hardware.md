---
id: creative-arts.animation.color.clean-video-output-io-hardware
name: clean-video-output-io-hardware
category: creative-arts
field: animation
product: color
tags: [video-output-card, decklink, ultrastudio, aja, sdi, clean-feed, monitor-calibration, resolve, video-monitoring]
level: practitioner
status: draft
description: "Feed a reference monitor a clean video signal from a dedicated I/O device (DeckLink, UltraStudio, AJA) so the grade bypasses OS colour management and GPU scaling."
sources:
  - https://www.blackmagicdesign.com/products/decklink
  - https://www.aja.com/
  - https://documents.blackmagicdesign.com/UserManuals/DaVinci_Resolve_19_Reference_Manual.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Clean video output via I/O hardware

**Goal:** the monitor receives exactly the pixels the timeline produces, in the video format and range of the
deliverable.

## Why not the GPU output

The desktop GPU output goes through the OS compositor, ICC profiles, scaling, possible 8-bit dithering and
full-range RGB. A video I/O device (Blackmagic DeckLink PCIe or UltraStudio Thunderbolt, AJA Kona/T-Tap) outputs
SDI or HDMI video at the timeline's frame rate, bit depth and YCbCr limited range, as a broadcast monitor expects.

## Setup in Resolve

1. Install the vendor's Desktop Video (Blackmagic) or AJA driver; set the device's output format in its utility.
2. Resolve: Preferences > System > Video and Audio I/O: select the device for *Use for capture and playback*.
3. Project Settings > Master Settings > Video Monitoring: format (1080p23.976), *Use 4:4:4 SDI* where supported,
   data levels **Video** for a broadcast monitor (Full only if the display is set to full range), bit depth 10-bit.
4. Monitor input: set to the same format, range, colour space (Rec.709) and gamma (BT.1886).
5. Calibration LUT on the monitor or LUT box, or in Resolve's video monitor LUT
   (see `creative-arts.animation.color.calibration-luts-in-the-monitoring-path`).

## Other apps

Premiere uses Mercury Transmit for the same devices; Nuke, Flame and RV support SDI output via vendor plug-ins.
Blender has no native SDI output; review its renders in a player that supports the device.

## Gotchas

- Frame rate mismatch between device and timeline gives judder; set both explicitly.
- Range mismatch is the top error: video-range signal on a monitor set to full range looks washed out.
- HDMI from consumer devices may apply TV "enhancements"; disable all picture processing on the display.

## Verify

Output a full-range/limited-range test pattern (e.g. PLUGE): the monitor shows the just-above-black bar and hides
the below-black bar; frame-step in the timeline advances the monitor exactly one frame.
