---
id: engineering-technology.agricultural-and-biosystems-engineering.food-process-engineering.thermal-process-lethality-design
name: thermal-process-lethality-design
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: food-process-engineering
tags: [agricultural-and-biosystems-engineering, food-process-engineering, thermal-processing, thermal-process-design, lethality, f-value, f0, d-value, z-value, 12d-concept, clostridium-botulinum, commercial-sterility, retort, canning, low-acid-canned-food, heat-penetration, cold-spot, general-method, ball-formula, pasteurisation, pasteurization, p-value, cook-value, process-authority, 21-cfr-113, aseptic-processing]
level: advanced
status: verified
description: "Design and check a thermal (retort or pasteurisation) process with D and z values, F0 lethality, 12D logic and heat-penetration data integrated by the General Method."
sources:
  - "https://www.ecfr.gov/current/title-21/chapter-I/subchapter-B/part-113"
  - "Stumbo, Thermobacteriology in Food Processing"
  - "Holdsworth & Simpson, Thermal Processing of Packaged Foods"
  - "https://www.ecfr.gov/current/title-21/part-113"
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Thermal process lethality design — D, z and F0 from heat-penetration data

**Goal:** set a time-temperature schedule that delivers a target lethality at the
slowest-heating point of the product, and prove it with measured data.

> Safety-critical. For low-acid canned or aseptic foods the scheduled process must be
> established by a recognised **process authority** and filed with the competent
> regulator (in the US, under 21 CFR 113/108). This skill explains the method; it does
> not replace that review.

## 1. Kinetics you need
- **D-value** (min): time at constant temperature for a 90 % (1-log) reduction.
- **z-value** (°C): temperature rise that cuts D by 10×.
- `D_T = D_ref × 10^((T_ref − T)/z)`
- **Lethal rate** `L = 10^((T − T_ref)/z)`: minutes at T_ref equivalent to one minute at T.
- **F-value** = `∫ L dt` (min). For sterilisation, `F0` uses T_ref = 121.1 °C and z = 10 °C.

## 2. Pick the target
| Product class | Target organism / basis | Typical target |
|---|---|---|
| Low-acid (pH > 4.6, aw > 0.85; 21 CFR 113.3), shelf-stable | C. botulinum spores, 12D | F0 about 3 min is the conventional botulinum minimum (12 x 0.21 = 2.52, rounded up; not a regulatory number); commercial 5–15 min to control spoilers (gated: unconfirmed, source is paywalled or blocked) |
| Acid / acidified (pH ≤ 4.6) | Vegetative cells, yeasts, moulds, acid-tolerant spore formers | Pasteurisation, P-value at 85–95 °C reference, z per organism |
| Milk (HTST) | Pathogens (e.g. Coxiella) | 72 °C for 15 s (jurisdictional legal minimum) |

12D logic: with D121.1 ≈ 0.21 min for C. botulinum, 12 × 0.21 ≈ 2.5 min, which is
why F0 = 3 min is the usual minimum botulinum cook. Thermophilic spoilage organisms
(e.g. G. stearothermophilus, D121 of several minutes (gated: unconfirmed, source is paywalled or blocked)) drive higher commercial F0
values; the target depends on storage temperature and acceptable spoilage rate.

## 3. Heat-penetration test
1. Find the **cold spot** for the container and product (geometric centre for
   conduction foods; lower on the axis for convection foods). Probe several positions first.
2. Fill at **worst-case** conditions: maximum fill weight, minimum headspace,
   minimum initial temperature, largest particles, highest viscosity.
3. Use calibrated thermocouples with suitable receptacle glands; record retort
   temperature with the reference thermometer and log every 15–60 s.
4. Run enough containers and replicate runs to capture variation (often 10+
   containers across 2–3 runs), and use the slowest-heating container for design.
5. Do a separate **temperature distribution** test to find the retort's cold zone and
   the venting/come-up schedule that removes air.

## 4. Integrate lethality (General Method)
Sum the lethal rates over the whole log, including come-up and cooling:

```python
import numpy as np
t = np.array(times_min)        # minutes
T = np.array(cold_spot_C)      # °C
L = 10 ** ((T - 121.1) / 10.0)
integrate = getattr(np, 'trapezoid', None) or np.trapz   # np.trapz was removed in newer NumPy
F0 = integrate(L, t)
```

Ball's formula method (fh, jh from the semilog heating curve) lets you recompute the
process time for a different retort temperature or initial temperature without a new
test; use the General Method to confirm.

## 5. Set the schedule
- Scheduled time = time at retort temperature that gives the target F0 for the slowest
  container, plus a safety margin agreed with the process authority.
- Specify every **critical factor**: initial temperature, fill weight, headspace,
  consistency/solids, container size, retort temperature, come-up/vent schedule,
  rotation speed (agitating retorts) and water-flow rates.
- Quality: compute a **cook value** C with z ≈ 25–45 °C (nutrients, colour (gated: unconfirmed, source is paywalled or blocked)) and
  T_ref = 100 °C to compare schedules; higher temperature, shorter time usually
  preserves quality in convection-heated products.

## Gotchas
- **Thermocouple conduction error**: the probe stem can carry heat to the junction;
  use fine wire and the correct gland.
- **Come-up and cooling lethality** can be large for conduction foods; including it is
  allowed under the General Method, but only if the real come-up matches the test.
- Formulation changes (starch, particle size, fill viscosity) change heating rate and
  invalidate the schedule. Re-test after any change.
- Altitude changes the boiling point; it matters for open-kettle and atmospheric
  processes, and pressure gauges must be read against the reference thermometer.
- Container integrity (seams, seals) is part of safety; lethality alone is not.

## Verify
- [ ] D, z and target F/P values are cited for the organism and product pH/aw.
- [ ] The cold spot was located experimentally, at worst-case fill conditions.
- [ ] The schedule was set on the slowest-heating container from replicate runs.
- [ ] F0 integrated by the General Method meets the target with an agreed margin.
- [ ] All critical factors are written into the scheduled process and reviewed by a process authority.
