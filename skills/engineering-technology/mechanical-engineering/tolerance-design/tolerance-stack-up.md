---
id: engineering-technology.mechanical-engineering.tolerance-design.tolerance-stack-up
name: tolerance-stack-up
category: engineering-technology
field: mechanical-engineering
product: tolerance-design
tags: [tolerance-stack-up, tolerance-analysis, worst-case, rss, root-sum-square, statistical-tolerancing, monte-carlo, gd-and-t, gdt, asme-y14-5, iso-1101, datum, position-tolerance, mmc, bonus-tolerance, floating-fastener, fixed-fastener, iso-286, limits-and-fits, cpk, loop-diagram]
level: advanced
status: verified
description: "1-D tolerance stack-up: loop diagram, worst-case vs RSS, converting GD&T to ± contributors, floating/fixed fastener formulas, and ISO 286 fit choice."
sources: ["ASME Y14.5-2018 Dimensioning and Tolerancing", "Fischer, Mechanical Tolerance Stackup and Analysis (CRC Press)", "ISO 286-1 and ISO 286-2 Geometrical product specifications — ISO code system for tolerances on linear sizes", "Drake, Dimensioning and Tolerancing Handbook (McGraw-Hill)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Tolerance stack-up — will it fit, every time?

**Goal:** determine the minimum and maximum of a functional gap (clearance, interference,
alignment) from the drawing tolerances, decide whether worst-case or statistical
analysis applies, and re-allocate tolerances where the result fails.

## 1. Define the requirement and the loop
1. Name the gap and its requirement (e.g. "axial clearance 0.1–0.6 mm").
2. Draw a **loop diagram**: start at one side of the gap, walk through each part's
   dimension along the shortest chain of contacting features back to the other side.
   Choose a positive direction (e.g. right/up = +).
3. Every link must be a dimension that actually exists on a drawing, measured from the
   datum features that locate the part in the assembly. If the drawing's datum scheme
   doesn't match how parts mate, fix the drawing — that's the real finding.
4. Fewest links wins: each extra part in the chain adds tolerance.

## 2. Convert everything to mean ± equal-bilateral
Convert `20 +0.1/-0.0` to `20.05 ± 0.05`. Geometric tolerances become ± contributors:
- Position Ø0.2 on a feature -> ±0.1 on its location.
- Profile 0.3 (equal-bilateral) -> ±0.15.
- Flatness/parallelism contribute only if they act in the loop direction.
- Clearance between a hole and a pin/shaft that floats: mean radial clearance becomes a
  contributor of ± (clearance range / 2) around the mean offset — or worst-case,
  assume parts biased to the side that hurts.
- **Bonus tolerance** at MMC: use the full available tolerance at LMC in worst-case.

## 3. Worst-case
`Gap_nominal = sum(signed nominals)`; `T_wc = sum(|t_i|)`. Gap range = nominal ± T_wc.
Guarantees 100 % assembly if every part is in tolerance. Use it for safety-critical
fits, few contributors (≤ ~4), or low volumes.

## 4. Statistical (RSS)
`T_rss = sqrt(sum(t_i^2))` assumes independent, normally distributed, centred
dimensions with each tolerance = ±3 sigma. With 5 equal ±0.1 contributors: worst-case
±0.5, RSS ±0.22 (computed: 0.2236; Bender 1.5 × RSS = 0.335).
- Reality is rarely centred: apply an inflation factor (Bender's 1.5 x RSS is a common
  conservative choice (gated: unconfirmed, source is paywalled or blocked)) or use a **modified RSS** with Cpk-based sigmas.
- RSS with fewer than ~4–5 contributors is optimistic.
- For non-linear stacks (angles, radial-to-linear projections) use sensitivities
  `dGap/dx_i` as multipliers, or **Monte Carlo** (10^5+ samples, real distributions);
  tools include CETOL, 3DCS, VisVSA and spreadsheet models.
- Statistical results are only valid when suppliers have process control (SPC, Cpk ≥ 1.33 (gated: unconfirmed, source is paywalled or blocked));
  tell them the dimension is statistically toleranced (Y14.5 has a statistical symbol).

## 5. Fastener formulas (ASME Y14.5 appendix approach)
- **Floating fastener** (bolt through clearance holes in both parts, nut): position
  tolerance per part `T = H - F` (H = MMC hole, F = MMC fastener).
  M8 bolt (F = 8.0) in 9.0 holes -> T = Ø1.0 on each part (arithmetic checked; the ASME Y14.5 floating/fixed fastener formulas are paywalled (gated: unconfirmed, source is paywalled or blocked)).
- **Fixed fastener** (one part tapped/pressed): `T1 + T2 = H - F`, usually
  `T = (H - F)/2` each -> Ø0.5. Add a **projected tolerance zone** on the threaded hole
  when the mating part is thick, otherwise thread tilt eats the clearance.

## 6. Fits (ISO 286 hole-basis)
Choose a fit rather than inventing ± values. Common hole-basis choices (gated: unconfirmed, source is paywalled or blocked): H8/f7 running;
H7/g6 sliding/close location; H7/h6 locational clearance; H7/k6 or H7/n6 transition;
H7/p6 light press; H7/s6 medium drive. For Ø25: H7 = 0/+0.021, g6 = -0.007/-0.020,
p6 = +0.022/+0.035 (internally consistent with IT6 = 13 µm and IT7 = 21 µm for 18–30 mm, but ISO 286 is paywalled (gated: unconfirmed, source is paywalled or blocked); check tables or a fit calculator for your size range).

## 7. If the stack fails
Order of attack: shorten the chain (fewer parts, better datums), tighten the
**largest** contributors (RSS is dominated by them), add an adjustment
(shims, slots, select-fit), and only then tighten everything.

## Verify
- [ ] Loop diagram uses only dimensions on drawings, from mating datums.
- [ ] All tolerances converted to mean ± equal-bilateral; GD&T and clearances included.
- [ ] Worst-case result reported; statistical result used only with justification (contributors, Cpk).
- [ ] Gap min/max compared with the functional requirement, with % contribution per link.
- [ ] Fastener position tolerances satisfy floating/fixed formulas; projected zones where needed.
