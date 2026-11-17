---
id: engineering-technology.agricultural-and-biosystems-engineering.irrigation-design.et0-penman-monteith-inputs-and-checks
name: et0-penman-monteith-inputs-and-checks
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: irrigation-design
tags: [agricultural-and-biosystems-engineering, irrigation-design, et0-calculation, crop-water-requirements, evapotranspiration, fao-56, penman-monteith, weather-data-quality, wind-2m]
level: practitioner
status: verified
description: "Compute FAO-56 reference evapotranspiration from station data: unit conversions, wind height, pressure, vapour pressure, radiation terms and weather-record quality checks."
sources:
  - "Allen, Pereira, Raes & Smith, FAO Irrigation and Drainage Paper 56: Crop Evapotranspiration (https://www.fao.org/4/x0490e/x0490e00.htm)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# ET0 inputs and checks (FAO-56 Penman-Monteith)

**Goal:** a trustworthy daily ET0 series for design and scheduling.

## Inputs and the formulas that trip people
- **Temperature**: Tmax, Tmin, Tmean. Saturation vapour pressure `es(T) = 0.6108 exp(17.27 T / (T + 237.3))` kPa; mean `es` is the average of es(Tmax) and es(Tmin), not es(Tmean).
- **Slope of curve**: `Delta = 4098 es / (T + 237.3)^2`.
- **Pressure and psychrometric constant**: `P = 101.3 ((293 - 0.0065 z) / 293)^5.26` kPa, `gamma = 0.000665 P`. Use station elevation z.
- **Actual vapour pressure ea**: from dew point, or from RHmax and RHmin, or RHmean.
- **Wind**: convert wind measured at height z_m to 2 m: `u2 = uz x 4.87 / ln(67.8 z_m - 5.42)`.
- **Radiation**: measured Rs, or estimated from sunshine hours (Angstrom) or Tmax-Tmin (Hargreaves form). Net radiation Rn = Rns - Rnl, with Rnl depending on Rs/Rso cloudiness and ea.
- Daily soil heat flux G is approximately zero.

## Quality checks
1. The station should represent a well-watered grass or similar reference surface; dry, hot surroundings bias temperature and humidity (aridity effects). FAO-56 provides a correction method for non-reference sites.
2. Check for sensor drift: RHmax should reach near 100 percent on calm mornings; Tmin should be close to the dew point at well-watered humid sites (FAO-56); in arid regions Tmin may exceed Tdew (subtract 2-3 C).
3. Compare the computed ET0 with a nearby reference station, a lysimeter, or pan data with an appropriate pan coefficient.
4. Use the tool (CROPWAT, FAO ET0 calculator or a validated spreadsheet) rather than hand code unless you test it against FAO-56 worked examples.

## Gotchas
- Mixing kPa and hPa, MJ m-2 d-1 and W m-2 are the common error sources.
- FAO-56 says u2 should be limited to at least 0.5 m/s in the ET0 equation.

## Verify
- [ ] FAO-56 worked example reproduced within rounding.
- [ ] Annual ET0 is plausible against regional climate atlases.
