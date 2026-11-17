---
id: creative-arts.animation.color.hdr-pq-hlg
name: hdr-pq-hlg
category: creative-arts
field: animation
product: color
tags: [pq-hlg, hdr, pq, st-2084, hlg, bt2100, nits, hdr-grading, rec2020, davinci-resolve, hdr10]
level: advanced
status: draft
description: "Choose and set up PQ or HLG HDR mastering for animation: absolute vs relative transfer, peak nits, Resolve colour management, reference display needs."
sources:
  - https://www.itu.int/rec/R-REC-BT.2100
  - https://partnerhelp.netflixstudios.com/hc/en-us
  - https://documents.blackmagicdesign.com/UserManuals/DaVinci_Resolve_19_Reference_Manual.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# HDR with PQ and HLG

**Goal:** an HDR master that uses the extra range deliberately (speculars, glows, magic FX, neon)
while the story-critical image sits where SDR viewers will also see it well.

## PQ vs HLG

| | PQ (SMPTE ST 2084) | HLG (ARIB STD-B67) |
|---|---|---|
| Nature | absolute: code value = nits | relative: scene-referred, display adapts |
| Used by | streaming (HDR10, Dolby Vision), cinema HDR | broadcast (BBC, NHK), live |
| Metadata | static (HDR10) or dynamic (DV, HDR10+) | none needed |
| SDR compatibility | needs a separate SDR trim/derived version | backward-compatible-ish on SDR displays |

Streaming animation is PQ (with Dolby Vision for Netflix originals that contract it).

## Setup in Resolve (colour-managed)

- Project Settings - Colour Management: DaVinci YRGB Colour Managed or ACES.
- Output colour space: Rec.2100 ST2084 (PQ), timeline in a wide gamut (DaVinci Wide Gamut /
  ACEScct). Output gamut Rec.2020 with mastering limited to P3-D65 (the common streaming spec:
  "P3-D65 limited, Rec.2020 container").
- Mastering peak: 1000 nits is the standard mastering target; set the timeline/output tone mapping
  to match the reference display.
- Monitor via a video I/O card into a PQ-capable reference monitor (1000-nit class). An HDR
  consumer TV or a laptop is not a mastering display.

## Grading approach for animation

- Place diffuse white (paper, white shirts, sky key) around 100-200 nits, not at peak. Faces and
  key story elements stay near SDR levels.
- Reserve 400-1000 nits for emitters: lasers, magic, sun glints, neon. Overusing peak causes
  fatigue and makes SDR trims hard.
- Saturated animated colours can exceed P3 when pushed in a wide working space; watch gamut
  warnings and the CIE scope.

## Gotchas

- Renders must be scene-linear with highlights above 1.0 preserved (EXR half); 8-bit display-
  referred renders cannot be promoted to real HDR.
- Viewing PQ on an SDR display without tone mapping looks dark and flat; it is the monitoring that
  is wrong.
- HLG and PQ masters are not interchangeable by retagging.

## Verify

Check on the reference display: MaxCLL/MaxFALL measured (Resolve: Analyse HDR) within spec, diffuse
white consistent across a sequence, and the SDR derivative (`creative-arts.animation.color.hdr-to-sdr-tone-mapping`)
reviewed.
