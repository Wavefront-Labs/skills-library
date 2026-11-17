---
id: creative-arts.photography-fine-art.fine-art-printing.lab-file-preparation-and-test-prints
name: lab-file-preparation-and-test-prints
category: creative-arts
field: photography-fine-art
product: fine-art-printing
tags: [fine-art-printing, lab-printing, lab-file-preparation, lab-test-print, lab-soft-proof-profile, print-ordering, bleed]
level: practitioner
status: draft
description: "Prepare files for a professional print lab (size, ppi, colour space, sharpening, bleed) and order test strips and proofs before the full print run."
sources: ["https://www.whcc.com/ (lab file specs)", "https://www.metroimaging.co.uk/ (fine art lab file guidelines)", "Jeff Schewe, The Digital Print (Peachpit)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Lab file preparation and test prints

## Ask the lab first
- Required file type (TIFF 8/16-bit, JPEG max quality), colour space (sRGB, Adobe RGB, or their profile),
  resolution (often 300 ppi at final size; Lambda/LightJet 200-400 ppi native), bleed and border handling.
- Download their **printer/paper ICC profile** for soft proofing (many fine-art labs publish them).
- Does the lab colour-correct? Ask for "no corrections" if you've soft proofed.

## Prepare
1. Duplicate the master; flatten; crop to exact aspect ratio of the print size.
2. Resize to final dimensions at the lab's ppi (Photoshop Image Size, Preserve Details 2.0 for upscaling).
3. Output sharpening for size/paper (light for matte, more for gloss; judge at 50% view).
4. Convert to the lab's requested space (Convert to Profile, chosen intent, BPC).
5. Add bleed/border as specified; name file with size and paper (e.g. title_50x60_baryta.tif).

## Test prints
- Order a **test strip** (crop of key areas) or small proof on the final paper before a large print.
- Evaluate under viewing light after dry-down; adjust and re-order if needed.
- Keep the approved proof as the reference for the edition.

## Gotchas
- Embedded wrong profiles or untagged files are the main cause of surprises.
- Large upsizing reveals noise and sharpening artefacts - test strip catches it.

## Verify
- [ ] File meets lab spec; approved proof on file before ordering the edition.
