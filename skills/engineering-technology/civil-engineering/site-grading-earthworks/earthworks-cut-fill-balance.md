---
id: engineering-technology.civil-engineering.site-grading-earthworks.earthworks-cut-fill-balance
name: earthworks-cut-fill-balance
category: engineering-technology
field: civil-engineering
product: site-grading-earthworks
tags: [site-grading-earthworks, earthworks, cut-and-fill, cut-fill-balance, bulk-earthworks, grading-plan, finished-levels, volume-surface, tin-volume, average-end-area, mass-haul, mass-haul-diagram, free-haul, bulking-factor, shrinkage-factor, swell, topsoil-stripping, batter-slope, embankment, civil-3d, 12d, earthwork-quantities, import-export, site-works]
level: practitioner
status: verified
description: "Balance site cut and fill: grading strategy, volume calcs from surfaces, bulking and shrinkage factors, topsoil, mass-haul and batter slope limits."
sources: ["Nunnally, Construction Methods and Management", "Peurifoy et al., Construction Planning, Equipment, and Methods", "Caterpillar Performance Handbook (material swell/load factors)", "Autodesk Civil 3D Help: Volumes Dashboard and Mass Haul", "BS 6031:2009 Code of practice for earthworks (BSI; unreinforced earthworks, GC1-3 per BS EN 1997-1:2004)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Earthworks cut/fill balance — get the real quantities, not just the geometric ones

**Goal:** set finished levels so the site's cut supplies its fill (or a deliberate,
costed import/export), with volumes that account for topsoil, unsuitable material,
bulking/shrinkage and haul distance — because trucking soil on or off site is often the
single largest earthworks cost.

## 1. Surfaces and the geometric volume
1. **Existing surface (EG):** from survey/LiDAR, checked against spot levels. A 50 mm
   systematic error over a 5 ha site is 2,500 m³.
2. **Stripped surface:** EG minus topsoil depth (commonly 100–300 mm (gated: unconfirmed, source is paywalled or blocked); take it from test
   pits, not a default). Topsoil is stockpiled, never used as structural fill.
3. **Design surface:** finished levels minus pavement boxing / building slab and
   subbase thickness → **subgrade (bulk earthworks) surface**. Balancing to finished
   levels instead of subgrade is the most common error.
4. Compute volumes **stripped vs subgrade** with a TIN-to-TIN volume surface (e.g.
   Civil 3D Volumes Dashboard, 12d volume tools). For linear works, cross-section
   average-end-area is fine; it overstates curved/transitioning prisms slightly.

## 2. Convert geometric volumes to real ones
Material occupies different volumes in the bank (in situ), loose (in the truck) and
compacted (in the fill). Use factors from lab tests (in-situ density vs target
compacted density) or, at concept stage, handbook ranges:

| Material | Bank → compacted | Bank → loose (swell) |
|---|---|---|
| Clays / silts | ~0.85–0.95 (shrinks) | ~1.2–1.4 |
| Sand / gravel | ~0.90–0.95 | ~1.1–1.15 |
| Blasted rock | ~1.2–1.4 (bulks) | ~1.5–1.7 |

(Ranges are indicative from equipment handbooks and texts (gated: unconfirmed, source is paywalled or blocked); site testing should replace
them.) So 10,000 m³ of clay cut may only make ~9,000 m³ of compacted fill.

Then deduct: unsuitable material to spoil (soft, organic, contaminated), trench
spoil displaced by services, and allow for over-excavation under footings.

## 3. Adjust levels to balance
- **Raise or lower building pads and road grades** in small steps: for a site of area A,
  lowering everything by Δh changes the net by about A·Δh. 0.1 m over 2 ha = 2,000 m³.
- Keep constraints while you adjust: minimum falls (pads ~1–2% away from buildings,
  roads ≥ 0.3–0.5% on kerbed sections), stormwater outfall levels, flood immunity /
  floor-level freeboard, driveway grades, and connection levels at boundaries.
- Target a **small surplus of suitable cut** (a few percent) rather than exact zero; it
  absorbs factor uncertainty more cheaply than a late import.

## 4. Haul: the mass-haul diagram
For roads, long sites or staged lots, plot cumulative (adjusted) volume against chainage.
- Rising line = cut, falling = fill; a horizontal **balance line** cuts the curve at
  points between which cut and fill balance.
- Area between curve and balance line = haul (volume × distance). Beyond the **free-haul**
  distance (contract-specific), overhaul is paid; beyond the economic haul, borrow/waste
  is cheaper.
- Choose the equipment by haul distance: dozers for very short pushes (< ~100 m),
  scrapers for ~100–1,000 m, trucks beyond (rules of thumb (gated: unconfirmed, source is paywalled or blocked)).

## 5. Batters (cut and fill slopes)
- Typical starting slopes: fill 1V:2H, cut in stiff soil 1V:1.5–2H, slopes to be mown or
  topsoiled 1V:3H or flatter, traversable roadside fill 1V:4H or flatter (AASHTO Roadside
  Design Guide as summarised by FHWA and KYTC: foreslopes 1V:4H or flatter are traversable and recoverable; between 1V:3H and 1V:4H traversable but not recoverable (provide a recovery area at the toe); steeper than 1V:3H not traversable. Confirm in the current RDG text and your road authority's manual).
- Any batter taller than roughly 3 m, on soft ground, or near structures needs a
  geotechnical stability check; a commonly adopted target is FS ≥ 1.5 static long-term
  (≈ 1.3 short-term/temporary) (practice figures (gated: unconfirmed, source is paywalled or blocked)), but use the project's geotechnical criteria.
- Batters change the footprint: re-run volumes after setting them, and check they stay
  within the boundary.

## 6. Erosion and sediment control link
Exposed earthworks need staged stripping, diversion drains and sediment basins sized to
the local guideline (e.g. the "Blue Book" in NSW, Landcom, Managing Urban Stormwater: Soils and Construction Vol. 1, 4th ed. 2004, free PDF via NSW Environment and Heritage, state DOT manuals in the US). Plan the
balance with stockpile locations that don't sit on flow paths.

## Verify
- [ ] Volumes are stripped-EG vs subgrade, not EG vs finished level.
- [ ] Topsoil, unsuitable, trench spoil and boxing quantities are listed separately.
- [ ] Bulking/shrinkage factors are stated with their source (test data or handbook).
- [ ] Levels still meet drainage falls, flood freeboard and boundary tie-ins after balancing.
- [ ] Mass-haul (or a haul assessment) shows realistic haul distances and equipment.
- [ ] Batter slopes are within geotechnical advice and fit inside the site boundary.
