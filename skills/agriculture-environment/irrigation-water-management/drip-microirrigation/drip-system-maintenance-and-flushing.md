---
id: agriculture-environment.irrigation-water-management.drip-microirrigation.drip-system-maintenance-and-flushing
name: drip-system-maintenance-and-flushing
category: agriculture-environment
field: irrigation-water-management
product: drip-microirrigation
tags: [drip-microirrigation, drip-irrigation, trickle-irrigation, micro-irrigation, micro-sprinkler, emitters, dripline, drip-tape, laterals, flushing, filtration, screen-filter, disc-filter, media-filter, sand-filter, chlorination, acid-injection, clogging, emitter-uniformity, fertigation, venturi, injector, backflow-prevention, pressure-regulator]
level: practitioner
status: gated
description: "Keep drip and micro-irrigation running: filter servicing, lateral flushing, chlorine and acid treatment, emitter flow checks and fertigation order."
sources: ["https://www.nrcs.usda.gov/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Drip system maintenance and flushing

**Goal:** stop emitters clogging — the main way drip systems fail — and catch
uniformity loss early, so every plant gets the water and fertiliser the schedule assumes.

## 1. Know your water first
Get a water test before choosing a maintenance routine. The usual clogging hazards
(thresholds are the commonly quoted "severe" levels; treat as guidance):

| Hazard | Watch for | What it means |
|---|---|---|
| Physical | suspended solids > 100 mg/L (gated: unconfirmed, source is paywalled or blocked), algae in open storages | filtration is the main defence |
| Chemical | pH > 7.5–8 with hardness/bicarbonate > ~150 mg/L; iron > 1.5 mg/L; manganese > 1.5 mg/L (gated: unconfirmed, source is paywalled or blocked) | lime scale or iron ochre — acid / oxidation treatment |
| Biological | iron bacteria, slime, high bacterial counts | chlorination |

## 2. Filtration routine
- Match filter fineness to the emitter maker's spec — typically **120–200 mesh
  (75–130 µm)**; the rule of thumb is filter openings ≤ 1/7 to 1/10 of the emitter (gated: unconfirmed, source is paywalled or blocked)'s
  smallest passage.
- Fit **pressure gauges either side** of the filter. Clean or backflush when the
  pressure drop rises **~35–70 kPa (5–10 psi) above the clean reading (gated: unconfirmed, source is paywalled or blocked)**. Auto-flushing
  filters do this on a ΔP switch or timer — check the switch actually trips.
- Media (sand) filters: backflush until the waste runs clear, top up media yearly,
  break up any crust. Disc filters: open and hose the discs apart during the season.
- Check screens for tears after every clean — a torn screen passes everything.

## 3. Flushing the network
Flush mains, submains and then laterals, in that order, so dirt is pushed out rather
than into the laterals.
1. Open the ends of a few laterals at a time (enough that the system can still
   reach flushing velocity — aim for about **0.3 m/s (1 ft/s)** (gated: unconfirmed, source is paywalled or blocked) in the lateral).
2. Run until the water runs clear, then a bit longer. Catch the first water in a jar
   or sock to see what's coming out (sand → filter problem; slime → biology; white
   grit → scale).
3. Frequency: at start-up, after any repair, after fertigation with a new product, and
   at least monthly in season (weekly for dirty surface water). Automatic flush valves
   at lateral ends help but don't replace a proper manual flush.

## 4. Chemical treatment
- **Chlorine (biology, slime, iron bacteria):** continuous injection to ~1–2 mg/L free (gated: unconfirmed, source is paywalled or blocked)
  chlorine at the furthest emitter, or a periodic shock of 10–30 mg/L (gated: unconfirmed, source is paywalled or blocked) held in the lines
  a few hours, then flushed. Chlorine works best below pH ~7.5. Test free chlorine at
  the end of the line with a pool test kit — injection rate at the head means nothing
  if it's all consumed.
- **Acid (scale, raise chlorine efficiency):** inject to bring water to pH ~5.5–6.5 (gated: unconfirmed, source is paywalled or blocked) for
  routine prevention, or lower (~pH 4) for a short clean-out — then flush thoroughly.
  Always add acid to water, never water to acid; use acid-rated injectors and PPE.
- **Never inject chlorine and fertiliser containing ammonium or phosphate at the same
  time**, and never mix chlorine with acid in the same tank (chlorine gas).

## 5. Fertigation sequence
Run each fertigation cycle as: **plain water to fill and pressurise the system →
fertiliser → plain water to flush the lines.** The final flush should be at least the
system's travel time (time for dye/conductivity change to reach the last emitter —
measure it once). Fertiliser left in lines feeds algae and precipitates. Fit a
backflow preventer / chemigation check valve where the law requires it (most places do
when connected to any potable or public source).

## 6. Check uniformity
Twice a season, catch emitter output for a timed period (e.g. 2–5 min in a cup or
measuring cylinder) at ~16–32 emitters spread from near the head to the far end, high
and low points. Compute the **emission uniformity**:
`EU = (average of lowest 25% of catches) ÷ (average of all) × 100`.
> 90% excellent, 80–90% good, < 70% needs action (gated: unconfirmed, source is paywalled or blocked) (clogging, pressure, leaks). Also read
pressure at the head and the end of a lateral — pressure-compensating emitters still
need to be inside their working range.

## Gotchas
- Rodents and insects chew tape; leaks steal pressure from the far end first.
- Drip tape on its first season often looks fine on uniformity while slowly clogging —
  trend the EU numbers.
- Chemical dose rates above are typical extension figures, **not checked against any
  product label**; follow the product label and local chemigation rules.

## Verify
- [ ] Filter ΔP gauge readings logged, clean-filter baseline known.
- [ ] Flushing done end-of-lateral until clear; dirt type identified.
- [ ] Free chlorine / pH measured at the far end, not just the injector.
- [ ] Emission uniformity calculated and ≥ 85%, or causes found.
- [ ] Every fertigation ended with a clean-water flush ≥ travel time.

## Checked

- Date: 2026-10-25. Jurisdiction: no regulation involved; follow the emitter maker's specification.
- Confirmed against: the unit conversions were recomputed (35-70 kPa = 5-10 psi; 0.3 m/s = 1 ft/s; 120-200 mesh = about 125-75 micrometres).
- Not confirmed: the water-quality clogging thresholds, filter opening ratio, pressure-rise trigger, chlorine and acid dosing figures and emitter uniformity classes (NRCS NEH 623 and ASABE EP405/EP458 were not read).

Method: documentation only; no commands were run.
