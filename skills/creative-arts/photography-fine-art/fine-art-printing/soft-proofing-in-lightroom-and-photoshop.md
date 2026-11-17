---
id: creative-arts.photography-fine-art.fine-art-printing.soft-proofing-in-lightroom-and-photoshop
name: soft-proofing-in-lightroom-and-photoshop
category: creative-arts
field: photography-fine-art
product: fine-art-printing
tags: [fine-art-printing, soft-proofing, simulate-paper-and-ink, gamut-warning, proof-copy, proof-setup, lightroom-soft-proofing]
level: practitioner
status: draft
description: "Soft proof prints in Lightroom and Photoshop: printer/paper profile, simulate paper and ink, gamut warnings, and proof copies with proof-specific adjustments."
sources: ["https://helpx.adobe.com/lightroom-classic/help/soft-proofing.html", "https://helpx.adobe.com/photoshop/using/proofing-colors.html", "Jeff Schewe, The Digital Print (Peachpit)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Soft proofing in Lightroom and Photoshop

## Lightroom Classic
1. Develop module: press **S** (or tick Soft Proofing under the image). Background turns paper-white.
2. Choose the printer/paper **Profile** (Other... to enable installed profiles), **Intent** (Perceptual / Relative).
3. Tick **Simulate Paper & Ink**: shows paper white and black ink density - image looks flatter (that's reality).
4. Gamut warnings: the icons top left (monitor) and top right (**destination**) of the histogram - red overlay
   marks colours the printer can't reproduce.
5. Click **Create Proof Copy** - a virtual copy for that paper; adjust it (often +contrast, +saturation, slight
   brightening of shadows) to look like the master *on that paper*.
6. Print the proof copy with the same profile/intent.

## Photoshop
1. View > Proof Setup > Custom: Device to Simulate (paper profile), Rendering Intent, BPC on, **Simulate Paper Color**.
2. Ctrl/Cmd+Y toggles proof; Shift+Ctrl/Cmd+Y toggles **Gamut Warning**.
3. Do proof-specific adjustments on separate adjustment layers (group named for the paper) - turn on for that print.
4. Window > Arrange > New Window to see proof and non-proof side by side.

## Gotchas
- Gamut warning overlays tend to scare - small out-of-gamut areas in saturated subjects are normal; judge visually.
- Soft proof is only as good as your display calibration and the paper profile.

## Verify
- [ ] Proof copy/adjustment layer named per paper; first print matches the soft proof under viewing light.
