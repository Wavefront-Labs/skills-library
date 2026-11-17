---
id: defence-public-safety.intelligence-and-espionage.imagery-and-geospatial-intelligence.imagery-interpretation-change-detection-and-reporting
name: imagery-interpretation-change-detection-and-reporting
category: defence-public-safety
field: intelligence-and-espionage
product: imagery-and-geospatial-intelligence
tags: [intelligence-and-espionage, imagery-and-geospatial-intelligence, imint, geoint, imagery-analysis, imagery-interpretation, photo-interpretation, satellite-imagery, change-detection, niirs, gsd, ground-sample-distance, sar, synthetic-aperture-radar, multispectral, shadow-mensuration, signatures, order-of-battle, geolocation, chronolocation, sentinel-2, landsat, planet, maxar, gis, qgis, cuban-missile-crisis, deception, camouflage, intelligence-studies]
level: practitioner
status: draft
description: "Imagery and geospatial intelligence method: interpretation keys, GSD and NIIRS, shadow mensuration, change detection, SAR vs optical, deception, and confidence-graded reporting."
sources: ["US NGA, GEOINT Basic Doctrine Publication 1.0 (2018, unclassified)", "Federation of American Scientists, NIIRS civil and military scales", "Brugioni, 'Eyeball to Eyeball: The Inside Story of the Cuban Missile Crisis' (1991)", "Brugioni, 'Photo Fakery' (1999)", "ESA Copernicus Sentinel-2 and USGS Landsat documentation"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Imagery interpretation, change detection and reporting

**Goal:** turn an image of a place into a defensible statement about what is there,
what changed and how sure you are. Applies to government GEOINT and to the open
commercial-imagery work now done by researchers, journalists and NGOs (e.g. tracking
facility construction, conflict damage, deforestation).

## 1. Know what your imagery can show
- **Ground sample distance (GSD)** — the ground size of one pixel. Rough rule: you need
  several pixels across an object to *detect* it and many more to *identify* it. Free
  Sentinel-2 (10 m) shows fields, large buildings, burn scars; commercial 30–50 cm shows
  vehicles by class; aircraft type identification typically needs finer.
- **NIIRS** (National Imagery Interpretability Rating Scale, 0–9) rates what tasks an
  image supports, not raw pixel size; haze, angle and compression all lower it.
- **Optical vs SAR:** optical needs daylight and clear sky; synthetic aperture radar sees
  through cloud and at night, shows texture, metal and moisture, but is harder to read
  (layover, speckle, foreshortening). Multispectral bands reveal vegetation stress,
  disturbed soil and burn areas invisible in true colour.

## 2. Interpretation keys (the classic elements)
Size, **shape**, **shadow**, tone/colour, texture, pattern, **site** (what a location
allows), and **association** (what objects are found together). Association carries
the most weight: a lone building is ambiguous; a building plus a security perimeter, a
dedicated power line and specific vehicle types is a signature. Build reference
signatures from known examples before judging unknowns.

## 3. Measurement
- **Shadow mensuration:** height = shadow length × tan(sun elevation). Sun elevation comes
  from image metadata or can be computed from time and location. Correct for sloping
  ground and off-nadir view angle, or heights will be wrong by a large margin.
- Measure in a GIS (e.g. QGIS) on orthorectified imagery; raw off-nadir imagery distorts
  distances. State the measurement uncertainty.

## 4. Change detection
- Compare the same place at different dates, ideally same sensor, similar sun angle and
  season. Seasonal vegetation, shadows and snow produce false "changes".
- Build a **timeline** rather than a pair: construction, activity and damage have
  sequences, and a single before/after misses when and how.
- Absence of change is a finding too — but only if revisit frequency could have caught it.

## 5. Deception and error
- Camouflage, decoys (inflatable vehicles, painted aircraft outlines) and activity timed
  for revisit gaps are long-standing countermeasures. The Cuban Missile Crisis (1962) is
  the textbook success — U-2 imagery identified MRBM sites by comparison with known Soviet
  site patterns — and also a reminder that interpreters missed some deployed systems.
- Mirror-imaging: assuming a facility is laid out the way your side would build it.
- Over-claiming from one image. Bring in other sources (open records, SIGINT, HUMINT)
  before confident functional judgements.

## 6. Reporting
State: image source and date/time, GSD/quality, location (coordinates and datum),
what is observed (fact), what it is assessed to be (judgement) with estimative language
and confidence, and what would change the assessment. Annotate images minimally and
legibly; keep an unannotated copy. For open-source work, verify provenance first (see
`media-communication.editorial-photography-and-photojournalism.image-verification.verifying-an-image-provenance-geolocation-and-manipulation`).
Gotcha: publishing precise imagery of humanitarian sites or civilians in a conflict can
endanger them; weigh harm before release.

## Verify
- [ ] Imagery date, sensor, GSD and quality are stated in the report.
- [ ] Observed facts are separated from functional assessments.
- [ ] Heights/sizes include the method and an uncertainty band.
- [ ] Changes are checked against season, sun angle and sensor differences.
- [ ] At least one alternative explanation (including deception) was considered.
