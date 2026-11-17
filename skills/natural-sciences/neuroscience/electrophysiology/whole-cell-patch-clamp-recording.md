---
id: natural-sciences.neuroscience.electrophysiology.whole-cell-patch-clamp-recording
name: whole-cell-patch-clamp-recording
category: natural-sciences
field: neuroscience
product: electrophysiology
tags: [electrophysiology, neuroscience, patch-clamp, whole-cell, voltage-clamp, current-clamp, gigaseal, pipette-resistance, series-resistance, access-resistance, input-resistance, capacitance-compensation, liquid-junction-potential, acsf, internal-solution, brain-slice, cultured-neurons, multiclamp, axopatch, pclamp, clampex, epsc, ipsc, action-potentials, faraday-cage]
level: advanced
status: draft
description: "Do whole-cell patch clamp in slices or cultured neurons: pipettes and solutions, gigaseal and break-in, series-resistance monitoring and compensation, junction potential, and quality criteria."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Whole-cell patch-clamp recording

**Goal:** record membrane currents (voltage clamp) or voltages (current clamp) from
a single neuron with known, stable recording quality, and know when to discard a cell.

## 1. Pipettes
- Pull from borosilicate glass with filament. Typical tip resistance in bath:
  **3–7 MΩ** for whole-cell from neurons (lower for big cells or fast currents,
  higher for small cells).
- Fire-polishing is optional for slices; helps for cultured cells.
- Fill with filtered (0.2 µm) internal solution; tap out bubbles; avoid wetting the
  outside of the shank (adds noise). Keep the fill short.

## 2. Solutions
- **External (aCSF)** for slices: carbogenated (95% O2/5% CO2), ~300–310 mOsm, pH ~7.4.
- **Internal:** K-gluconate-based for current clamp and physiology; Cs-based
  (often with QX-314) to block K+ and Na+ channels for clean voltage clamp of
  synaptic currents. ~280–295 mOsm (slightly below external), pH 7.2–7.3, with ATP/GTP;
  keep on ice, aliquot frozen.
- Compute the **liquid junction potential** (often ~10–15 mV for K-gluconate) and
  correct offline or online; report whether you corrected.

## 3. Approach and seal
1. Apply **positive pressure** before entering the bath; it keeps the tip clean.
2. Zero the pipette offset in bath; set a test pulse (e.g. 5–10 mV) to monitor resistance.
3. Approach the cell under DIC/IR optics; when a dimple appears on the membrane (or
   resistance rises ~0.1–0.5 MΩ), **release pressure**; apply gentle suction and set
   holding to around −60/−70 mV.
4. Wait for a **gigaseal** (≥1 GΩ). Compensate fast (pipette) capacitance in cell-attached mode.

## 4. Break-in and whole-cell
- Rupture the patch with short, sharp suction pulses (or a "zap"). Large capacitive
  transients appear.
- Compensate slow (whole-cell) capacitance; read **membrane capacitance (Cm)**,
  **series/access resistance (Rs)** and **input resistance (Rin)**.
- Note resting membrane potential immediately in current clamp (I = 0) before dialysis changes it.

## 5. Series resistance — the main quality variable
- Aim for **Rs < ~20 MΩ** (smaller is better) and **stable within ~20%** across the
  recording; discard or exclude periods outside your pre-set criteria.
- Voltage error = I × Rs: a 1 nA current through 20 MΩ gives a 20 mV error.
- **Rs compensation** (prediction/correction, often 60–80%) improves voltage
  clamp of large currents; over-compensation causes oscillation that can kill the cell.
- Space-clamp is poor in neurons with long dendrites; distal synaptic currents are
  filtered and under-clamped whatever you do.

## 6. Noise and stability
- Faraday cage closed, single-point ground, unused equipment off, perfusion lines and
  bath level steady; Ag/AgCl reference re-chlorided regularly.
- Typical acquisition: filter at 2–10 kHz (Bessel), sample at ≥ 2–5× the filter
  frequency (often 10–20 kHz). Software: pCLAMP/Clampex, WinWCP, Patchmaster, others.

## 7. Analysis and reporting
Report cell inclusion criteria (Rs threshold, Rin, resting potential, spike overshoot),
junction potential correction, temperature (room vs physiological; kinetics are
temperature-dependent), solutions, and n as cells *and* animals. Analysis tools:
Clampfit, Easy Electrophysiology, or Python (`pyabf`, `neo`, `elephant`).

## Gotchas
- Rundown of currents over minutes (washout of intracellular factors) — use
  perforated patch when signalling must be preserved.
- Clogged tips from losing positive pressure: change pipette rather than fight it.
- Unhealthy slices: swollen or shrunken cells under DIC; improve slicing (cold,
  NMDG or sucrose cutting solutions) rather than recording from them.

## Verify
- [ ] Seal ≥ 1 GΩ before break-in.
- [ ] Cm, Rs and Rin recorded at start and tracked through recording.
- [ ] Rs below and stable within pre-set criteria; cells outside excluded.
- [ ] Junction potential computed and correction reported.
- [ ] Filtering/sampling and temperature documented.

*Draft note:* numeric ranges are common lab practice and vary by preparation, cell
type and question; set inclusion criteria before collecting data.
