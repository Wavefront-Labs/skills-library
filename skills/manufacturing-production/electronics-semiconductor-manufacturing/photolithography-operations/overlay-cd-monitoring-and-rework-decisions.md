---
id: manufacturing-production.electronics-semiconductor-manufacturing.photolithography-operations.overlay-cd-monitoring-and-rework-decisions
name: overlay-cd-monitoring-and-rework-decisions
category: manufacturing-production
field: electronics-semiconductor-manufacturing
product: photolithography-operations
tags: [photolithography-operations, photolithography, litho, lithography, scanner, stepper, asml, nikon, canon, track, tel, coater-developer, photoresist, resist, overlay, critical-dimension, cd, cd-sem, overlay-metrology, kla, archer, focus, dose, fem, focus-exposure-matrix, apc, run-to-run, rework, resist-strip, ash, hotspot, defect-inspection, semiconductor, fab]
level: practitioner
status: draft
description: "Run a litho cell's daily metrology loop: read overlay and CD results, tell scanner, track and reticle causes apart, use APC corrections sensibly, and decide when to strip and rework a lot."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Overlay and CD monitoring and rework decisions

**Goal:** catch a bad litho exposure while it can still be reworked. Lithography is the
one major fab step that is routinely **reversible**: resist can be stripped and the
wafer re-coated and re-exposed. Once the wafer goes to etch or implant, the pattern
is permanent. So litho metrology is the last cheap gate.

## 1. The measurement loop
After develop, sample wafers per lot are measured for:
- **Overlay** — alignment of this layer to previous layers (box-in-box, AIM or
  diffraction-based targets on e.g. KLA Archer-class tools). Reported as x/y mean
  + 3σ, and decomposed into model terms (translation, rotation, magnification,
  higher-order) per field and per wafer.
- **CD** (critical dimension) — line/space width on a CD-SEM or by scatterometry.
- **Macro/defect inspection** — coating defects, comets, striations, focus spots,
  missing exposure fields.
The results feed an **APC/run-to-run** controller that adjusts scanner overlay and
dose for the next lot, and the lot's pass/rework decision.

## 2. Reading the signature
| Symptom | Likely source |
|---|---|
| Whole-wafer overlay translation/rotation | Wafer alignment, previous-layer tool difference, wrong APC context |
| Field-level magnification/rotation repeated every field | Reticle or scanner lens/stage setup, reticle heating |
| Overlay bad only at wafer edge | Wafer warp/bow from prior process, clamping |
| Single bad field / spot | Focus spot (particle on chuck or wafer backside), hot spot |
| CD shift across whole lot | Dose, resist batch, track bake (PEB) temperature, develop |
| CD across-wafer pattern (radial) | Track hotplate or coat uniformity, develop nozzle |
| CD + focus both off at one chuck | Scanner chuck contamination (dual-stage tools: compare chucks) |
Comparing **per-chuck, per-track-module and per-reticle** splits finds most root causes
fast; the MES or metrology database usually lets you filter by context.

## 3. APC — use it, don't fight it
- Make sure lots run with the right **context** (layer, product, tool, reticle);
  wrong context = wrong correction applied.
- After a PM, reticle change or new product, APC has no history — many fabs require
  a **send-ahead/pilot wafer** before the lot. Don't skip it.
- Manual overrides of APC corrections must be documented; they poison the feedback
  history.

## 4. Rework decision
Disposition per the layer's spec and the OCAP:
- Measured lot out of spec, or defect inspection fails → **rework**: strip resist
  (ash and/or wet strip), clean, re-coat, re-expose with corrected settings, re-measure.
- Check the **rework count**: many layers allow only a limited number of reworks
  (each strip can damage underlying films or change CD).
- Underlying film must survive the strip chemistry — some layers can't be reworked
  safely; know which.
- Rework the whole lot when the cause is systematic; a single wafer if it is a
  one-off (e.g. focus spot).
- Fix the cause *before* re-exposing the reworked wafers on the same tool.

## Gotchas
- Metrology target quality (damaged targets, CMP-eroded marks) gives false overlay
  values — check the target image/fit quality flags.
- Resist is time-sensitive: delay between coat, expose and post-exposure bake can
  shift CD (especially chemically amplified resists). Watch queue times.
- Ambient amine contamination degrades chemically amplified resist (T-topping);
  track environmental alarms matter.

## Verify
- [ ] Every lot measured per sampling plan before release to etch.
- [ ] Out-of-spec lots dispositioned (rework/hold), not passed on.
- [ ] Rework count within the layer's limit; reworked lots re-measured.
- [ ] Root cause split by chuck/track/reticle identified before resuming.

*Draft: tool names illustrative; specs, sampling and rework limits are layer- and
fab-specific and not given numerically here.*
