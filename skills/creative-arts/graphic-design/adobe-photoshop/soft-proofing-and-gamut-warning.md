---
id: creative-arts.graphic-design.adobe-photoshop.soft-proofing-and-gamut-warning
name: soft-proofing-and-gamut-warning
category: creative-arts
field: graphic-design
product: adobe-photoshop
tags: [graphic-design, adobe-photoshop, photoshop, photoshop-color-management, color-modes, soft-proofing, gamut-warning, proof-setup, simulate-paper-color, simulate-black-ink, out-of-gamut]
level: practitioner
status: draft
description: "Preview print output in Photoshop: Proof Setup with the printer's profile, paper and black ink simulation, gamut warning, and print-only adjustments."
sources:
  - https://helpx.adobe.com/photoshop/using/proofing-colors.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Soft proofing and gamut warning

**Goal:** see on screen roughly how an image will print, and fix problems before paying for proofs.

## Proof Setup (View > Proof Setup > Custom)
- **Device to Simulate:** the printer's profile (CMYK press, or the inkjet/paper profile for fine-art printing).
- **Preserve CMYK Numbers** (for CMYK files already converted to this profile): simulates exactly
  what those numbers will print. Off for RGB files.
- **Rendering Intent:** the one you plan to use (Relative Colorimetric or Perceptual); flip between to compare.
- **Simulate Paper Color:** shows paper white and the reduced contrast - the most realistic (and
  most disappointing) view. **Simulate Black Ink** shows real black density.
- Save the setup (`.psf`); it appears in the Proof Setup menu.

Toggle the proof with **Ctrl/Cmd+Y**; the document tab shows the profile name.

## Gamut warning
View > **Gamut Warning** (Shift+Ctrl/Cmd+Y): grey overlay on colours that cannot be printed with the
proof profile. Change the overlay colour in Preferences > Transparency & Gamut.

## Fix out-of-gamut colours (keeping the RGB master)
- Proof on, adjust with **Hue/Saturation** (reduce saturation of the offending range) or Selective
  Color, masked to the area, until the gamut warning shrinks to acceptable small patches.
- Use a separate group named `Print adjustments` you can turn off for screen versions.
- Do not try to eliminate every warning pixel; small saturated highlights clip invisibly.

## Make it meaningful
- Calibrated, profiled monitor, brightness ~80-120 cd/m2 for print work, neutral surroundings, and
  ISO 3664 viewing light for comparing prints (see viewing conditions skill).
- Soft proofing is a preview, not a contract proof - for colour-critical jobs, order a contract proof.

## Gotchas
- Simulate Paper Color looks dull because screens are brighter than paper; let your eyes adapt
  (look only at the proof for a minute, or hide the UI with F).
- Proof setup is per window: View > New Window to see proof and original side by side.

## Verify
- [ ] Proof setup uses the printer's profile with paper simulation on.
- [ ] Key colours (brand, skin) acceptable in proof view; gamut warning only on minor areas.
