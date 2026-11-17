---
id: creative-arts.graphic-design.editorial-layout.spot-uv-foil-and-embossing-artwork
name: spot-uv-foil-and-embossing-artwork
category: creative-arts
field: graphic-design
product: editorial-layout
tags: [graphic-design, editorial-layout, print-finishing, print-specification, spot-uv, foil-stamping, embossing, debossing, special-finishes, finishing-plates, registration-tolerance, soft-touch-laminate]
level: practitioner
status: draft
description: "Prepare artwork for special finishes (spot UV, foil, emboss/deboss): separate 100% spot plates set to overprint, minimum line weights, registration tolerances and finish order."
sources:
  - https://helpx.adobe.com/indesign/using/spot-process-colors.html
  - https://helpx.adobe.com/illustrator/using/spot-process-colors.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Spot UV, foil and embossing artwork

**Goal:** finishes that land exactly where intended and are technically producible.

## General setup (all finishes)
- Each finish gets its own **spot colour swatch** named as the printer specifies (`Spot UV`, `Foil Gold`, `Emboss`), on
  its own layer, **100% solid** - finishes are on/off, no tints or gradients (except some digital spot UV with
  raised effects - ask).
- Objects set to **Overprint Fill/Stroke** so they do not knock out the CMYK artwork underneath.
- Supply as part of the PDF (separate plates) or as separate PDFs, per printer instructions. Always provide a visual
  mock-up showing the intent.

## Spot UV
- Glossy varnish on selected areas, usually over **matt or soft-touch laminate** for contrast.
- Minimum line/text: ~0.5-1 pt lines, text >= 8-10 pt bold; fine detail fills in.
- Registration tolerance ~0.5-1 mm: either **choke** the UV slightly (0.1-0.25 mm inside the printed shape) or overlap
  it into a safe area - ask the printer which.

## Foil stamping (hot foil / cold foil)
- Hot foil uses a metal die: minimum line ~0.3 mm (0.75-1 pt), minimum gaps ~0.3-0.5 mm; very large solid areas can
  blister or flake (break them up or check). Small reversed text in foil fills in.
- Foil is opaque: artwork underneath is hidden. Do not place CMYK detail beneath unless intentional; knock out or
  keep backgrounds simple.
- Cold foil (inline on press) allows overprinting CMYK on foil for coloured metallics - different rules; ask.

## Embossing / debossing
- Dies are made from your artwork: provide a clean vector (outlined) shape. Multi-level or sculpted embosses need
  a depth description or greyscale height map.
- Heavier, uncoated stocks emboss best; avoid fine details and text below ~10 pt.
- Registered emboss (aligned to print) has tolerance - leave margin; blind emboss (no print) is easier.

## Order and tolerances
Finishes are separate passes after printing: misregistration is normal at 0.5-1 mm. Design so small shifts do not
show (avoid hairline outlines meant to align exactly with a foil shape).

## Verify
- [ ] One 100% spot plate per finish, overprinting, named per printer.
- [ ] Minimum line/text sizes respected; tolerance strategy agreed; mock-up supplied.
