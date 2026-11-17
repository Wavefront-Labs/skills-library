---
id: manufacturing-production.electronics-semiconductor-manufacturing.thin-film-etch-operations.plasma-etch-endpoint-and-chamber-seasoning
name: plasma-etch-endpoint-and-chamber-seasoning
category: manufacturing-production
field: electronics-semiconductor-manufacturing
product: thin-film-etch-operations
tags: [thin-film-etch-operations, plasma-etch, dry-etch, rie, icp, endpoint-detection, oes, optical-emission-spectroscopy, interferometry, chamber-seasoning, conditioning-wafers, wet-clean, pm, particle-monitoring, particle-adders, cvd, pecvd, pvd, sputtering, deposition, lam-research, applied-materials, tel, etch-rate, uniformity, rf-hours, fdc, semiconductor, fab]
level: practitioner
status: draft
description: "Keep plasma etch (and deposition) chambers stable: read endpoint traces, recover a chamber after wet clean with seasoning and quals, and run particle checks before product returns."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Plasma etch endpoint and chamber seasoning

**Goal:** etch steps that stop at the right place on every wafer, from a chamber whose
condition is known — especially in the hours after a wet clean or PM, when most etch
and deposition excursions happen.

## 1. Endpoint: what the trace tells you
Most production etch recipes end a main step on **endpoint detection** rather than a
fixed time:
- **OES** (optical emission spectroscopy) watches a wavelength from an etch product or
  reactant; the signal changes when the film being etched clears.
- **Interferometry/reflectometry** tracks remaining film thickness on the wafer.
Then a timed **over-etch** step clears residues.

Reading traces (on the tool or in the FDC system):
- Endpoint time drifting longer over days → etch rate falling (chamber wall build-up,
  part wear, RF component ageing) or incoming film thicker. Check the upstream
  thickness data before blaming the chamber.
- **Endpoint not found / timeout** → wafer aborted or ran to max time; hold the wafer
  and the lot; check whether the correct film/recipe was run and whether the OES
  window is dirty.
- Noisy or flat trace on low-open-area layers (small exposed area) is normal-ish;
  these recipes often rely on time — know which steps are which.

## 2. Chamber condition
Chamber walls accumulate polymer and by-products; the chemistry a wafer sees depends
on wall condition. Tracking **RF hours** since the last wet clean is the usual PM trigger.

After a **wet clean / PM** the chamber is "too clean" — rates and selectivity differ
until the walls are re-coated:
1. Pump down, leak-rate check (rate-of-rise test against spec).
2. Run the **seasoning** recipe on dummy or bare wafers (a set number of wafers or RF
   minutes, per the recovery procedure).
3. Run **quals**: etch-rate and uniformity on blanket film monitors; for etch, sometimes
   a patterned qual measured for CD/profile.
4. **Particle check**: particle-adder wafer measured before and after a pass through
   the chamber (and transfer system); adders must be under the limit.
5. Engineering releases the chamber; first product lot often runs with extra metrology.

Many fabs also run a short **conditioning wafer** at the start of a run after idle
time ("first-wafer effect"), and some recipes include an in-situ clean between wafers.

## 3. Deposition chambers, same pattern
CVD/PECVD and PVD follow the same logic: after cleans or target change, run the
**burn-in/pasting** recipe (PVD target burn-in, CVD chamber coat), then thickness,
uniformity, stress/RI and particle quals. PVD target life (kWh) is tracked like RF hours.

## 4. Particle control
- Flakes from wall deposits are the classic etch/dep particle source; they rise as
  RF hours approach the PM limit.
- Watch for particle "spikes" after vent/pump events, robot handling alarms, or a
  wafer broken in the transfer chamber (requires inspection/cleaning before resuming).
- Pattern of defects (edge ring, centre cluster, single side) points to the component
  (edge ring, showerhead, lift pins).

## Gotchas
- A recipe edit to "fix" a drifting endpoint hides chamber degradation; the root
  cause is usually the chamber or the incoming film.
- Mixing different products in a freshly seasoned chamber can shift results —
  some fabs dedicate chambers.
- Seasoning wafers are consumed; run out and people skip seasoning. Keep stock.

## Verify
- [ ] Endpoint times trended per chamber; drifts investigated before recipe changes.
- [ ] Post-PM: leak rate, seasoning, rate/uniformity quals and particle check all pass
      before release.
- [ ] FDC alarms on RF, pressure and endpoint reviewed, not just acknowledged.

*Draft: recovery steps generalised across vendors (Lam, Applied, TEL); actual counts
and limits come from each tool's recovery procedure.*
