---
id: natural-sciences.atmospheric-sciences.synoptic-dynamic-meteorology.surface-chart-analysis-and-fronts
name: surface-chart-analysis-and-fronts
category: natural-sciences
field: atmospheric-sciences
product: synoptic-dynamic-meteorology
tags: [synoptic-dynamic-meteorology, synoptic-meteorology, surface-analysis, weather-map, station-model, isobars, mslp, sea-level-pressure, isobar-interval, cold-front, warm-front, occluded-front, stationary-front, trough, dryline, dewpoint, wind-shift, pressure-tendency, thermal-advection, 850-hpa, 500-hpa, thickness, upper-air-analysis, norwegian-cyclone-model, frontogenesis, metar]
level: practitioner
status: docs-checked
description: "Hand-analyse a surface chart: decode station plots, draw isobars, locate cold, warm and occluded fronts from temperature, dewpoint, wind shift and pressure, then check aloft."
sources: [https://www.wpc.ncep.noaa.gov/html/stationplot.shtml]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Surface chart analysis and locating fronts

**Goal:** turn a plot of station observations into an analysed chart — isobars, highs
and lows, and fronts drawn where the data put them — and cross-check with upper-air
fields so the analysis is physically consistent.

## 1. Read the station model
Each station plot (from METAR/SYNOP) shows temperature, dewpoint, sea-level pressure,
pressure tendency, wind and present weather around the station circle (the layout is
in the plotted legend of your service: use that for positions and units).
- **Sea-level pressure** is plotted in tenths of hPa/mb with the leading 10 or 9
  omitted: `103` → 1010.3, `987` → 998.7, `872` → 987.2, `410` → 1041.0 (the working
  rule is that a value below 500 takes the prefix 10 and one of 500 or more takes 9).
- **Pressure tendency:** the number is the 3-hour change in tenths of hPa; the symbol
  shows how the change occurred.
- **Wind barb** points *from* the wind direction in knots, plotted in 5 kt steps: half
  barb = 5, full barb = 10, pennant = 50. A circle with no barb is calm.
- A present-weather symbol is plotted when precipitation is occurring or conditions
  reduce visibility.

## 2. Isobars
- Draw isobars at a fixed interval (check the interval your forecasting service uses)
  and keep it constant over the chart.
- Start in a data-dense area; interpolate between stations; isobars never cross, split
  or end except at chart edges.
- Check against the winds: above the boundary layer flow is roughly parallel to isobars
  (geostrophic); at the surface, friction turns it across isobars toward low pressure.
  Tighter spacing = stronger wind.
- Mark H and L centres with central pressure.

## 3. Find the fronts — use several signals together
A front is the warm-air edge of a zone of strong temperature (more precisely, density)
gradient. Look for coincident:
| Signal | Cold front | Warm front |
|---|---|---|
| Temperature | Sharp drop behind | Rise after passage |
| Dewpoint | Usually drops behind | Rises |
| Wind shift | Veers sharply (Northern Hemisphere) | Veers (Northern Hemisphere) |
| Pressure | Lowest at passage, sharp rise after | Falls ahead, levels after |
| Weather | Narrow band of showers/thunderstorms | Broad area of stratiform precip ahead |
Isobars **kink** at fronts, with the kink pointing toward higher pressure — the front lies
in a trough. In the Southern Hemisphere wind shifts are backing, not veering.

- **Occluded front:** where the cold front has caught the warm front, extending from the
  low's centre to the triple point.
- **Stationary front:** little movement, winds roughly parallel on both sides.
- **Dryline** (e.g. US Great Plains): strong dewpoint gradient with little temperature
  contrast — not a front by temperature.
- **Troughs** without air-mass change are drawn as dashed lines, not fronts.

## 4. Check aloft
- 850 hPa temperatures show the baroclinic zone without surface diurnal noise; the
  surface front should sit on the warm edge of the 850 hPa gradient.
- **1000–500 hPa thickness** lines bunch along frontal zones; cold advection is where wind
  blows from low to high thickness.
- At 500 hPa, surface lows deepen under the region **ahead of an upper trough** (positive
  vorticity advection, divergence aloft).
- Satellite imagery: cold fronts often show as a long cloud band; check your drawn
  position against it.

## Gotchas
- Diurnal heating and coastal effects mimic frontal temperature contrasts; rely on wind
  shift + pressure trough + dewpoint, not temperature alone.
- Mountain stations reduce poorly to sea level; their pressure values can be misleading.
- Shallow cold air (cold-air damming) can hide a warm front aloft.
- Analysis is a hypothesis; re-draw at the next chart time and check continuity of
  front motion.

Plotting conventions (units, codes) vary by national service.

## Checked
2026-11-01. Confirmed in the NOAA WPC page "Station Model Information for Weather
Observations": pressure plotted in tenths with leading 10 or 9 omitted and the examples
above, tendency as a 3-hour change in tenths, wind barb values and 5 kt steps, calm
circle, when a weather symbol is plotted. Removed: the station-plot position layout,
the 4 hPa isobar interval, the 10-30 degree friction turning, and the front speed
range (none stated on a page read). The frontal signals and upper-air checks are
qualitative synoptic practice, not sourced figures.
Method: documentation only; no commands were run.

## Verify
- [ ] Pressure values decoded correctly; isobars at a consistent interval and consistent with winds.
- [ ] Every drawn front supported by at least three signals (T, Td, wind shift, pressure trough/tendency, weather).
- [ ] Fronts lie in pressure troughs on the warm edge of the 850 hPa gradient.
- [ ] Positions consistent with satellite cloud bands and the previous analysis.
