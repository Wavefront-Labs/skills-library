---
id: creative-arts.photography-fine-art.darkroom-practice.reading-characteristic-curves
name: reading-characteristic-curves
category: creative-arts
field: photography-fine-art
product: darkroom-practice
tags: [darkroom-practice, sensitometry, characteristic-curve, h-and-d-curve, contrast-index, gamma, toe-shoulder]
level: practitioner
status: draft
description: "Read film and paper characteristic (H&D) curves: toe, straight line, shoulder, gamma and contrast index, and use them to choose development and grade."
sources: ["Ansel Adams, The Negative (Little, Brown)", "https://en.wikipedia.org/wiki/Sensitometry"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reading characteristic curves

The **characteristic (H&D) curve** plots density (y) against log exposure (x).

## Parts
- **Base + fog**: density with no exposure.
- **Toe**: low exposures; shadows; gradual rise (low local contrast in shadows).
- **Straight line**: mid-tones; slope = gamma.
- **Shoulder**: high exposures; highlights compress (film usually has a long straight line; papers
  have strong shoulders).

## Measures
- **Gamma**: slope of the straight line.
- **Contrast index (CI)** (Kodak): average slope between a point 0.1 above FB+F and a point 2.0 log E
  units further - better represents the used part. Typical diffusion enlarger target CI ~0.56-0.62;
  condenser ~0.42-0.50.
- Datasheets show curves at several development times -> pick time for target CI.

## Using
1. More development = steeper curve = more contrast (N+).
2. Scene brightness range (in stops x 0.3 = log units) times CI gives negative density range.
3. Match to paper exposure scale (ISO range); choose grade accordingly.

## Gotchas
- Curves from datasheets are for their test conditions; your agitation and enlarger differ.
- Paper curves are reflection densities with Dmax limits.

## Verify
- [ ] You can predict negative density range for a scene and choose development to fit grade 2.
