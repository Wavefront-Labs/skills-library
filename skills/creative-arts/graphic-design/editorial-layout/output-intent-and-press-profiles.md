---
id: creative-arts.graphic-design.editorial-layout.output-intent-and-press-profiles
name: output-intent-and-press-profiles
category: creative-arts
field: graphic-design
product: editorial-layout
tags: [graphic-design, editorial-layout, print-colour, iso-12647, output-intent, fogra, fogra39, fogra51, pso-coated-v3, gracol, swop, icc-profile, pdf-x, print-production, prepress]
level: advanced
status: draft
description: "Pick the right press characterisation (FOGRA39/51, GRACoL, SWOP, uncoated) as PDF/X output intent, matched to the printing condition and paper."
sources:
  - https://www.color.org/chardata/drsection1.xalter
  - https://www.idealliance.org/gracol
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Output intent and press profiles

**Goal:** the PDF tells the press exactly which printing condition the colours were prepared
for, and the CMYK values in it are right for that condition.

## What the output intent is
A PDF/X file must declare one **output intent**: an ICC profile (and characterisation name)
describing the target printing condition. RGB/Lab content in PDF/X-4 is converted to that
condition by the RIP; CMYK content is assumed already prepared for it.

## Common characterisations
| Region / process | Paper | Characterisation | ICC profile |
|---|---|---|---|
| Europe offset, ISO 12647-2:2004 | Coated (PT1/2) | **FOGRA39** | Coated FOGRA39 / ISO Coated v2 (ECI) |
| Europe offset, ISO 12647-2:2013 | Coated, OBA paper | **FOGRA51** | PSO Coated v3 |
| Europe offset | Uncoated (PT5) | FOGRA47 / FOGRA52 | PSO Uncoated ISO12647 / PSO Uncoated v3 |
| USA sheetfed (G7) | Grade 1 coated | **GRACoL 2013 (CRPC6)** | GRACoL2013_CRPC6 |
| USA web offset (publication) | Grade 3/5 | SWOP 2013 (CRPC5) / SWOP v2 | SWOP2013C3_CRPC5 |
| Newspaper | Newsprint | ISO 12647-3 / IFRA26 | ISOnewspaper26v4 |

**Ask the printer** which they print to; many publish a PDF preset with the intent built in.

## Where to set it
- InDesign/Illustrator Export PDF > **Output**: Destination profile and **Output Intent Profile
  Name** (PDF/X). For PDF/X-4 keep "No Color Conversion" or "Convert to Destination
  (Preserve Numbers)" so CMYK values you set (black text 0/0/0/100) are not changed.
- Photoshop: convert images to the same profile if delivering CMYK images.
- Make the CMYK working space in Color Settings match (see colour settings skill).

## What goes wrong
- **Coated profile on uncoated paper:** images print dark and muddy (higher dot gain, ink
  limit too high - FOGRA39 TAC 330% vs ~300% uncoated).
- **Mixed profiles** (images converted to SWOP in a FOGRA39 job): neutral greys and skin tones shift.
- **Rich black recipe** depends on the condition: keep total area coverage under the profile's limit.

## Verify
- [ ] Acrobat > Print Production > Output Preview shows the expected output intent.
- [ ] Total area coverage in images below the condition's limit (e.g. 300-330% coated, 260-300% uncoated).
- [ ] Printer's stated profile, preset name and paper all match.
