---
id: energy-mining-utilities.oil-gas-extraction.wireline-coiled-tubing.slickline-runs-and-coiled-tubing-cleanouts
name: slickline-runs-and-coiled-tubing-cleanouts
category: energy-mining-utilities
field: oil-gas-extraction
product: wireline-coiled-tubing
tags: [wireline-coiled-tubing, wireline, slickline, braided-line, e-line, electric-line, logging, lubricator, stuffing-box, grease-head, wireline-bop, wireline-valve, pressure-control-equipment, toolstring, jars, spang-jars, gauge-run, drift-run, fishing, coiled-tubing, ct, injector-head, stripper, coil-fatigue, cleanout, nitrogen-lift, n2-kickoff, well-intervention, plug-setting]
level: practitioner
status: draft
description: "Run well interventions: rigging up lubricator and pressure control, slickline toolstrings and jarring, stuck-tool decisions, coiled tubing cleanouts and nitrogen lifts, fatigue tracking."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Slickline runs and coiled-tubing cleanouts

**Goal:** do live-well interventions without losing pressure control, without leaving
tools in the hole, and without fatiguing the coil to failure.

> Status: draft. Generic practice; pressure control equipment (PCE) configuration and test
> values follow the service company's standards and the operator's well intervention
> rules. Weight and pressure numbers depend on the unit.

## 1. Rig-up and pressure control
- Stack from the wellhead up (generic slickline): **wireline valve/BOP**, **lubricator**
  long enough for the whole toolstring, and a **stuffing box** (slickline) or **grease
  head** (braided/e-line) at the top.
- **Pressure test** the PCE before opening the swab valve: low then high to the agreed
  value, held for the agreed time. Record it.
- Open the well slowly and **equalise** across the swab valve before opening fully;
  count valve turns so you know it's fully open (a partly open valve can cut the wire).

## 2. Slickline toolstrings and runs
- Typical string: rope socket, stem (weight bars), jars (spang or hydraulic), knuckle
  joint, then the running/pulling tool or gauge.
- **Gauge/drift run** first, with a gauge cutter sized to the tubing, to confirm the
  path is clear before running anything expensive.
- Watch the **weight indicator**: going in, weight drops when tools hit fluid or tags;
  coming out, overpull signals a restriction. Speed down near nipples, the end of tubing
  and known restrictions.
- **Jarring:** pick up, let the jars set, slack off, then pull to fire. Count jar
  licks and stay below the wire's safe working load (a set fraction of breaking
  strength, adjusted for wire age and condition).
- Stuck tools: don't pull past the weak point unless that is the plan; use a planned
  release (shear pin), and log everything for the fishing plan.
- Stop at the top with the tools fully in the lubricator — check by counter and
  feel — before closing the swab valve. Closing it on wire or tools cuts them.

## 3. Coiled tubing cleanouts
- CT stack: injector head, stripper (stuffing element), CT BOP (blind, shear, slip,
  pipe rams), riser to the wellhead.
- Run in circulating fluid (water, gel, foam or nitrogen); **wash down** through fill
  (sand, scale) in increments, then **sweep** back to keep the annulus clean. Pumping
  too little lets solids settle around the coil and stick it.
- Monitor **pull and push weights** (pick-up and slack-off) against the model; a
  deviation means drag, sticking or buckling (lock-up in horizontals).
- **Nitrogen lift (kickoff):** pump N₂ through the coil at depth to lighten the fluid
  column so the well can flow. Watch returns, N₂ rate and well response; nitrogen
  is an asphyxiant — manage vents.

## 4. Coil fatigue and integrity
- Every trip over the gooseneck and reel bends the coil plastically. Fatigue software
  tracks life per foot; retire or cut the string when it reaches the limit.
- Avoid repeated cycling at the same depth while pressurised — that section fatigues
  fastest.
- Inspect for ballooning, corrosion, and flat spots; a coil failure under pressure is
  a well control event.

## Gotchas
- H₂S service needs suitable wire and coil grades — standard wire can embrittle.
- Hydrates can form in the lubricator on gas wells; inject methanol/glycol.
- Two people should confirm tools are in the lubricator before closing valves.

## Verify
- [ ] PCE pressure tested and recorded before opening the well.
- [ ] Gauge run completed before main run.
- [ ] Safe working load and weak point known and respected.
- [ ] Tools confirmed in the lubricator before closing the swab valve.
- [ ] Coil fatigue logged for the job.
