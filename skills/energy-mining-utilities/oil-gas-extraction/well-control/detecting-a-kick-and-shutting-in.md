---
id: energy-mining-utilities.oil-gas-extraction.well-control.detecting-a-kick-and-shutting-in
name: detecting-a-kick-and-shutting-in
category: energy-mining-utilities
field: oil-gas-extraction
product: well-control
tags: [well-control, kick, kick-detection, blowout, blowout-prevention, bop, blowout-preventer, annular, pipe-rams, shear-rams, hard-shut-in, soft-shut-in, flow-check, pit-gain, sidpp, sicp, shut-in-pressure, kill-mud-weight, kill-sheet, drillers-method, wait-and-weight, engineers-method, choke, choke-manifold, maasp, gas-migration, iwcf, iadc-wellsharp, drilling-operations]
level: advanced
status: draft
description: "Recognise a kick, shut the well in fast, record SIDPP/SICP and pit gain, and work out kill mud weight for the driller's or wait-and-weight method."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Detecting a kick and shutting in

**Goal:** catch formation influx early, close the well before it grows, and collect the
numbers the kill depends on.

> Status: draft. This summarises the standard logic taught in IWCF/IADC well control
> courses. It is not a substitute for certification or for your rig's well control
> manual, shut-in procedure and pre-recorded kill sheet. Units below are oilfield (ppg,
> psi, ft); check for metric rigs.

## 1. Kick warning signs
Primary (act immediately):
- **Pit gain** — active pit volume increasing.
- **Flow rate increase** on the return flow sensor with constant pump rate.
- **Well flowing with pumps off.**
- **Wrong hole fill on trips** (see energy-mining-utilities.oil-gas-extraction.drilling-operations.tripping-pipe-and-managing-the-hole).
Secondary (investigate, often flow check):
- Drilling break (sudden increase in rate of penetration).
- Pump pressure decrease with pump strokes increase.
- Gas-cut mud, increased connection or background gas, changes in cuttings.

**If in doubt, flow check; if flowing, shut in.** The size of the kick is the single
biggest factor in how hard the kill will be.

## 2. Shutting in (typical hard shut-in while drilling)
1. Stop rotating, pick up off bottom to the **space-out** position (tool joint clear of
   the BOP elements you'll close).
2. Stop the pumps.
3. Close the BOP (often the annular, or the designated ram) per the rig's procedure.
4. Confirm the well is shut in: choke closed (hard shut-in) and no flow.
5. Notify the toolpusher/company representative.
6. Record: time, **pit gain**, **SIDPP** (shut-in drill pipe pressure) and **SICP**
   (shut-in casing pressure), reading every minute until they stabilise.
Tripping: install the full-opening safety valve (stab-in valve) in the open position,
close it, then close the BOP.

## 3. Reading the pressures
- **SIDPP** reflects formation pressure minus the drill-string hydrostatic (the string
  is full of known mud): formation pressure = SIDPP + 0.052 × MW × TVD.
- **SICP** is usually higher than SIDPP because the influx in the annulus is lighter
  than mud. Big SICP–SIDPP differences suggest a gas kick.
- If both pressures keep **rising slowly** after stabilising, gas is likely migrating;
  bleed small controlled volumes per procedure (volumetric method) to hold bottom-hole
  pressure, rather than letting pressure build.
- Watch **MAASP** (max allowable annular surface pressure) from the leak-off test:
  exceed it and you risk breaking down the shoe.

## 4. Kill mud weight
**KMW (ppg) = OMW + SIDPP ÷ (0.052 × TVD)**, where OMW is the original mud weight.
Example: OMW 10.0 ppg, SIDPP 520 psi, TVD 10,000 ft → 10.0 + 520 / 520 = 11.0 ppg.

## 5. Kill methods (outline)
- **Driller's method:** first circulation with original mud to get the influx out,
  holding drill pipe pressure constant at the initial circulating pressure (ICP = SCR
  pressure + SIDPP) once pump is at kill rate; second circulation with kill mud.
  Simple, starts immediately, higher annular pressures.
- **Wait-and-weight (engineer's) method:** weight up to KMW first, then circulate once,
  following a drill pipe pressure schedule from ICP down to FCP (final circulating
  pressure = SCR pressure × KMW/OMW). Lower annular pressures, needs time and
  calculation.
- Bring the pump up to kill rate while the choke operator holds **casing pressure
  constant**, then switch to drill-pipe pressure control — the classic place mistakes
  happen.

## Gotchas
- Slow circulating rates (SCRs) must be recorded each tour and after mud or BHA
  changes; the kill sheet is worthless without current values.
- Choke response lags (seconds per thousand feet of hole); don't chase the gauge.
- Gas expands rapidly near surface; pit volume rising late in the kill is expected —
  manage it with the choke, don't panic and close it.

## Verify
- [ ] Shut-in drills (pit, trip) done and timed regularly.
- [ ] SCRs and kill sheet current.
- [ ] Pressures recorded to stabilisation; pit gain logged.
- [ ] KMW calculated and checked by a second person.
- [ ] MAASP known and not exceeded.
