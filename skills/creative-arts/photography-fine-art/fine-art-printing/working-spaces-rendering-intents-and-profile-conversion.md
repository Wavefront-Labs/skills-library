---
id: creative-arts.photography-fine-art.fine-art-printing.working-spaces-rendering-intents-and-profile-conversion
name: working-spaces-rendering-intents-and-profile-conversion
category: creative-arts
field: photography-fine-art
product: fine-art-printing
tags: [fine-art-printing, color-management, working-color-space, rendering-intent-choice, convert-to-profile, prophoto-rgb, black-point-compensation, assign-profile]
level: practitioner
status: draft
description: "Choose working colour space (ProPhoto, Adobe RGB, sRGB), pick perceptual vs relative colorimetric with BPC per image, and assign vs convert correctly."
sources: ["https://helpx.adobe.com/photoshop/using/converting-colors.html", "Jeff Schewe, The Digital Print (Peachpit)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Working spaces, rendering intents and profile conversion

## Working space
| Space | Use |
|---|---|
| **ProPhoto RGB, 16-bit** | raw-to-print fine-art workflow; holds all printable colours (Lightroom's internal space is similar) |
| Adobe RGB (1998) | covers most inkjet gamut; OK in 8-bit for many images |
| sRGB | web, many labs; clips saturated printable cyans/greens |
Use 16-bit with ProPhoto - 8-bit ProPhoto bands in smooth gradients.

## Rendering intents (for out-of-gamut colours)
- **Perceptual**: compresses the whole gamut to fit; keeps relationships; may desaturate in-gamut colours.
  Good for saturated images with lots out of gamut.
- **Relative colorimetric + Black Point Compensation (BPC)**: keeps in-gamut colours exact, clips out-of-gamut;
  BPC maps black to paper black (essential, keeps shadow detail). Default for most well-behaved images.
- Saturation: graphics. Absolute colorimetric: simulates paper white - proofing only.
Choose per image by soft proofing both.

## Assign vs convert
- **Assign profile**: changes how numbers are interpreted (appearance changes) - only to fix untagged/mis-tagged files.
- **Convert to profile** (Edit > Convert to Profile): changes numbers to keep appearance - use when sending to
  sRGB for web or to a lab's required space, with the chosen intent and BPC on.

## Gotchas
- Photoshop Color Settings: preserve embedded profiles; warn on mismatches.
- Sending ProPhoto files to labs that expect sRGB leads to dull or wild colour.

## Verify
- [ ] Files carry an embedded profile; conversions done with intent/BPC chosen from soft proof.
