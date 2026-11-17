---
id: agriculture-environment.crop-farming.crop-sprayer.boom-sprayer-calibration-nozzles-and-drift
name: boom-sprayer-calibration-nozzles-and-drift
category: agriculture-environment
field: crop-farming
product: crop-sprayer
tags: [crop-sprayer, boom-sprayer, sprayer-calibration, application-rate, l-ha, nozzle-output, jug-test, nozzle-selection, flat-fan, air-induction, droplet-size, asabe-s572, iso-25358, spray-drift, delta-t, temperature-inversion, wind-speed, boom-height, tank-mixing, mixing-order, wales, jar-test, triple-rinse, ppe, pesticide-label, spray-records, buffer-zones, pwm, self-propelled-sprayer]
level: practitioner
status: gated
description: "Run a boom sprayer accurately and on target: calibrate output with the L/ha formula and a jug test, choose nozzles and droplet size, judge drift conditions, mix tanks in order, and rinse safely."
sources: ["https://webstore.ansi.org/preview-pages/ASABE/preview_ANSI+ASABE+S572.3+FEB2020.pdf", "https://www.croplife.com/?p=82735", "https://smallgrains.wsu.edu/spraytool/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Boom sprayer calibration, nozzles and drift

**Goal:** the labelled dose on the target, nothing on the neighbour. The **label is the
law**: it sets the rate, water volume, droplet size, wind limits, buffer zones, PPE and
re-entry/withholding periods. Everything here sits inside that.

## 1. The calibration formula
```
L/ha = nozzle output (L/min) × 600 ÷ (speed (km/h) × nozzle spacing (m))
```
Rearranged to find the nozzle output needed:
```
L/min per nozzle = L/ha × speed × spacing ÷ 600
```
Example: 100 L/ha at 16 km/h on 0.5 m spacing → 100 × 16 × 0.5 ÷ 600 = **1.33 L/min**
per nozzle. Pick a nozzle that gives that output in the middle of its pressure range.

## 2. Jug test (do it at least each season and after changing nozzles)
1. Clean water, sprayer at working pressure, all filters clean.
2. Catch each nozzle for exactly 1 minute (or 30 s × 2) in a graduated jug.
3. Compare each to the chart and to the boom average. Replace any nozzle more than
   **~5% off** (gated: unconfirmed, source is paywalled or blocked) the chart or the average (worn nozzles flow *more*, not less; replace
   the whole set if many are worn).
4. Check speed: time a measured 100 m in the field at working speed, or verify GPS
   speed on the controller. `km/h = 360 ÷ seconds per 100 m`.
5. Rate controllers adjust pressure with speed — but output only changes with the
   square root of pressure (to double flow you need 4× pressure), so big speed changes
   push nozzles out of their droplet-size range. Keep speed steady, or use PWM systems.

## 3. Nozzle and droplet choice
- Droplet size classes (ASABE S572 / ISO 25358): extremely fine → very fine → fine → medium → coarse →
  very coarse → extremely coarse → ultra coarse (eight classes; ASABE S572.3 is aligned with ISO 25358:2018). **Labels increasingly specify a
  minimum class** (often medium or coarse) for drift control.
- **Air-induction (AI)** nozzles give coarse droplets with good coverage for most
  herbicides; finer sprays (medium) may be needed for contact products on small
  targets — follow the label.
- Boom height: for 110° nozzles at 0.5 m spacing, ~50 cm above the target (gated: unconfirmed, source is paywalled or blocked) is the
  usual starting point for correct overlap; higher = more drift. Use boom height
  control on uneven ground.

## 4. When to spray (drift)
- **Wind:** guidance varies by source (roughly 3 to 20 km/h), steady, blowing away from sensitive
  areas; check the label's limits. Dead calm is not safe — it often means an inversion.
- **Surface temperature inversions:** common from late afternoon through to after
  sunrise on clear, light-wind nights; signs are mist, smoke or dust hanging in layers,
  dew. Fine droplets travel kilometres in inversion layers. Many labels prohibit
  spraying in them.
- **Delta T** (dry-bulb minus wet-bulb temperature): commonly used guidance — ~2–8 °C
  preferred, up to ~10 °C with coarse droplets; above that evaporation is high, under
  ~2 °C indicates inversion risk/high humidity.
- Record weather at start, during and end: wind speed and direction, temperature,
  humidity/Delta T.
- Respect buffer zones to water, sensitive crops (vines, cotton, gardens) and
  dwellings set on the label or by local rules; notify neighbours where required.

## 5. Tank mixing
- Read every label for compatibility and mixing instructions; do a **jar test** with
  new combinations (same proportions in a jar, check for clumping, separation, heat).
- General order many guides use (W-A-L-E-S): fill tank ½–¾ with water, agitation on,
  then **W**ettable powders/water-dispersible granules → **A**gitate thoroughly → **L**iquid
  flowables/suspensions → **E**mulsifiable concentrates → **S**olutions/soluble products,
  then adjuvants as labelled, and top up. Some labels differ — label wins.
- Water quality matters: hard water antagonises some herbicides (e.g. glyphosate);
  muddy water binds glyphosate and paraquat. Use clean water and conditioners as labelled.

## 6. After spraying
- **Triple rinse** empty containers (or pressure rinse), puncture and recycle via
  the approved scheme (drumMUSTER-type programmes).
- Rinse the sprayer in the field you sprayed (or onto a designated area), never near
  water; decontaminate thoroughly before switching to a sensitive crop (e.g. after
  hormone herbicides like 2,4-D or dicamba, follow specific cleanout procedures).
- **Spray records:** date, field, crop, target, product, rate, volume, nozzle,
  pressure, weather, operator, re-entry/withholding. Often a legal requirement.
- PPE per label; wash after; keep product licences/accreditation current.

## Gotchas
- A 10% speed error is a 10% dose error.
- Filters blocked → uneven boom output; check after each tank.
- Inversion drift damage often appears days later, kilometres away.

## Verify
- [ ] Jug test done; all nozzles within ~5% of the chart.
- [ ] Rate calculated with the formula and confirmed by area sprayed per tank.
- [ ] Droplet class meets label minimum; boom height correct.
- [ ] Wind, Delta T and inversion checks recorded at start and during spraying.
- [ ] Containers triple-rinsed; spray record complete.

## Checked

- Date: 2026-10-25. Jurisdiction: no single jurisdiction; Australian conventions (L/ha, drumMUSTER) assumed, and the product label governs everywhere.
- Confirmed against: the ASABE S572.3 (Feb 2020) scope aligning with ISO 25358:2018 and the eight droplet classes (extremely fine through ultra coarse, which fixed a missing class in the old text); Delta T about 2-8 with caution below 2 or above 10 (WSU and other extension guidance); wind guidance differs by source (WSU 4-10 mph, others 5-20 km/h), so the skill now says to follow the label; the calibration formula and the jug-test arithmetic were recomputed (100 L/ha, 16 km/h, 0.5 m = 1.33 L/min).
- Not confirmed: the 50 cm boom height and the 5% nozzle tolerance (GRDC pages returned 403, ASABE and ISO texts are paywalled).

Method: documentation only; no commands were run.
