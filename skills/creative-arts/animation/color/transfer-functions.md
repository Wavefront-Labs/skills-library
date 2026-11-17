---
id: creative-arts.animation.color.transfer-functions
name: transfer-functions
category: creative-arts
field: animation
product: color
tags: [transfer-function, scene-linear, linear-workflow, oetf, eotf, srgb, gamma-2-4, bt1886, pq, log, colour-science, double-gamma]
level: advanced
status: draft
description: "Understand and diagnose transfer functions (sRGB, BT.1886 gamma 2.4, log, PQ) across an animation pipeline; fix double-gamma and linear-as-display errors."
sources:
  - https://www.itu.int/rec/R-REC-BT.1886
  - https://opencolorio.readthedocs.io/en/latest/concepts/overview/overview.html
  - https://docs.acescentral.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Transfer functions

**Goal:** know at every step whether pixel values are linear light or encoded, and with which
curve, so nothing is decoded twice or not at all. A transfer function maps light to code values
(OETF, camera/encoding side) or code values to display light (EOTF, display side).

## The ones in an animation pipeline

| Curve | Where you meet it | Notes |
|---|---|---|
| Linear (scene-referred) | EXR renders, comp working space, ACEScg | 0.18 = mid grey; values above 1.0 are valid |
| sRGB piecewise (~2.2) | 8-bit textures (albedo), PNG/JPEG, UI, web | linear toe below 0.0031308 |
| BT.1886 (gamma 2.4) | HD video mastering displays, Rec.709 deliverables | the EOTF for broadcast SDR |
| BT.709 OETF | camera encoding; often confused with the display curve | not the inverse of BT.1886 |
| Log (ACEScct, LogC, ...) | grading space, film-style interchange | equal steps per stop |
| PQ (ST 2084), HLG | HDR deliverables | absolute (PQ) vs relative (HLG) |

## Classic errors and their look

| Look | Cause | Fix |
|---|---|---|
| washed out, low contrast | encoded data decoded as linear then encoded again (double gamma) | tag the input as its true curve (e.g. texture as sRGB, not linear) |
| very dark, crushed, harsh highlights | linear EXR shown with no view transform | apply the display/view transform (OCIO) |
| colour textures fine but roughness/normal maps wrong | data maps tagged sRGB | set non-colour data to Raw/Non-Color |
| slight contrast mismatch between QuickTime and Resolve | sRGB vs BT.1886 viewing assumption | pick a show standard, tag files (`creative-arts.animation.encode-delivery.colour-metadata-tags`) |

## Rules

1. Colour textures painted on screen: sRGB encoded. Data textures (normal, roughness, masks): raw.
2. Lighting, rendering, compositing: linear. Never grade or blur in an encoded space unless the
   tool is designed for it (grading in log is fine; compositing maths is not).
3. Encode for display only once, at view/output, through the OCIO display/view.
4. Every file written outside the linear core says what curve it is in (name, metadata, or both).

## Quick numeric check

Mid grey 0.18 linear should read about 0.46 in sRGB and about 0.49 in BT.1886 (gamma 2.4)
encoded output. In a viewer, sample a grey card: if you read 0.18 on an "sRGB" PNG, it was saved
linear; if you read 0.46 in an EXR, someone baked a curve into the render.

## Verify

Render a linear grey ramp and a 0.18 patch through the full chain (render, comp, grade, encode);
sample the final file: the patch lands on the expected code value for the delivery curve.
