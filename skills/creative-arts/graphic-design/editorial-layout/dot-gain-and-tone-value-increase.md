---
id: creative-arts.graphic-design.editorial-layout.dot-gain-and-tone-value-increase
name: dot-gain-and-tone-value-increase
category: creative-arts
field: graphic-design
product: editorial-layout
tags: [graphic-design, editorial-layout, print-colour, iso-12647, dot-gain, tone-value-increase, tvi, paper-types, screen-ruling, minimum-dot, reversed-type, uncoated-paper]
level: advanced
status: draft
description: "Understand tone value increase (dot gain) by paper and process, how press profiles compensate, and design rules for shadows, light tints and reversed type."
sources:
  - https://www.iso.org/standard/57833.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dot gain and tone value increase

**Goal:** artwork whose tones, shadows and fine details survive the way ink spreads on the chosen paper.

## What it is
Halftone dots print larger than their nominal size (ink spread on paper + optical effects). A 50% tone may print as
62-72%. **Tone value increase (TVI)** is the standard term in ISO 12647-2; "dot gain" is the trade term.
- Typical TVI at 50% (ISO 12647-2:2013, 175 lpi-ish screens): **coated ~13-16%**, **uncoated ~18-22%** or more;
  newsprint higher (ISO 12647-3, ~26%).
- More gain on uncoated, lower-quality and absorbent stock; with finer screens; on web presses vs sheetfed.

## How it is handled
- Press profiles (FOGRA39/51, GRACoL, uncoated profiles) model TVI: converting images with the right profile lightens
  midtones to compensate. Using a coated profile for uncoated paper = dark, muddy prints (see output intent skill).
- Platemaking curves on press calibrate to the standard (G7 for GRACoL, PSO for FOGRA).
- Greyscale images: use a matching gray profile (e.g. Dot Gain 20%) when converting.

## Design rules that follow
- **Shadow detail:** dark tones fill in (plug). Keep important shadow detail below ~90% on uncoated; open up shadows in Curves.
- **Minimum dot:** very light tints (< 3-5%) can drop out; specify tints >= 5% (and pale tints carefully on uncoated).
- **Fine reversed text** (white out of a dark area) fills in: on uncoated stock keep reversed text >= 8-9 pt and avoid
  hairline serifs; avoid reversing small text out of 4-colour builds (registration).
- **Thin rules** and fine type in tints break up - use solid colours or heavier weights.
- **Rich black areas** limited by TAC (see output preview skill).

## Verify
- [ ] Images converted with the profile for the actual paper.
- [ ] Shadows hold detail; tints >= 5%; reversed type sizes suit the stock.
- [ ] For critical work, a contract proof on the target condition approved (see proofing skill).
