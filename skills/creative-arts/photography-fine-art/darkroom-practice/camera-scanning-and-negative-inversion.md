---
id: creative-arts.photography-fine-art.darkroom-practice.camera-scanning-and-negative-inversion
name: camera-scanning-and-negative-inversion
category: creative-arts
field: photography-fine-art
product: darkroom-practice
tags: [darkroom-practice, film-scanning, camera-scanning, negative-inversion, negative-lab-pro, dslr-scanning, macro-copy-stand, high-cri-light]
level: practitioner
status: draft
description: "Digitise film with a camera, macro lens and light source, then invert colour negatives with Negative Lab Pro or manual curves for accurate colour."
sources: ["https://www.negativelabpro.com/guide/", "https://www.valoi.co/", "https://www.negativesupply.com/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Camera scanning and negative inversion

## Setup
- Camera on a copy stand, sensor parallel to film (use a mirror or bubble level on both).
- **Macro lens** (true 1:1 for 35 mm on FF; flat-field macro), f/5.6-f/8.
- **High-CRI light source** (CRI 95+, e.g. Negative Supply, Kaiser slimlite, CS-Lite) - white, even;
  some workflows use narrowband RGB for colour negatives.
- Film holder that keeps film flat (Valoi easy35, Negative Supply carriers); anti-newton glass if needed.
- Mask stray light around the frame (reduces flare and contrast loss).

## Capture
1. Manual exposure, base ISO, raw; expose so the film base (orange mask or clear) is bright but not clipped.
2. Focus at 100% live view on grain.
3. Shoot one blank frame of the light source for flat-field correction (Lightroom Flat-Field / NLP).

## Inversion (colour negative)
- **Negative Lab Pro** (Lightroom plugin): white-balance on the film border with the eyedropper, then
  Negative Lab Pro > Convert; choose tone profile and colour model; batch sync roll.
- Manual: invert curve per channel in Photoshop (set black/white points per channel from the base).
- Black-and-white: invert the tone curve in Lightroom (drag points), or use NLP's B&W mode.

## Gotchas
- Dust shows strongly; blow film with a rocket blower, use anti-static brush.
- Inverted files have reversed slider behaviour in Lightroom (if you invert via curve) - NLP handles this.

## Verify
- [ ] Grain sharp corner to corner; neutral greys neutral; batch consistent across a roll.
