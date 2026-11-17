---
id: agriculture-environment.soil-land-management.soil-survey-mapping.soil-pit-description-and-land-capability
name: soil-pit-description-and-land-capability
category: agriculture-environment
field: soil-land-management
product: soil-survey-mapping
tags: [soil-land-management, soil-survey-mapping, soil-survey, soil-pit, soil-profile, soil-description, soil-horizons, munsell, soil-colour, mottles, redoximorphic, soil-structure, texture-by-feel, hcl-fizz-test, field-ph, land-capability, land-capability-class, lcc, luc, land-use-capability, em38, em-survey, electromagnetic-induction, eca, apparent-conductivity, paddock-mapping, soil-map, ground-truthing, qgis, trench-safety]
level: practitioner
status: gated
description: "Describe a soil pit (horizons, Munsell colour, mottles, structure, texture, fizz, pH), assign a land-capability class, and map paddock soils from EM survey plus ground-truth."
sources: ["https://www.ecfr.gov/current/title-29/part-1926/subpart-P/section-1926.652"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Soil pit description and land-capability mapping

**Goal:** know what is under each part of the farm, record it in a repeatable
format, and turn it into a map that says what each area can safely be used for.

## 1. Place the pits
- Stratify first: walk the landscape (crest, mid-slope, lower slope, flat, drainage
  line) and use any EM, yield or NDVI map to pick **one pit per distinct zone**,
  then a few auger checks between pits to confirm boundaries.
- Avoid disturbed spots (tracks, old dams, stockyards) unless they are the question.
- Log GPS for every pit and auger hole.

## 2. Dig safely
- Backhoe pit ~1–1.5 m deep or to rock; step one end so you can stand at a working
  depth. **Do not enter an unsupported pit or trench deeper than about 1.2 m** (a conservative limit: US OSHA 29 CFR 1926.652(a)(1) requires a protective system from 5 ft / 1.5 m deep unless the excavation is in stable rock, and a competent person must assess shallower ones; other jurisdictions differ, so check yours) — walls collapse without warning.
  Keep spoil ≥1 m back from the edge; fence or fill pits the same day (stock and
  children).
- Check for buried services before digging.
- Hand option: auger or hydraulic core to ~1.2 m, laid out on a tray in order.

## 3. Describe the profile (top to bottom)
Clean the sunlit face with a knife, then for each **horizon** record:
1. **Depths** (cm) of top and bottom boundary; boundary sharpness.
2. **Horizon:** O (organic litter), A (dark topsoil), E (pale, leached — bleached
   layer above a clay often signals perched water), B (subsoil, clay or iron
   accumulation), C (weathered parent material), R (rock).
3. **Colour** (moist) using a Munsell chart — hue value/chroma, e.g. `10YR 3/2`.
   Dark = organic matter; red/brown = well-drained, oxidised iron; grey/bluish =
   long waterlogging.
4. **Mottles / redox features:** abundance, size, colour. Orange and grey mottles
   mark the seasonal wet zone — the most decision-relevant thing in the pit.
5. **Texture** by feel (ribbon test — see
   `agriculture-environment.soil-land-management.soil-testing.soil-sampling-and-test-interpretation`).
6. **Structure:** grade (structureless/weak/moderate/strong), size, and type
   (granular, blocky, prismatic, columnar, platy, massive). Columnar tops often mean
   sodicity; platy layers under the topsoil mean compaction.
7. **Coarse fragments** % and type; **consistence** (loose → very firm) dry and moist.
8. **Roots:** abundance by depth, and where they stop or turn sideways.
9. **Carbonate:** a drop of dilute HCl (about 1 M, roughly 3.5% w/w: 1 part concentrated ~12 M acid to about 11 parts water, acid added to water) — no fizz / slight /
   strong. Wear eye protection.
10. **Field pH:** indicator kit (e.g. Raupach-type colour kit) every horizon.
Photograph with a tape measure in frame and a label board (site ID, date). Use your
national schema — Australian Soil and Land Survey Field Handbook, USDA Field Book
for Describing and Sampling Soils, or FAO Guidelines for Soil Description — so
others can read it.

## 4. Land-capability class
Land capability ranks how intensively land can be used **without degrading it**,
based on its most limiting factor. Several systems are in use, broadly similar:
- **USDA LCC:** Classes I–VIII (I = few limits, suits cultivation; V–VII = grazing
  or forestry; VIII = conservation only) with subclasses e (erosion), w (wetness),
  s (soil root-zone), c (climate).
- **NZ LUC** and **NSW LSC** each use eight classes on the same idea.
Method: for each map unit list slope, erosion hazard, wetness/drainage, rooting
depth, salinity/sodicity, rockiness and climate. The class is set by the **worst**
factor — deep fertile loam on a 25% slope is limited by slope. Write the limiting
factor next to the class (e.g. `IVe`).

## 5. Build the paddock map
1. **EM survey** (e.g. EM38 towed behind a quad with GNSS): apparent conductivity
   (ECa) responds to clay, moisture and salt together. Vertical-dipole mode reads to
   ~1.5 m, horizontal ~0.75 m (gated: unconfirmed, source is paywalled or blocked). Survey when the profile is uniformly moist, on
   transects ~10–20 m apart (gated: unconfirmed, source is paywalled or blocked).
2. Interpolate in QGIS (or the vendor's software), classify into 3–5 zones.
3. **Ground-truth:** pits/cores in each zone to explain *why* ECa differs — high ECa
   might be clay (good water holding) or salt (bad). The map means nothing until
   checked.
4. Draw final soil-type boundaries, attach pit descriptions and land-capability class
   per polygon, and use them for zone soil sampling and management.

## Gotchas
- Colour is read **moist** and in daylight, not in shade or under a car's headlights.
- A single pit describes a point; boundaries come from augering between pits.
- EM readings drift with temperature; re-run a short calibration line at start and end.
- Capability ≠ suitability: a class says what is sustainable, not what is profitable.

**Uncertainty:** class definitions and trench-safety depths differ between countries;
summaries here are simplified. Not field-verified by the author.

## Verify
- [ ] Each zone has a pit (or core) described horizon by horizon with photos and GPS.
- [ ] Mottle depth and root-limiting depth recorded for every pit.
- [ ] Every map unit has a capability class with its limiting factor letter.
- [ ] EM zones ground-truthed and the cause of each zone's ECa explained.
- [ ] No pit was entered unsupported beyond safe depth; all pits filled or fenced.

## Checked

- Date: 2026-10-25. Jurisdiction: United States for the excavation rule (OSHA 29 CFR 1926.652); other jurisdictions differ.
- Confirmed against: 29 CFR 1926.652(a)(1) requires a protective system for excavations 5 ft (1.5 m) or deeper unless in stable rock, and for shallower ones where a competent person finds a cave-in risk (eCFR); the HCl strength was corrected by arithmetic (1 M is about 3.5% w/w, made by adding 1 part of about 12 M concentrated acid to about 11 parts water; the old text equated 1 M with 10%).
- Not confirmed: the EM38 effective depths and survey line spacing (Geonics documentation not read).

Method: documentation only; no commands were run.
