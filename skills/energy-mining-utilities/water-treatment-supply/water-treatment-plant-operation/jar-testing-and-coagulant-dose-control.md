---
id: energy-mining-utilities.water-treatment-supply.water-treatment-plant-operation.jar-testing-and-coagulant-dose-control
name: jar-testing-and-coagulant-dose-control
category: energy-mining-utilities
field: water-treatment-supply
product: water-treatment-plant-operation
tags: [water-treatment-supply, water-treatment-plant-operation, jar-test, jar-testing, coagulation, flocculation, coagulant-dose, alum, aluminium-sulphate, ferric-chloride, ferric-sulphate, pacl, polyaluminium-chloride, polymer, coagulation-ph, settled-turbidity, filtered-turbidity, dosing-pump, mg-per-litre, raw-water-change, toc, colour-removal, drinking-water, water-operator]
level: practitioner
status: draft
description: "Run a jar test to pick coagulant dose and pH, translate it to plant dosing pump settings, and track the change through settled and filtered turbidity."
sources:
  - "AWWA Manual M37 (Operational Control of Coagulation and Filtration Processes), paraphrased"
  - "US EPA / state operator-certification training material on jar testing, paraphrased"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Jar testing and coagulant dose control

**Goal:** when raw water changes (storm, algae, reservoir turnover, source switch), find the
coagulant dose and pH that give the best settled water, then set the plant to it and prove
it worked at the filters.

## 1. When to jar test
- Raw turbidity, colour or UV254/TOC moves noticeably (a common rule of thumb: >20–30% from
  the last test, or any storm event).
- Settled turbidity drifts up or floc looks pin-point or fluffy and carrying over.
- Coagulant batch, type or supplier changes.
- Routinely (daily–weekly) even when steady, so you know where the "cliff" is.

## 2. Set up
1. Six 1–2 L jars (square jars give better mixing than round beakers) on a gang stirrer.
2. Collect raw water **at the point before chemical addition**, mix well, fill all jars the
   same volume at the same temperature. Test promptly; warming water changes results.
3. Make a stock solution of the *same* coagulant the plant is using, from today's day tank
   if possible. With 1 L jars, a 1 g/L (0.1%) stock gives 1 mL = 1 mg/L. Confirm whether the
   plant reports dose as product, as Al/Fe, or as Al2O3 — mixing these up is the classic
   factor-of-several error.
4. Bracket the current plant dose: e.g. 20, 25, 30, 35, 40, 45 mg/L. If pH matters, run a
   second set holding dose and varying pH with acid/alkali.

## 3. Mimic the plant
Match the plant's mixing, not a textbook. A typical starting regime (adjust to your basins):
- **Rapid mix:** 100–300 rpm for 30–60 s with all doses added simultaneously (use syringes
  lined up and inject together).
- **Flocculation:** 20–40 rpm for 15–30 min, ideally tapering, to match detention time.
- **Settle:** quiescent for the equivalent of basin surface loading — often 15–30 min.
- Add polymer at the same delay after coagulant as on the plant.

## 4. Read the jars
For each jar note: time to first visible floc, floc size and how it settles, then sample
from a fixed depth (e.g. 10 cm below surface) by siphon or tap without disturbing sludge.
Measure settled turbidity, pH, and where relevant colour, UV254, residual Al/Fe. Filter a
portion through a 0.45 µm or filter-paper bench filter to estimate filtered result.
Pick the **lowest dose at or near the best result** — overdosing restabilises particles,
wastes chemical and raises residual metal and sludge.

## 5. Translate to the plant
Dose (mg/L) × flow (ML/d) = kg/d; divide by solution strength and density to get L/d,
then by 24 for L/h, then convert to pump stroke/speed with the calibration curve.
Example (dose expressed as liquid product): 30 mg/L × 20 ML/d = 600 kg/d of product;
at a density of ~1.3 kg/L that is ~460 L/d ≈ 19 L/h. If dose is expressed as dry alum or
as Al, divide by the product's strength first — take strength and density from *your*
supplier's certificate, they vary.
Do a **drawdown (calibration column) test** on the pump after any big change.

## 6. Follow through
Change dose in steps, note the time, and expect a lag of the basin detention time
(often 2–4 h) before settled turbidity shows it. Watch filtered turbidity per filter, filter
head loss and run time. Log the jar result and plant response together.

## Gotchas
- Stock solutions degrade; make dilute coagulant fresh daily.
- Cold water flocs slowly — jars at room temperature flatter the result.
- pH is often the real control variable (alum works best around 5.8–7.0; ferric over a wider
  range); a dose increase without alkalinity can crash pH.
- Streaming current/charge monitors drift; recalibrate against jar results.

## Verify
- [ ] Jar regime matches plant mixing energy and times.
- [ ] Dose units (as product vs as metal) checked against the pump setting.
- [ ] Pump output proven by drawdown after change.
- [ ] Settled and filtered turbidity improved within one detention time; logged.

*Uncertain:* the mixing speeds and timings above are typical training values, not universal;
calibrate to your plant's G-values and detention times.
