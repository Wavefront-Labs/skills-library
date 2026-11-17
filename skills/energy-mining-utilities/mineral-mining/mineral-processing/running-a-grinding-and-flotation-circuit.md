---
id: energy-mining-utilities.mineral-mining.mineral-processing.running-a-grinding-and-flotation-circuit
name: running-a-grinding-and-flotation-circuit
category: energy-mining-utilities
field: mineral-mining
product: mineral-processing
tags: [mineral-processing, beneficiation, concentrator, process-plant-operator, comminution, crusher, sag-mill, ball-mill, grinding, cyclone, hydrocyclone, classification, p80, pulp-density, marcy-scale, flotation, froth-flotation, rougher, scavenger, cleaner, collector, frother, reagents, ph, froth, recovery, concentrate-grade, tailings, gravity-separation, magnetic-separation, thickener, filter]
level: practitioner
status: draft
description: "Operate a concentrator's grinding and flotation section: mill feed and density control, cyclone checks, froth reading, reagent and air adjustments, and sampling to close the loop."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Running a grinding and flotation circuit

**Goal:** hold grind size and pulp conditions steady so flotation can make target
concentrate grade at the best recovery, and know which knob to turn when it drifts.

> Status: draft. Setpoints are ore- and plant-specific; this gives the control logic an
> operator uses, not numbers for your plant. Circuit sizing is in
> engineering-technology.mining-geological-engineering.mineral-processing.comminution-circuit-sizing.

## 1. Grinding: hold feed, density and size
- **Steady feed** beats high feed. A SAG mill is controlled on **mill weight/load
  cell or bearing pressure** and power: rising weight with falling power means the
  mill is overloading (charge too full, not tumbling) — cut feed early. Listen too: a
  change in mill sound is often the first sign.
- **Pulp density:** check with a Marcy scale or density gauge at the mill discharge
  and cyclone feed. Too thin and grinding efficiency falls; too thick and the slurry
  gets viscous and the mill can choke. Add or cut water at the mill feed/sump.
- **Cyclones:** the overflow (fines) goes to flotation, underflow (coarse) back to
  the mill. **Roping** — a solid rope-like underflow instead of a spray cone — means
  the cyclone is overloaded and coarse material is leaking to overflow. Reduce
  feed density or open another cyclone. Worn apexes and spigots shift the cut size.
- Check grind with a screen sample of cyclone overflow (or an online particle-size
  analyser). Coarse grind → poor liberation → recovery drops in flotation hours later.

## 2. Flotation: read the froth
- Arrangement: **roughers** float most of the valuable mineral, **scavengers** pick up
  what's left, **cleaners** upgrade the concentrate.
- What the froth tells you (general patterns; learn your ore):
  - Small, tight, well-loaded bubbles with mineral colour: good.
  - Large, glassy, barren bubbles that burst: under-collected or too much frother lost,
    or low mineral in feed.
  - Very fine, stiff, sticky froth that won't flow: too much frother or too fine/slimy
    feed — entrains gangue and drops grade.
  - Froth spilling over violently: too much air or a low pulp level setting.
- Knobs, one at a time: **pulp level** (froth depth), **air rate**, **collector**,
  **frother**, **pH modifier** (lime). Deeper froth and less air tend to raise grade
  and drop recovery; shallower froth and more air the opposite.
- Reagent additions are usually flow- or dose-controlled per tonne of feed; check
  pumps are actually delivering — a blocked reagent line explains a lot of "mystery"
  recovery losses.

## 3. Close the loop with samples
- Shift composite samples of feed, concentrate and tails go to the lab (or online
  analysers give minute-by-minute assays). Recovery is calculated from the three
  assays: R = c(f − t) / f(c − t), where f, c, t are the feed, concentrate and tail
  grades.
- Compare with the previous shift; a falling recovery with steady feed grade points
  at grind or reagents first.

## 4. Downstream
Thickeners: watch underflow density and overflow clarity; dose flocculant to keep
overflow clear without rat-holing. Filters: cake moisture against the shipping
specification.

## Gotchas
- Change one variable, wait at least a residence time, then judge.
- Recycling loads build up silently; a rising scavenger or cleaner-tail flow is a warning.
- Ore type changes from the pit can swamp any control action — ask what's on the feed.

## Verify
- [ ] Mill weight, power and density stable and within setpoints.
- [ ] Cyclones not roping; overflow sizing on target.
- [ ] Froth appearance normal and reagent pumps confirmed delivering.
- [ ] Shift recovery and concentrate grade calculated and compared.
- [ ] Changes logged with time so the lab results can be matched to them.
