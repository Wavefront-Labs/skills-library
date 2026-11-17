---
id: creative-arts.visual-art.printmaking.screenprint-colour-separations-and-film-positives
name: screenprint-colour-separations-and-film-positives
category: creative-arts
field: visual-art
product: printmaking
tags: [visual-art, printmaking, screenprinting, screen-printing, colour-separations, film-positive, halftone, trapping, inkjet-film, registration-marks, spot-colour]
level: practitioner
status: draft
description: "Make colour separations and film positives for screenprinting: spot-colour layers, hand-drawn positives, inkjet film, halftones and LPI for mesh, trapping and registration marks."
sources: ["https://www.speedballart.com/", "https://www.ryonet.com/", "https://www.bloomsbury.com/uk/printmaking-9781856697118/", "https://www.sefar.com/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Screenprint colour separations and film positives

Each colour needs its own screen, so each needs a separate **positive**: an opaque black image on clear film, exposed onto emulsion. Black blocks UV, leaving stencil open where ink will print.

## Separate the artwork
- **Spot colour**: one layer per ink in the design file (or one drawing per colour). Each layer becomes pure black at 100% opacity.
- Order: typically light to dark, with the key (black line) last.
- **Trapping**: extend lighter colours slightly under darker ones (e.g. 0.5-1 mm) so small misregistration doesn't leave white gaps.
- Add **registration marks** (crosshairs) outside the image on every layer, identical positions.

## Hand-drawn positives
- Draw on drafting film (matt polyester) or tracing with opaque media: drawing ink, opaque marker, litho crayon, grease pencil, Indian ink washes, cut Rubylith/amberlith masking film.
- Hold up to light: anything not truly opaque under-exposes and partially washes out - test on a step wedge.

## Digital positives
- Print on inkjet or laser **film** in black only, maximum density. Many studios use a RIP or the printer's highest black density, or print twice and overlay.
- Print the positive right-reading (unmirrored); it is placed on the screen so the image reads correctly from the print side.
- **Halftones** for tonal images: convert to bitmap halftone dots. Pick a line screen (LPI) to suit the mesh: around 45-65 LPI on 110-160 threads/inch (43-62 threads/cm) mesh is common for art printing; mesh count should be roughly 4-5 times the LPI. Use a dot angle (e.g. 22.5 or 45 degrees) to reduce moire with the mesh.

## Gotchas
- **Grey, not black** positives give soft, washed-out stencils.
- Halftone dots too fine for the mesh fall through or close up.
- Separations without registration marks are very hard to line up.

## Verify
- [ ] Every colour layer black, opaque, with identical registration marks.
- [ ] Trapping added where colours meet.
- [ ] Halftone LPI matched to mesh; moire checked.
