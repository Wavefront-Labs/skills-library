---
id: manufacturing-production.printing-production.print-colour-management.g7-calibration-icc-profiling-and-press-ok-decisions
name: g7-calibration-icc-profiling-and-press-ok-decisions
category: manufacturing-production
field: printing-production
product: print-colour-management
tags: [print-colour-management, colour-management, color-management, g7, idealliance, gracol, swop, iso-12647, iso-12647-2, fogra, fogra51, fogra39, icc-profile, profiling, characterisation, calibration, nprdc, grey-balance, gray-balance, spectrophotometer, x-rite, i1pro, techkon, delta-e, de2000, de76, cielab, m0, m1, m2, viewing-booth, iso-3664, d50, press-ok, colour-tolerance]
level: advanced
status: draft
description: "Keep print colour right proof to press: calibrate to G7 or ISO 12647, build and verify ICC profiles, measure correctly, and make defensible press-side colour OK calls."
sources: ["Idealliance G7 methodology (general reference)", "ISO 12647 series and ISO 13655 measurement conditions (general reference)", "ISO 3664 viewing conditions (general reference)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Print colour management: G7, ICC profiles and press OK decisions

**Goal:** make proofs and presses (offset, digital, flexo) agree, and decide at the
press with numbers plus eyes whether a sheet matches — so arguments become
measurements.

## 1. Measurement basics (get these wrong and nothing else matters)
- **Instrument:** a spectrophotometer (X-Rite i1Pro/eXact, Techkon SpectroDens,
  Barbieri, inline scanners). Calibrate it on its white tile per maker's schedule.
- **Measurement condition (ISO 13655):** **M0** (legacy, undefined UV), **M1** (D50
  incl. UV — for papers with optical brighteners), **M2** (UV cut). Proof, press and
  reference must use the **same** condition or ΔE values are meaningless.
- **Backing:** white or black backing as the standard specifies; be consistent.
- **ΔE formula:** state which — **ΔE2000** (ΔE00) is the modern standard; ΔE76 is
  larger for the same difference. "ΔE 3" without the formula is ambiguous.
- **Viewing:** ISO 3664 booth, D50, P1 condition for critical comparison; turn off
  other room lights near the booth.

## 2. Calibration: G7 vs ISO 12647 approaches
- **ISO 12647-2 (offset) / process control:** hit specified **solid Lab values** for
  CMYK on a defined paper type and a **tone value increase (TVI)** curve. Plate
  curves adjust TVI.
- **G7 (Idealliance):** calibrate so the press reproduces a **neutral print density
  curve (NPDC)** and **grey balance** defined in relation to the paper and solid
  densities. The press is printed with a **P2P target**, measured, and curves are
  calculated (e.g. Curve4/other G7-aware tools), applied to plates/RIP, then verified.
  Strength: devices with different solids still look alike in neutrals and tone.
- Verification levels in G7 (Grayscale, Targeted, Colorspace) define which
  tolerances must pass — check the current Idealliance spec.
- Calibrate first; **profile only a calibrated, stable device**.

## 3. ICC profiling
1. Print a characterisation chart (e.g. IT8.7/4 or ECI 2002) on the calibrated device
   and stock, with no colour management applied to the chart.
2. Measure; build the profile (i1Profiler, ColorLogic, etc.) setting **TAC** and
   **black generation (GCR/UCR)** to suit the process (heavier GCR stabilises grey on
   press).
3. Or, for a press calibrated to a standard, **use the standard characterisation
   data/profile** (e.g. FOGRA51 / GRACoL2013 / CRPC6) rather than a custom one — that is
   the point of printing to a standard.
4. Verify: print a control strip/test form through the profile, measure, compare to
   reference. Re-profile only when calibration can't bring it back.

## 4. The press-side OK decision
Decide with a sequence, not a feeling:
1. **Substrate:** is the paper white what the proof simulated? If not, expectations
   must shift (and the proof should have used the right paper simulation).
2. **Solids** within tolerance of target (e.g. a few ΔE00 for primaries; your
   contract/standard sets the numbers).
3. **Grey balance/NPDC** close — neutrals are what eyes notice first.
4. **Spot/brand colours** within the brand owner's tolerance; measured, not judged by
   eye only.
5. **Visual** comparison to the contract proof in the booth: skin tones, key product
   colours, defects.
6. If numbers pass and the customer still dislikes it, document the measurements and
   what was changed at their request; that sheet becomes the new OK.

## Gotchas
- Measuring wet sheets: values shift on drying (dry-back). Use a known wet-to-dry
  offset or measure dry samples for compliance.
- Mixed measurement conditions between proof (M1) and press (M0) give phantom ΔE.
- Profiles cannot fix an unstable press — fix process variation (ink-water,
  dampening, TVI drift) first.
- Optical brighteners make papers look bluer under UV-rich light; D50 booths with
  correct UV content reduce proof/press disagreement.

## Verify
- [ ] Instrument calibrated; measurement condition and ΔE formula stated on every report.
- [ ] Device calibrated (G7 or ISO) and verified before any profiling.
- [ ] Profile or standard characterisation chosen deliberately and verified on a test form.
- [ ] OK sheet decision recorded with measurements (solids, grey, spots) plus visual.
- [ ] Booth meets ISO 3664 (D50) and is used for every visual judgement.

*Draft note:* G7 tolerance levels and tool names change between spec revisions; check
the current Idealliance documentation before certifying.
