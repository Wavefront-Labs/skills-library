---
id: engineering-technology.agricultural-and-biosystems-engineering.irrigation-design.crop-water-requirement-and-drip-design
name: crop-water-requirement-and-drip-design
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: irrigation-design
tags: [agricultural-and-biosystems-engineering, irrigation-design, crop-water-requirement, fao-56, penman-monteith, reference-evapotranspiration, et0, etc, crop-coefficient, kc, drip-irrigation, trickle-irrigation, micro-irrigation, emitter, emission-uniformity, lateral-design, hazen-williams, darcy-weisbach, christiansen-factor, pump-sizing, irrigation-scheduling, soil-water-balance, leaching-requirement, sprinkler-irrigation, coefficient-of-uniformity, cropwat]
level: practitioner
status: gated
description: "Size an irrigation system from crop water demand: FAO-56 Penman-Monteith ETc, gross depth, drip emitter and lateral hydraulics, uniformity, pump power and a soil-water scheduling rule."
sources:
  - "Allen, Pereira, Raes & Smith, FAO Irrigation and Drainage Paper 56: Crop Evapotranspiration (https://www.fao.org/4/x0490e/x0490e00.htm)"
  - "Keller & Bliesner, Sprinkle and Trickle Irrigation"
  - "Ayers & Westcot, FAO Irrigation and Drainage Paper 29: Water Quality for Agriculture"
  - "USDA NRCS National Engineering Handbook, Part 623 (Irrigation)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Crop water requirement and drip design — from ETc to pump kilowatts

**Goal:** turn climate and crop data into a peak design flow, then lay out drip
laterals and a pump that deliver it uniformly.

## 1. Reference evapotranspiration (FAO-56)
Use the FAO-56 Penman-Monteith equation with daily or monthly weather:

`ET0 = [0.408 Δ (Rn − G) + γ (900 / (T + 273)) u2 (es − ea)] / [Δ + γ (1 + 0.34 u2)]`

ET0 in mm/day; Rn net radiation (MJ/m²/day); G soil heat flux (≈0 daily); T mean air
temperature (°C); u2 wind at 2 m (m/s); es − ea vapour pressure deficit (kPa); Δ slope
of the vapour pressure curve and γ psychrometric constant (kPa/°C). FAO CROPWAT, the
FAO ET0 Calculator or a spreadsheet does this; check against a nearby agro-met station.
Wind measured at other heights must be converted to 2 m. If only temperature exists,
Hargreaves is a fallback with larger error.

## 2. Crop evapotranspiration
`ETc = Kc × ET0`. FAO-56 Kc examples (standard conditions, adjust for climate):
maize (field) Kc_mid 1.20, tomato Kc_mid 1.15, citrus without ground cover Kc_mid 0.45 to 0.65 for 20 to 70 percent canopy (FAO-56 Table 12). Kc_ini varies widely by crop and wetting frequency; read it from FAO-56 Table 12.
Design on **peak-month ETc**, not the season average.

For drip on partial canopy, apply a cover reduction such as Keller's
`Kr = Gc / 0.85` (≤ 1), where Gc is the shaded fraction at noon (gated: unconfirmed, source is paywalled or blocked).

## 3. Gross requirement and system flow
- Net depth/day `d_n = ETc × Kr − effective rain` (rain ≈ 0 at peak for design).
- Gross `d_g = d_n / (EU × (1 − LR))`, where EU is emission uniformity as a fraction.
- Leaching requirement: FAO-29 gives the Rhoades form `LR = ECw / (5 ECe − ECw)` for ordinary surface methods; a drip/high-frequency form `LR = ECw / (2 × max ECe)` with the crop's zero-yield ECe is also used (gated: unconfirmed, source is paywalled or blocked). The FAO-29 equations are images, so confirm them in the paper.
- System flow `Q (m³/h) = 10 × d_g (mm/day) × A (ha) / T_op (h/day)`.

Example: peak ETc 6 mm/d, Kr 0.7 → 4.2 mm/d; EU 0.9 and LR negligible → 4.7 mm/d.
On 10 ha running 20 h/d: Q = 10 × 4.7 × 10 / 20 ≈ 23 m³/h (6.5 L/s).

## 4. Emitters and laterals
- Emitter law `q = k H^x`: x ≈ 0.5 for turbulent emitters, ≈ 0–0.1 for
  pressure-compensating (PC). With x = 0.5, a 20 % head variation gives ~10 % flow
  variation; that is the classic design limit for non-PC laterals.
- Friction in PE laterals: Darcy-Weisbach with Blasius f = 0.316 Re^−0.25 (smooth
  pipe), or Hazen-Williams (C ≈ 140–150 for PE (gated: unconfirmed, source is paywalled or blocked)). Multiply the full-flow loss by
  Christiansen's multiple-outlet factor F (≈ 0.35 for many outlets with Hazen-Williams, ≈ 0.36 with Blasius; computed).
  Add emitter barb losses as an equivalent length (vendor data).
- Lay laterals **downhill or along the contour**; a modest downslope can cancel friction.
  Use PC emitters on steep or long runs.
- Design EU (Keller-Karmeli):
  `EU = 100 (1 − 1.27 Cv/√n) q_min/q_avg`, with Cv the manufacturer's coefficient of
  variation and n the emitters per plant. Target EU ≥ 90 % on uniform slopes (gated: unconfirmed, source is paywalled or blocked).

## 5. Pump
`P_shaft (kW) = 9.81 × Q (m³/s) × H (m) / η`
H = static lift + mainline/submain/lateral friction + filter loss (design at the dirty
setpoint, typically 0.5–0.7 bar for media/disc filters (gated: unconfirmed, source is paywalled or blocked)) + required emitter inlet
pressure + fittings. For 6.5 L/s at 35 m with η = 0.65: P ≈ 3.4 kW; choose the next
motor size and check the duty point sits near the best-efficiency point on the curve.

## 6. Scheduling
Soil water balance: `TAW = 1000 (θ_FC − θ_WP) Zr` (mm); `RAW = p × TAW` with p from FAO-56 Table 22 (the text gives 0.30 for shallow-rooted crops at ETc above 8 mm/d to 0.70 for deep-rooted crops at ETc below 3 mm/d; 0.50 is commonly used). Irrigate before depletion exceeds RAW. Drip usually runs daily or
every other day, replacing ETc since the last set.

## Sprinkler notes
Average application rate must stay below the soil's basic intake rate; spacing about
50–65 % of wetted diameter depending on wind (gated: unconfirmed, source is paywalled or blocked); target Christiansen CU ≥ 85 % (gated: unconfirmed, source is paywalled or blocked).

## Gotchas
- Using average ETc under-sizes the system for the hottest weeks.
- Water quality (iron, carbonates, algae) clogs emitters; specify filtration mesh to
  the emitter manufacturer's requirement and plan acid/chlorine injection.
- Air and vacuum relief valves are needed at high points and submain ends.
- Kc values assume standard conditions; arid, windy sites need the FAO-56 climatic correction.
- Water rights, backflow prevention and chemigation rules vary by jurisdiction.

## Verify
- [ ] ET0 computed with FAO-56 PM and spot-checked against a local station.
- [ ] Design flow is based on peak ETc, uniformity, leaching and actual operating hours.
- [ ] Lateral head variation is within the emitter's allowable range (or PC emitters used).
- [ ] Pump duty point (Q, H) sits near best efficiency on the vendor curve.
- [ ] A catch-can or flow test after commissioning confirms field EU.
