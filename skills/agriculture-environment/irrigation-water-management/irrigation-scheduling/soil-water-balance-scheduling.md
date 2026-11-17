---
id: agriculture-environment.irrigation-water-management.irrigation-scheduling.soil-water-balance-scheduling
name: soil-water-balance-scheduling
category: agriculture-environment
field: irrigation-water-management
product: irrigation-scheduling
tags: [irrigation-scheduling, irrigation, water-balance, checkbook-method, evapotranspiration, et, eto, etc, crop-coefficient, kc, fao-56, readily-available-water, total-available-water, management-allowed-depletion, mad, soil-moisture, tensiometer, capacitance-probe, neutron-probe, field-capacity, wilting-point, deficit-irrigation, rdi, weather-station, effective-rainfall]
level: practitioner
status: gated
description: "Schedule irrigation with a daily soil-water balance: ETo x Kc, root-zone capacity, allowable depletion trigger, and soil-moisture sensor checks."
sources: ["FAO Irrigation and Drainage Paper 56 (Allen et al., 1998)", "USDA NRCS National Engineering Handbook Part 652, Irrigation Guide", "https://www.fao.org/4/x0490e/x0490e0b.htm", "https://www.fao.org/4/x0490e/x0490e0e.htm"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Soil-water balance ("checkbook") irrigation scheduling

**Goal:** decide *when* to irrigate and *how much* to put on, by tracking how much
plant-available water is left in the root zone each day and refilling before the crop
is stressed — instead of watering by calendar or by eye.

## 1. Set up the "bank account" (once per block)
You need four numbers for each irrigation block:

| Item | How to get it | Typical values |
|---|---|---|
| **Available water capacity (AWC)** | soil survey or lab: field capacity minus wilting point | sand 50-80 mm/m, loam 120-170 mm/m, clay loam 150-200 mm/m (gated: unconfirmed, source is paywalled or blocked) |
| **Effective root depth (Zr)** | dig a pit; use where most roots are, not the deepest one | FAO-56 Table 22 maximum effective root depth: onion 0.3-0.6 m, tomato 0.7-1.5 m, field maize 1.0-1.7 m, alfalfa hay 1.0-2.0 m, spring wheat 1.0-1.5 m; use the depth you find in a pit |
| **Total available water (TAW)** | AWC × Zr | e.g. 150 mm/m × 0.6 m = 90 mm |
| **Management allowed depletion (MAD / p)** | FAO-56 Table 22, or agronomist | FAO-56 Table 22 (for ETc about 5 mm/day): onion 0.30, tomato 0.40, sweet maize 0.50, field maize, wheat and alfalfa hay 0.55, alfalfa seed 0.60 |

**Readily available water (RAW) = TAW × MAD** (FAO-56 Eq. 82-83: TAW = 1000(θFC − θWP)Zr in mm, RAW = p·TAW). In the example, 90 mm × 0.5 = 45 mm. That
is your trigger: irrigate when depletion approaches 45 mm.

## 2. Run the daily balance
```
Depletion_today = Depletion_yesterday + ETc − effective_rain − net_irrigation
ETc = ETo × Kc
```
- **ETo** (reference evapotranspiration, mm/day) from the nearest weather station or
  your own station (Penman-Monteith). Most national met services and many irrigation
  district websites publish it daily.
- **Kc** from FAO-56 Table 12 for your crop and growth stage (initial / development /
  mid / late). Example: field maize Kc_mid 1.20 and Kc_end 0.60 (high grain moisture at harvest) to 0.35 (grain dried in field to about 18%) per FAO-56 Table 12; Kc_ini about 0.3 was not legible in the fetched text (gated: unconfirmed, source is paywalled or blocked). Adjust locally
  if your extension service publishes regional curves — they are usually better.
- **Effective rain:** ignore small falls (a ~5 mm cut-off is a common rule of thumb); count roughly 70-80% of larger falls (gated: unconfirmed, source is paywalled or blocked), capped so depletion never goes below 0
  (anything beyond field capacity drains away).
- **Net irrigation** = gross applied × application efficiency (drip ~0.9, pivot ~0.8-0.85, furrow 0.5-0.75 (gated: unconfirmed, source is paywalled or blocked)). Use your audited figure if you have one.

A spreadsheet with one row per day and these columns is enough. Many free tools do the
same thing (e.g. state/university "irrigation scheduler" apps) — the logic is identical.

## 3. Decide when and how much
- **When:** irrigate so that the water lands before depletion exceeds RAW. Look ahead: if
  ETc is 7 mm/day and you're at 35 mm of a 45 mm RAW, you have about one day, and a pivot
  that takes 3 days to lap must start *now*.
- **How much (net):** refill to slightly below field capacity — usually the current
  depletion minus a 5–10 mm allowance for forecast rain. **Gross = net ÷ efficiency.**
- **Don't over-fill:** water beyond field capacity drains past the roots, taking nitrate
  with it.

## 4. Ground-truth with soil moisture
The balance drifts (wrong Kc, uneven rain, runoff). Correct it weekly with a measurement:
- **Tensiometers:** read in kPa (centibars). Rough triggers: sand 20-30 kPa, loam
  30-50 kPa, clay 50-70 kPa (gated: unconfirmed, source is paywalled or blocked). Install at ¼ and ¾ of root depth; refill and re-zero after
  they suck air. They fail above ~80 kPa.
- **Capacitance / FDR probes** (logging, multi-depth): watch the *trend line*, not the
  absolute number — factory calibrations can be well off for your soil. Set "full"
  as the reading ~24–48 h after a soaking, and the refill line where the daily uptake
  curve starts to flatten (roots struggling).
- **Feel-and-appearance** (NRCS method) is a valid cross-check if you have nothing else.
If the sensor and the spreadsheet disagree, reset the balance to the measured depletion.

## 5. Deficit strategies (deliberate under-watering)
Regulated deficit irrigation (RDI) — e.g. in winegrapes and some tree crops — keeps
depletion beyond RAW at chosen stages to control vigour or save water. Only do this with
a crop-specific protocol; the same deficit at flowering or grain fill can cost serious yield.

## Gotchas
- Root depth is shallow early in the season — using the mature Zr at planting means
  seedlings run dry while the sheet says there's plenty of water.
- Sloping or compacted ground runs off: if application rate exceeds infiltration, your
  "net irrigation" is fiction. Check for ponding.
- Sensors placed in the wet spot right next to a dripper read wetter than the bed.
- Values above (AWC, MAD, triggers) are typical ranges from the literature, not
  measured for any specific site — **unconfirmed for your soil**; calibrate locally.

## Verify
- [ ] TAW and RAW written down for each block, with the root depth actually measured.
- [ ] Daily ETo source identified and Kc curve chosen for the crop.
- [ ] Balance never shows depletion < 0 or > TAW (clamp it).
- [ ] Sensor readings and balance agree within ~10 mm, or the balance was reset.
- [ ] After an irrigation, a probe or spade shows water reached the bottom of the root zone, not past it.

Related: engineering-technology.agricultural-and-biosystems-engineering.irrigation-design.crop-water-requirement-and-drip-design
