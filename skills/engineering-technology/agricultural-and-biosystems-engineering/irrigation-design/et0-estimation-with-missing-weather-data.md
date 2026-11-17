---
id: engineering-technology.agricultural-and-biosystems-engineering.irrigation-design.et0-estimation-with-missing-weather-data
name: et0-estimation-with-missing-weather-data
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: irrigation-design
tags: [agricultural-and-biosystems-engineering, irrigation-design, hargreaves-et0, crop-water-requirements, evapotranspiration, missing-weather-data, fao-56, radiation-estimate]
level: practitioner
status: verified
description: "Estimate ET0 when weather records are incomplete: Hargreaves equation, FAO-56 procedures for dew point, wind and radiation substitutes, and when to flag low confidence."
sources:
  - "Allen, Pereira, Raes & Smith, FAO Irrigation and Drainage Paper 56: Crop Evapotranspiration (https://www.fao.org/4/x0490e/x0490e00.htm)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# ET0 with missing weather data

**Goal:** a usable ET0 when only temperature, or some variables, are available.

## Hierarchy (FAO-56 chapter 3, https://www.fao.org/4/x0490e/x0490e07.htm)
1. **Missing humidity**: estimate dew temperature as Tmin (well-watered, humid sites); for arid regions FAO-56 says Tmin may be better approximated by subtracting 2-3 C.
2. **Missing radiation**: estimate Rs from the temperature range `Rs = kRs sqrt(Tmax - Tmin) Ra`, with kRs between 0.16 and 0.19 (about 0.16 for interior and about 0.19 for coastal locations, FAO-56 Eq. 50); Ra is extraterrestrial radiation from latitude and day of year.
3. **Missing wind**: use a regional or nearby-station average, or the FAO-56 global default u2 = 2 m/s as a last resort.
4. Apply the full Penman-Monteith with these estimates.

## Hargreaves (temperature only)
`ET0 = 0.0023 Ra (Tmean + 17.8) sqrt(Tmax - Tmin)` with ET0 and Ra both in mm/day (FAO-56 Eq. 52). It needs only Tmax and Tmin. FAO-56 says to verify it in each region against Penman-Monteith and, if needed, calibrate with ET0 = a + b ET0(Eq. 52).

## Gotchas
- Check Tmax - Tmin quality: a miss-set screen produces nonsense.
- Do not use pan evaporation without an appropriate pan coefficient and fetch assessment.
- Flag low confidence in the design report and use a safety margin in design capacity.

## Verify
- [ ] Reference period compared with a station that has full data; bias stated.
