---
id: manufacturing-production.food-beverage-processing.frozen-chilled-processing.blast-spiral-and-iqf-freezer-operation
name: blast-spiral-and-iqf-freezer-operation
category: manufacturing-production
field: food-beverage-processing
product: frozen-chilled-processing
tags: [frozen-chilled-processing, freezing, chilling, blast-freezer, blast-chiller, spiral-freezer, iqf, individually-quick-frozen, tunnel-freezer, fluidised-bed-freezer, cryogenic-freezing, liquid-nitrogen, co2, ammonia-refrigeration, evaporator-defrost, frost-build-up, dwell-time, core-temperature, minus-18c, cooling-curve, temperature-mapping, data-loggers, glazing, clumping, cold-chain, dispatch, reefer, cold-store, chilled-food, frozen-food, food-processing]
level: practitioner
status: draft
description: "Freeze and chill product at line scale: set dwell and air temperature on spiral, tunnel and IQF freezers, prove core temperature, manage frost and defrost, map cold rooms and hand off the cold chain."
sources:
  - "https://www.gov.uk/food-hygiene-businesses/chilling-and-freezing"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Blast, spiral and IQF freezer operation

**Goal:** every unit reaches its target core temperature within the required time,
without freezer burn, clumping or damage, and stays cold until it leaves your gate.
Reefer transport after the gate: transportation-logistics (search "reefer").

## 1. The targets
- **Frozen**: take the storage and distribution core temperature and any permitted fluctuation from the quick-frozen food rules that apply to you and your customer specification.
- **Chilled**: UK chilled food must be kept at 8 °C or below (legal in England, Wales and Northern Ireland, a recommendation in Scotland), with a fridge setting of 5 °C or below advised (gov.uk). Cooked-food cooling rules are time-bound and
  differ by jurisdiction; use the limit in your HACCP plan.
- Fast freezing through the 0 to −5 °C zone forms small ice crystals → better texture and less drip loss.

## 2. Freezer types and their knobs
| Type | Main settings | Watch for |
|---|---|---|
| **Blast room/chiller** (batch) | Air temperature, fan speed, load pattern | Overloading, blocked airflow, warm product loaded on top of part-frozen |
| **Spiral freezer** | Belt speed (= dwell time), air temperature (e.g. −35 to −40 °C), fan speed | Product spacing, belt tracking, frost on coils |
| **Tunnel / impingement** | Belt speed, air velocity | Lifting of light product at high air velocity |
| **IQF fluidised bed** (peas, berries, diced) | Bed depth, air velocity (to fluidise), feed rate | Clumping if surface water present; product blown out |
| **Cryogenic** (LN2, CO2) | Spray rate, exhaust, belt speed | Cracking from too fast freeze; **asphyxiation hazard** — O2 monitors must work |
Feed product at the rate the freezer was set for; increasing throughput without lengthening dwell gives warm cores.

## 3. Proving core temperature
- Probe the **largest/thickest units** at the **exit**, at the geometric centre, with a
  calibrated probe (pre-drilled holes or a hand drill for hard-frozen product).
- Check at start, per frequency, and after any change in product size, feed rate or
  freezer setting. Record actual values.
- Not at target → adjust dwell (slow the belt) or reduce feed, and hold product since the
  last good check for re-freezing/assessment (don't send warm product to cold store and
  expect the store to finish the job — stores are designed to hold, not freeze).

## 4. Frost and defrost
- Moisture from product (especially unwrapped, warm, wet) builds frost on evaporator coils
  → airflow drops → freezing slows. Watch rising air temperature or falling fan amps.
- Plan defrosts between runs or use sequential defrost if fitted. Pre-dry product surfaces
  (dewatering shaker for IQF veg) to cut frost load.
- After defrost, clear ice from floors and drains — slip hazard.

## 5. Mapping and monitoring cold rooms
- **Temperature mapping**: place loggers through the room (corners, near doors, top and
  bottom of racks, near evaporators) for a representative period, loaded and empty; find
  warm spots and don't store sensitive product there.
- Continuous monitoring with alarms; respond to alarms per procedure (not just silence them).
- Door discipline: strip curtains intact, doors closed, no props.

## 6. Cold-chain hand-off
- Pre-cool trailers to setpoint before loading (the unit maintains, it doesn't pull down cargo).
- Load from cold store quickly; check product temperature at loading and record it.
- Seal number, setpoint and product temperature on dispatch paperwork.

## Safety
- Cold-store entry: don't work alone; know the inside release and alarm; appropriate PPE and time limits.
- Ammonia plants: know the leak alarm response and muster point.

## Gotchas
- Mixing product sizes on one setting — the biggest pieces come out warm.
- Glazing water too warm or uneven (fish/seafood), adding weight but not protection.
- Labelling product "frozen" when the core has only crusted.

## Verify
- [ ] Freezer settings match the product recipe; feed rate within limit.
- [ ] Exit core temperatures on the largest units meet target at every check.
- [ ] Evaporators defrosted on schedule; airflow normal.
- [ ] Cold-room monitoring active; no unresolved alarms; mapping current.
- [ ] Dispatch temperature and trailer setpoint recorded.

## Checked

Date: 2026-10-25. Jurisdiction: United Kingdom (gov.uk food hygiene guidance) for chilled storage.

Confirmed on gov.uk: chilled food 8 °C or below (legal in England, Wales and Northern Ireland), fridge 5 °C or below. Removed as unconfirmed: the -18 °C frozen figure and EU fluctuation allowance (EUR-Lex is blocked to the tool), the US Food Code cooling limits (the FDA Food Code PDF could not be read as text) and the UK 90 minute figure (not on the gov.uk pages read). Freezer air temperatures, belt and equipment figures are craft values that were not checked, so the skill stays draft.

Method: documentation only; no commands were run.
