---
id: creative-arts.photography-fine-art.fine-art-printing.soft-proofing-paper-choice-and-editioning
name: soft-proofing-paper-choice-and-editioning
category: creative-arts
field: photography-fine-art
product: fine-art-printing
tags: [fine-art-printing, inkjet-printing, pigment-printing, giclee, archival-pigment-print, monitor-calibration, colour-management, icc-profile, paper-profile, soft-proofing, rendering-intent, perceptual, relative-colorimetric, black-point-compensation, matte-paper, baryta, fibre-paper, cotton-rag, photo-black, matte-black, printer-driver, colour-management-off, edition, limited-edition, certificate-of-authenticity, signing, print-viewing-booth]
level: practitioner
status: draft
description: "Making exhibition inkjet prints: calibrated monitor, ICC paper profiles, soft-proofing and rendering intents, paper choice (matte vs baryta), print settings, and editioning and signing conventions."
sources: ["Andrew Rodney, Color Management for Photographers", "Paper manufacturer profiles and guides (Hahnemühle, Canson, Ilford)", "Edition conventions vary by market; see notes"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Soft proofing, paper choice and editioning

**Goal:** a print that matches your intention (not just your screen), on the right
paper, produced as a controlled, documented edition.

## 1. Calibrate the screen first
- Use a hardware calibrator. For print work a common target is **D65 white point,
  gamma 2.2, luminance around 80–120 cd/m²** — much dimmer than factory settings.
  The #1 cause of "prints too dark" is an over-bright monitor.
- Evaluate prints under controlled light (around D50/5000 K viewing booth or good
  daylight-balanced lamps) at a brightness similar to the exhibition.

## 2. Choose the paper
| Type | Look | Black density | Use |
|---|---|---|---|
| Matte cotton rag | soft, no glare | lower (use Matte Black ink) | painterly, quiet images |
| Baryta / fibre gloss | darkroom-like sheen | high (Photo Black) | B&W, high detail |
| Lustre/pearl RC | modest sheen | high | proofs, budget |
- **OBA-free** (no optical brighteners) papers age more predictably; OBA papers look
  whiter at first but can shift over time.
- Order a **sample pack** and print the same test image on 3–4 papers.

## 3. Profiles and soft proofing
- Download the **ICC profile** for your exact printer + paper + ink combination from
  the paper maker (or make a custom one).
- Soft-proof in Lightroom (Develop › Soft Proofing, `S`) or Photoshop (View › Proof
  Setup). Turn on **Simulate Paper & Ink** to see reduced contrast and paper white.
- **Rendering intent:** *Perceptual* compresses all colours to fit (good for saturated
  images); *Relative Colorimetric* with **Black Point Compensation** keeps in-gamut
  colours accurate (good for most photos). Compare both.
- Make a **proof copy** with adjustments for that paper (often a little more
  brightness/contrast for matte). Keep it separate from the master.

## 4. Print settings
- **Application manages colour; the printer driver colour management OFF.** If both
  manage (or neither), colour is wrong — the most common print error.
- Select the paper's **media type** in the driver as the profile maker specifies;
  highest quality, no "high speed" bidirectional printing for finals.
- Print at native resolution (often 300 or 360 ppi depending on brand — check);
  apply output sharpening for the paper type.
- Let prints **dry down** 24 h before final judgement; colour and density shift.

## 5. Editioning
- Decide edition size and **sizes per edition** before selling the first print and
  never exceed them. Artist's proofs (APs) are usually a small additional number
  (often around 10% of the edition) — conventions vary.
- Sign and number on the back or margin with an archival pencil/pen, e.g. "3/10".
- Keep an **edition log**: number, size, paper, date printed, buyer (privately), file
  version. Issue a certificate of authenticity with the same data.
- Some jurisdictions have laws on disclosing multiples' edition details — check
  where you sell.

## Gotchas
- Mixing Photo Black and Matte Black papers causes ink-swap waste on some printers;
  batch by paper type.
- Clogged nozzles produce banding — print a nozzle check before final runs.
- Uncertain: calibration targets and AP percentages are common practice, not
  standards.

## Verify
- [ ] Monitor calibrated within the past month at print-oriented brightness.
- [ ] Soft proof made with the correct ICC profile and intent.
- [ ] Driver colour management off; app manages colour.
- [ ] Nozzle check clean; print evaluated after dry-down under proper light.
- [ ] Edition logged, numbered and documented.
