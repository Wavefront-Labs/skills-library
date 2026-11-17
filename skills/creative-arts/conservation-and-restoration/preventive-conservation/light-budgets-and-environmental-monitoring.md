---
id: creative-arts.conservation-and-restoration.preventive-conservation.light-budgets-and-environmental-monitoring
name: light-budgets-and-environmental-monitoring
category: creative-arts
field: conservation-and-restoration
product: preventive-conservation
tags: [preventive-conservation, collections-care, light-budget, lux, lux-hours, annual-exposure, uv, microwatts-per-lumen, light-sensitivity, blue-wool-standard, fading, rotation, environmental-monitoring, relative-humidity, rh, temperature, data-loggers, hygrometer, climate-control, bizot-green-protocol, pas-198, ashrae, fluctuation, mould-risk, display-cases, museum-lighting, led, integrated-pest-management, agents-of-deterioration]
level: practitioner
status: draft
description: "Set light budgets and monitor RH/temperature for a collection: classify sensitivity, convert lux limits to annual lux-hours, place and read loggers, and act on fluctuations not single readings."
sources:
  - "Canadian Conservation Institute, Agents of Deterioration (light, UV and IR; incorrect RH; incorrect temperature)"
  - "BSI PAS 198:2012, Specification for environmental conditions for cultural collections"
  - "Bizot Group / AIC-IIC interim environmental guidelines (2014 onward)"
  - "ASHRAE Handbook, Museums, Galleries, Archives and Libraries chapter"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Light budgets and environmental monitoring

**Goal:** slow the two slow killers of collections — **light damage** (cumulative and
irreversible) and **damaging humidity/temperature** — by setting exposure limits per
object and watching the environment with loggers, so problems are caught as trends.

> **Status: draft.** Figures below are widely cited conventional values. Current guidance
> (CCI, PAS 198, Bizot) favours risk-based, object-specific targets over one-size rules;
> treat these as defaults to adapt, not law.

## Light: think in dose, not brightness
Damage ∝ **illuminance × time**. 50 lux for 10 hours does roughly what 500 lux does in one.

| Sensitivity | Examples | Conventional limit |
|---|---|---|
| High | watercolours, works on paper, textiles, dyed materials, photographs, manuscripts | **50 lux** |
| Medium | oil and tempera paintings, undyed organics, wood, lacquer | **150–200 lux** |
| Low | stone, metal, ceramic, most glass | no strict limit (heat/IR still matter) |

**Annual budget** = lux × hours open per day × days per year.
Example: 50 lux × 8 h × 300 days = **120,000 lux-hours/year**. Many institutions cap
high-sensitivity items lower (e.g. ~50,000 lux-h) by rotating them off display, or by
lighting only when visitors are present (motion sensors).

**UV** contributes damage but no useful visibility: aim for **< 75 µW/lm** (older target),
ideally near zero — modern LEDs emit almost none; filter windows and older fluorescents.

How to manage it:
- Measure with a lux meter at the object surface, at the brightest point.
- Track cumulative exposure per sensitive object in the collection database.
- Rotate: e.g. three to six months on, then years in dark storage, by sensitivity.
- Blue Wool standard cards placed in a case give a crude cumulative fade check.

## Relative humidity and temperature
Typical targets for mixed collections: **~40–60% RH**, with gradual seasonal drift
allowed and **short-term swings limited (often ±10% RH within 24 h)**; temperature
~16–25 °C. Specific risks:
- **> ~65–70% RH** for days: mould risk, corrosion, pests.
- **Low RH** (< ~30%): cracking of wood, paint, ivory, adhesives.
- **Rapid swings:** the main mechanical risk for panel paintings, veneers, drums.
- **Metals and archaeological iron** want much drier microclimates (often < 35%, much lower for
  unstable iron) — use cases with silica gel.

## Monitoring with loggers
1. **Place** digital RH/T loggers in each room and in cases, away from vents, radiators,
   outside walls and direct sun — unless that's the microclimate you're checking.
   Record locations.
2. Log every **15–60 min**; download or sync at least monthly.
3. **Calibrate/check** loggers yearly (salt test or reference instrument); drift of
   several % RH is common.
4. **Read trends:** daily range, seasonal drift, spikes when doors open or HVAC cycles.
   Graph the month; compare rooms.
5. Act on **sustained patterns**: a single spike rarely matters; a week at 70% does.

## Gotchas
- **Heating changes RH:** warming a cold building in winter drops RH sharply.
  Conservation heating (heating to control RH rather than comfort) exists for this.
- Tight cases buffer swings — but trap off-gassing from MDF, adhesives and paints;
  test materials (Oddy test) before building.
- Sensors in a duct aren't the environment at the object.
- Light damage is cumulative and can't be reversed; "it's only for a week" adds up.

## Safety
Silica gel conditioning and pest freezing are low risk; avoid legacy pesticides
(naphthalene, paradichlorobenzene) found in old storage — gloves, ventilation, proper disposal.

## Verify
- [ ] Each display object classified by light sensitivity with a lux limit and annual budget.
- [ ] Lux and UV measured at the object; exposure tracked.
- [ ] Loggers placed, documented, calibrated, downloaded on schedule.
- [ ] RH/T targets written down, with action thresholds for sustained excursions.
- [ ] Monthly review notes what changed and what was done.
