---
id: creative-arts.photography-fine-art.darkroom-practice.flatbed-scanning-and-dust-removal
name: flatbed-scanning-and-dust-removal
category: creative-arts
field: photography-fine-art
product: darkroom-practice
tags: [darkroom-practice, film-scanning, flatbed-scanning, infrared-dust-removal, digital-ice, silverfast-isrd, epson-v850, film-holder-height]
level: practitioner
status: draft
description: "Scan film on a flatbed (Epson V850/V600) with SilverFast or Epson Scan: holder height, resolution, 48-bit raw output, and infrared dust removal (iSRD/ICE)."
sources: ["https://www.silverfast.com/", "https://epson.com/ (Epson Perfection V850 user guide)", "https://www.vuescan.com/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Flatbed scanning and dust removal

## Settings
- Software: Epson Scan 2, SilverFast (Ai Studio, HDR raw), VueScan.
- Output: **48-bit (16 bit/channel) raw or linear TIFF** (SilverFast HDRi / VueScan raw) for editing latitude.
- Resolution: real resolving power of consumer flatbeds is about 2000-2400 ppi despite 6400 claims; scan
  at 2400-3200 ppi for 35 mm; 2400 ppi for 120; 1200-1600 ppi for 4x5.
- Turn off auto sharpening, auto colour, grain reduction in software - do it later.

## Focus (holder height)
Flatbed lenses focus at a fixed height. Adjust film holder height (Epson holder feet; Betterscanning
adjustable holders) in 0.5 mm steps; scan a test strip at each; pick the sharpest.

## Infrared dust removal
- **Digital ICE** (Epson) / **iSRD** (SilverFast) use an infrared channel to map dust and scratches.
- Works on colour negatives, chromogenic B&W (XP2) and most slides; **does not work on silver-based B&W
  film** or Kodachrome reliably (silver blocks IR) - remove dust manually there.
- SilverFast: set iSRD strength low-medium; detect, then check the mask preview.

## Gotchas
- Newton rings with glass: anti-newton glass or fluid mounting.
- Scanning colour negatives with "film type" profiles bakes in conversion; raw + NLP gives more control.

## Verify
- [ ] Grain sharp at holder height chosen; no IR artefacts; files 16-bit.
