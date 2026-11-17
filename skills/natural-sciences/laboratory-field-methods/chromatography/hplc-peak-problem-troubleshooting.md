---
id: natural-sciences.laboratory-field-methods.chromatography.hplc-peak-problem-troubleshooting
name: hplc-peak-problem-troubleshooting
category: natural-sciences
field: laboratory-field-methods
product: chromatography
tags: [chromatography, hplc, uhplc, reversed-phase, c18, peak-tailing, peak-fronting, split-peaks, broad-peaks, ghost-peaks, retention-time-drift, baseline-drift, baseline-noise, backpressure, system-suitability, tailing-factor, resolution, plate-count, mobile-phase, buffer-ph, sample-solvent, guard-column, column-void, dead-volume, degassing, troubleshooting]
level: practitioner
status: draft
description: "Diagnose HPLC problems from the chromatogram: tailing, fronting, split or ghost peaks, retention drift, pressure changes and baseline noise, isolating column vs system vs method one change at a time."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# HPLC peak-problem troubleshooting

**Goal:** get back to sharp, symmetric, reproducible peaks by working out whether the
problem lives in the sample, the method, the column or the instrument — changing one
thing at a time and checking against a known-good reference.

## 1. First questions
- **What changed?** New column, mobile phase batch, sample prep, instrument service.
- **Does it affect all peaks or only some?** All peaks → physical/system (column inlet,
  dead volume, flow). Some peaks → chemical (pH, secondary interactions, co-elution).
- **Compare with a system-suitability or reference chromatogram** — tailing factor,
  plate count, retention time and pressure on a good day are your baseline. Keep one.

## 2. Symptom table
| Symptom | All peaks? | Likely cause | Try |
|---|---|---|---|
| **Tailing** | Only basic analytes | Silanol interaction | Lower pH (~2–3) or add buffer strength; end-capped/modern high-purity column |
| Tailing | All | Blocked inlet frit, column void, extra-column volume | Reverse-flush (if allowed), replace guard, check fittings/tubing |
| **Fronting** | Often | Column overload (mass or volume), sample solvent stronger than mobile phase | Inject less; dissolve sample in mobile phase |
| **Split/shoulder peaks** | All | Partially blocked frit or void at column head | Replace guard/column; check for sample precipitation |
| Split | One | Co-elution or sample solvent mismatch | Change gradient; weaker injection solvent |
| **Broad peaks** | All | Dead volume, wrong tubing ID, low temperature, aged column | Shorter/narrower tubing; column oven |
| **Ghost peaks** | — | Carryover, contaminated mobile phase, late eluters from previous run | Blank injection; needle wash; extend gradient/wash |
| **Retention drifts** | All, gradually | Insufficient equilibration, temperature, evaporation of organic, pH drift | ≥ ~10 column volumes equilibration; column oven; fresh, capped mobile phase |
| Retention jumps | All, suddenly | Flow rate/pump issue, leak, wrong mobile phase | Check pressure trace, leaks, check valves |

Tailing factor (USP T) ≤ ~1.5 is commonly acceptable; many methods specify ≤ 2.0.

## 3. Pressure
- **High pressure:** isolate by disconnecting from the detector backwards — remove the
  column (replace with a union): if pressure drops to normal, it's the column (or guard);
  if not, a blocked inline filter or tubing upstream.
- **Low or fluctuating pressure:** air in the pump, failing check valve, leak. Purge the
  pump, check degasser, look for wet fittings or salt crystals.
- Pressure ripple that tracks pump strokes points to a check valve or seal.

## 4. Baseline problems
- **Drift during gradient** at low UV wavelength: mobile-phase absorbance mismatch;
  match additive (e.g. 0.1 % TFA in both A and B), or use a higher wavelength.
- **Noise/spikes:** air bubbles (degas, back-pressure regulator on the detector outlet),
  failing lamp (check lamp hours/energy), dirty flow cell.
- **Wander:** temperature fluctuation — use the column oven and keep the detector away from drafts.

## 5. Mobile phase hygiene
- Buffers: prepare fresh, filter (0.2–0.45 µm), measure pH of the **aqueous** portion
  before adding organic. Choose a buffer within ±1 pH of its pKa.
- Never let buffer meet high organic in the lines without flushing — salts precipitate
  (phosphate in > ~80 % acetonitrile is a classic).
- Flush buffered systems with water then storage solvent (as the column datasheet
  specifies) at the end of the day.

## 6. Protect the column
Use a guard column or inline filter; filter or centrifuge samples; respect the column's
pH and pressure limits. Keep a column log (injections, pressure, plate count) to see
degradation trends.

## Gotchas
- Fix one thing at a time and re-inject the reference standard after each change.
- Reverse-flushing is not allowed for all columns (some UHPLC columns) — check the datasheet.
- Sample diluent stronger than the starting mobile phase is the single most common cause
  of distorted early peaks.
- Some "column problems" are actually a mis-made mobile phase; re-make it before buying a column.

Uncertain here: acceptance limits vary by method and pharmacopoeia; use the values in your
validated method.

## Verify
- [ ] Reference standard meets system suitability (retention, tailing, plates, resolution).
- [ ] Pressure back to the logged normal for this column and flow.
- [ ] Blank injection shows no ghost peaks or carryover above your limit.
- [ ] Root cause recorded in the instrument/column log.
