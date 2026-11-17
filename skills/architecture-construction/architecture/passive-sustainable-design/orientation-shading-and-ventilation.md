---
id: architecture-construction.architecture.passive-sustainable-design.orientation-shading-and-ventilation
name: orientation-shading-and-ventilation
category: architecture-construction
field: architecture
product: passive-sustainable-design
tags: [passive-sustainable-design, passive-design, bioclimatic-design, climate-responsive-design, solar-orientation, sun-path, shading, overhang, brise-soleil, fins, solar-gain, shgc, g-value, cross-ventilation, stack-ventilation, natural-ventilation, thermal-mass, night-purge, window-to-wall-ratio, wwr, daylighting, daylight-factor, glare, climate-analysis, epw, ladybug, climate-consultant, passivhaus, overheating, low-energy-design]
level: practitioner
status: draft
description: "Design the passive basics from climate data: orient and proportion the plan, size overhangs and fins by sun angle, set glazing ratios, and plan cross and stack ventilation before mechanical systems."
sources: ["Givoni / Olgyay bioclimatic design principles", "CIBSE Guide A and TM52 (overheating)", "Passivhaus Institut planning principles", "US DOE / climate design guidance"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Orientation, shading and natural ventilation

**Goal:** get the building's form, openings and shading right for its climate at
concept stage, so heating, cooling and lighting loads are small before any equipment
is chosen. These moves are nearly free early and very expensive late.

## 1. Read the climate first
Get an **EPW weather file** for the nearest station and plot: monthly temperature
ranges, humidity, solar radiation by orientation, wind rose by season, and a
psychrometric chart with comfort zone (Climate Consultant, Ladybug Tools, or similar).
Classify the strategy:
- **Heating-dominated:** maximise winter solar gain, compact form, airtight and insulated.
- **Cooling-dominated, hot-dry:** shade, thermal mass with night purge, small openings
  to sun, courtyards.
- **Hot-humid:** shade everything, maximise cross-ventilation, lightweight raised
  construction (mass gives little benefit when nights stay warm).
- **Mixed:** seasonal shading that admits low winter sun and blocks high summer sun.

## 2. Orientation and form
- Long axis roughly **east–west** so the main glazing faces the equator (south in the
  northern hemisphere, north in the southern). Within about ±15–20° of true is usually
  acceptable (rule of thumb).
- Minimise east and west glazing — low sun angles are hard to shade and drive
  afternoon overheating.
- Plan depth: for daylight and cross-ventilation, keep habitable rooms within roughly
  2–2.5× head height of a window (single-sided) or ~5× ceiling height overall for
  cross-ventilated plans (CIBSE-style rules of thumb).

## 3. Size shading by geometry
For an equator-facing horizontal overhang:
`projection = window height (from sill to underside of overhang) ÷ tan(solar altitude)`
using the **summer** noon altitude you want to block. Solar noon altitude ≈
`90° − latitude + declination` (declination +23.45° at June solstice, −23.45° at December,
northern hemisphere; flip for southern).
Example: latitude 40° N, block sun from about May–August: noon altitude ~70°;
for 1.5 m of glazing below the overhang, projection ≈ 1.5 ÷ tan 70° ≈ 0.55 m. Check
that winter sun (altitude ~26.5° at solstice) still reaches the glass.
- East/west: **vertical fins** or adjustable external shading; overhangs barely work.
- External shading beats internal blinds — once sun is through the glass, most of
  its heat is inside.
- Verify with a sun-path/shadow study for the critical dates and hours, not just noon.

## 4. Glazing
- Window-to-wall ratio: moderate (often 20–40% per façade as a starting band);
  more glass is rarely better for energy.
- Choose **g-value/SHGC** by orientation: higher on shaded equator-facing glass in cold
  climates, low on east/west.

## 5. Natural ventilation
- **Cross-ventilation:** openings on opposite (or adjacent) walls facing the
  prevailing summer breeze; outlet area ≥ inlet improves flow.
- **Stack:** vent low and high; driving force grows with height difference and
  inside-outside temperature difference. Use stairs, atria or chimneys.
- **Night purge** with exposed thermal mass where nights are cool (diurnal swing
  roughly >8–10 K as a guide): secure, rain-proof openable vents.
- Check noise, security and air quality — they often kill openable windows in practice.

## Gotchas
- Overheating is now a common failure of well-insulated homes; check against an
  overheating criterion (e.g. CIBSE TM52/TM59 where applicable).
- Rules of thumb vary by source; *validate with dynamic simulation* for anything beyond
  concept.

## Verify
- [ ] Climate strategy written from actual weather data, not assumption.
- [ ] Equator-facing shading blocks summer sun and admits winter sun on a sun-path check.
- [ ] East/west glazing minimised or externally shaded.
- [ ] Every habitable room has a ventilation path (cross or stack) drawn in section.
- [ ] Overheating risk assessed for the worst-case room.
