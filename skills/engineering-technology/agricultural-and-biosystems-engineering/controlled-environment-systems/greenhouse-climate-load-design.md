---
id: engineering-technology.agricultural-and-biosystems-engineering.controlled-environment-systems.greenhouse-climate-load-design
name: greenhouse-climate-load-design
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: controlled-environment-systems
tags: [agricultural-and-biosystems-engineering, controlled-environment-systems, controlled-environment-agriculture, cea, greenhouse, glasshouse, heat-loss, heating-load, u-value, infiltration, air-changes-per-hour, ventilation-rate, cooling-load, evaporative-cooling, pad-and-fan, thermal-screen, energy-curtain, supplemental-lighting, grow-lights, led, dli, daily-light-integral, ppfd, par, livestock-housing-ventilation, asabe-ep406, ngma]
level: practitioner
status: draft
description: "Size greenhouse heating, ventilation, pad-and-fan cooling and supplemental lighting: U-value heat loss, infiltration, summer air exchange, DLI/PPFD targets and LED power, with a worked example."
sources:
  - "ASABE EP406 Heating, Ventilating and Cooling Greenhouses"
  - "National Greenhouse Manufacturers Association (NGMA), greenhouse heat loss and ventilation standards"
  - "Aldrich & Bartok, Greenhouse Engineering (NRAES-33)"
  - "ASHRAE Handbook — Fundamentals (design climatic data)"
  - "MidWest Plan Service MWPS-32/MWPS-34, livestock housing ventilation"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Greenhouse climate load design — heating, ventilation, cooling and light

**Goal:** size the heating plant, ventilation/cooling capacity and supplemental
lighting so the crop's set points hold on design days, without oversizing.

## 1. Design conditions
- Inside set point per crop (e.g. 18 °C night for tomato, lower for many ornamentals).
- Outside heating design temperature: the local 99 % (or 99.6 %) winter dry-bulb from
  ASHRAE or national climate data.
- Summer design: local 1–2 % dry-bulb and coincident wet-bulb, peak solar radiation.

## 2. Heating load
`Q_total = Q_cover + Q_infiltration + Q_perimeter`

**Cover conduction:** `Q_cover = U × A_cover × (T_i − T_o)`
Typical U-values (W/m²·K; NGMA/EP406 style values, check supplier data):

| Glazing | U (W/m²·K) |
|---|---|
| Single glass | ~6.2–6.4 |
| Single polyethylene film | ~6.8 |
| Double inflated polyethylene | ~4.0 |
| Twin-wall polycarbonate (8 mm) | ~3.3–3.7 |
| Any of the above + closed energy curtain | reduce 30–50 % (curtain-specific) |

**Infiltration:** `Q_inf (W) ≈ 0.33 × N × V × (T_i − T_o)`, with V in m³ and N in air
changes per hour (sensible only). Typical N: new double poly 0.5–1.0; new glass
0.75–1.5; old glass 2–4. Wind raises N.

**Perimeter/floor:** often small; add per-metre perimeter loss for uninsulated foundations.

**Worked example:** 30 × 50 m gutter-connected double poly, floor 1,500 m², cover
area ≈ 2,100 m², volume ≈ 6,750 m³, T_i = 18 °C, T_o = −15 °C (ΔT 33 K).
Cover: 4.0 × 2,100 × 33 ≈ 277 kW. Infiltration at N 0.75: 0.33 × 0.75 × 6,750 × 33
≈ 55 kW. Total ≈ 330 kW (≈ 220 W/m² floor). Add 10–15 % for pick-up and distribution;
split across at least two units so one failure does not freeze the crop.

## 3. Summer ventilation
Energy balance on the house, with ρc_p ≈ 1,200 J/m³·K:
`V (m³/s) = (τ × R_s × f_sensible × A_floor) / (1,200 × ΔT)`
With R_s = 800 W/m², transmissivity τ = 0.7, sensible fraction ≈ 0.5 (a transpiring
crop takes the rest as latent heat) and ΔT = 4 K: V ≈ 0.058 m³/s per m² floor. The
long-standing rule is **about 0.04–0.06 m³/s per m² floor (8–12 cfm/ft²)** at sea level,
increased for altitude, high radiation and a smaller allowed temperature rise.
Fan selection uses rated flow at about 30 Pa (0.125 in. water) static pressure.

## 4. Evaporative pad-and-fan cooling
- Leaving air temperature: `T_out = T_db − η (T_db − T_wb)`; 100 mm cellulose pads
  reach η ≈ 0.75–0.85.
- Pad face velocity about 1.25 m/s for 100 mm and 1.75 m/s for 150 mm pads (vendor data).
- Pad area = ventilation flow ÷ face velocity. Keep fan-to-pad distance around
  30–60 m; longer houses get a large temperature gradient.
- Cooling is weak in humid climates (small wet-bulb depression); fogging and shading
  are the alternatives.

## 5. Supplemental lighting
- `DLI (mol/m²·day) = PPFD (µmol/m²·s) × hours × 0.0036`
- Targets (typical): lettuce 12–17, tomato/cucumber 20–30, cannabis flowering 35–45.
- `PPFD_supp = (DLI_target − DLI_natural) / (hours × 0.0036)`
- Electrical load: `W/m² ≈ PPFD_supp / (efficacy × utilisation)`. Current horticultural
  LEDs are roughly 2.5–3.5 µmol/J; utilisation 0.8–0.9 after edge and shading losses.
  Example: 150 µmol/m²·s ÷ (2.8 × 0.85) ≈ 63 W/m².
- Check uniformity (min/average ≥ 0.8) with the vendor's photometric files.

## 6. Livestock housing (same principles)
Minimum ventilation is set by moisture, gas (NH₃, CO₂) and odour removal in cold
weather; maximum by sensible heat at a 2–3 °C rise in summer. Use per-head or
per-mass rates for the species and stage from MWPS or national guidance, staged by
fan steps and controlled inlets.

## Gotchas
- **Combustion heaters inside** need combustion air and flue venting; ethylene and CO
  from incomplete combustion damage crops and people. Boilers and gas work need
  licensed installers and local code compliance.
- Snow and wind loads on the structure require a qualified structural engineer and the
  local building code.
- Energy curtains open in the morning release cold air onto the crop; open in steps.
- Lighting adds heat (~all electrical input); reduce winter heating and raise summer cooling accordingly.
- Altitude reduces air density: increase fan flow by the density ratio.

## Verify
- [ ] Heating design uses the local 99 % design temperature and cover-specific U-values.
- [ ] Infiltration and edge losses are included; capacity is split across units.
- [ ] Ventilation rate is justified by an energy balance, corrected for altitude.
- [ ] Pad area and face velocity match the pad vendor's rating.
- [ ] Supplemental lighting meets the crop DLI on the darkest design month with checked uniformity.
