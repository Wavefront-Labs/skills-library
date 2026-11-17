---
id: creative-arts.comics-and-sequential-art.comic-colouring.soft-proofing-and-printed-proofs-for-comics
name: soft-proofing-and-printed-proofs-for-comics
category: creative-arts
field: comics-and-sequential-art
product: comic-colouring
tags: [comic-colouring, print-colour, cmyk-comics, soft-proofing, print-proof, monitor-calibration, paper-white, hard-proof]
level: practitioner
status: draft
description: "Predict printed colour before the run: calibrate the monitor, soft-proof with the printer profile and paper simulation, order a hard/printed proof, and check it under good light."
sources:
  - https://helpx.adobe.com/photoshop/using/proofing-colors.html
  - https://www.ingramspark.com/hubfs/downloads/file-creation-guide.pdf
  - https://openlibrary.org/search?q=DC+Comics+Guide+to+Coloring+and+Lettering+Comics
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Soft proofing and printed proofs

**Goal:** no surprises when the printed book arrives: too dark, too dull, or colour-cast.

## 1. Calibrate the monitor
- Use a hardware colorimeter; target roughly D65 white and a **lower brightness**
  (around 80-120 cd/m2) for print work. Bright monitors make colourists colour too dark.
- Re-calibrate monthly.

## 2. Soft proof
- Photoshop: View > Proof Setup > Custom: device = the printer's profile, intent as
  you'll convert, enable **Simulate Paper Color** (and Black Ink). The image dulls:
  that's the point.
- Toggle proof (Ctrl/Cmd+Y) while adjusting; fix shadows that block up and blues that
  shift purple.
- For uncoated/newsprint-like paper, expect much lower contrast and darker midtones
  (dot gain); lighten midtones.

## 3. Printed proofs
- **Contract/hard proof** from the printer (calibrated inkjet simulating the press) or
  a **digital printed copy** for POD. Order one before a large run.
- Inspect under consistent, daylight-balanced light, not a warm desk lamp.
- Check: shadow detail, skin tones, line art sharpness, lettering, trim/bleed, page
  order.

## 4. Common adjustments after proofing
- Dark pages muddy: open shadows, reduce total ink.
- Colours flat on uncoated stock: boost contrast in RGB before reconverting.
- Line art fringing: lines not K-only.

## Verify
- [ ] Monitor calibrated recently at print brightness.
- [ ] Soft proof reviewed with paper simulation.
- [ ] Physical proof approved before the run.
