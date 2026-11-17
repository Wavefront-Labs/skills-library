---
id: creative-arts.photography-fine-art.fine-art-printing.bronzing-gloss-differential-and-metamerism
name: bronzing-gloss-differential-and-metamerism
category: creative-arts
field: photography-fine-art
product: fine-art-printing
tags: [fine-art-printing, black-and-white-inkjet, gloss-differential, bronzing, metamerism, gloss-optimizer, chroma-optimizer, illuminant-shift]
level: practitioner
status: draft
description: "Diagnose and reduce bronzing, gloss differential and metamerism in pigment inkjet prints using gloss optimiser, paper choice, ink limits and viewing tests."
sources: ["https://www.usa.canon.com/ (PRO-1000 Chroma Optimizer)", "https://www.wilhelm-research.com/", "Jeff Schewe, The Digital Print (Peachpit)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Bronzing, gloss differential and metamerism

## Definitions
- **Bronzing**: a metallic, reddish/bronze sheen in dense dark areas of glossy pigment prints viewed at an angle.
- **Gloss differential**: uneven gloss between areas with different ink load (paper white areas shinier or
  duller than inked ones).
- **Metamerism (illuminant metamerism)**: colours shift under different lights - a neutral B&W print looks
  greenish under tungsten and magenta under daylight.

## Diagnosing
Look at the print at a raking angle under a point source for bronzing/gloss; compare the same print under
daylight-booth and tungsten/LED lamps for metamerism.

## Remedies
- **Gloss/Chroma optimiser** (clear coat ink on Canon PRO-1000/PRO-300 Chroma Optimizer, Epson models with
  Gloss Optimizer) evens gloss and reduces bronzing - set "Overall" rather than "Auto" for even gloss.
- Choose baryta/lustre papers with less bronzing tendency for your printer; matte papers don't bronze.
- Post-coat with a spray (Hahnemuhle Protective Spray, Premier Print Shield) to unify gloss.
- Reduce ink density in deep shadows (lower Max Optical Density in ABW or a profile with lower total ink).
- For metamerism: use ABW/QTR B&W modes (more black/grey inks), or a profile built for the display illuminant;
  view the final under the exhibition light.

## Verify
- [ ] Print shows even gloss at an angle and stays neutral under both D50 and 3000 K light.
