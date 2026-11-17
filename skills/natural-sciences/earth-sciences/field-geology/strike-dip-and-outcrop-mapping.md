---
id: natural-sciences.earth-sciences.field-geology.strike-dip-and-outcrop-mapping
name: strike-dip-and-outcrop-mapping
category: natural-sciences
field: earth-sciences
product: field-geology
tags: [field-geology, geological-mapping, strike-and-dip, dip-direction, compass-clinometer, brunton, freiberg, clar-compass, fieldmove, stereonet, outcrop-description, field-notebook, magnetic-declination, right-hand-rule, cross-section, rule-of-vs, bedding, foliation, lineation, structural-geology, base-map, gps]
level: practitioner
status: gated
description: "Take reliable strike/dip readings, record outcrops in a notebook a stranger can use, and build a geological map and cross-section from them, including the classic errors."
sources: ["Barnes & Lisle, Basic Geological Mapping (Wiley)", "Coe (ed.), Geological Field Techniques (Wiley-Blackwell)", "https://pages.uoregon.edu/millerm/Srpatterns.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Strike, dip and outcrop mapping

**Goal:** turn a day of walking over rock into station records and a map that another
geologist could re-occupy and check — with orientations you can trust.

## 1. Before you go out
- **Base map** at a scale that suits the task (1:10 000 for detailed student mapping,
  1:25 000–1:50 000 for reconnaissance), plus air photos or satellite imagery.
- **Set declination on the compass** for the date and place (look it up from a national
  geomagnetic model, e.g. NOAA/BGS calculators). Record in the notebook whether bearings
  are true or magnetic. Mixed conventions in one notebook are the most common silent error.
- Agree a **convention** and write it on the first page: strike/dip with the right-hand
  rule (dip is to the right when facing along strike, e.g. `040/35`), or dip direction/dip
  (`130/35`). Both are fine; mixing them is not.

## 2. Taking an orientation reading
1. Find a **true bedding surface** (or cleavage, foliation, joint — say which). Avoid
   cross-bed foresets, slumped blocks, frost-heaved or loose boulders. Ask: is this outcrop
   *in place*? Look for continuity with neighbouring rock and consistent jointing.
2. If the surface is small or rough, lay a **clipboard or notebook** on it to average.
3. Clinometer: find the steepest line (dip) and its direction; strike is perpendicular.
   With a Clar/Freiberg-type compass you get dip direction and dip in one move.
4. **Take 3–5 readings** across the outcrop; record them all, not a mental average.
5. Keep **magnetic objects away**: hammer, phone, vehicle, magnetite-rich rock (basalts,
   banded ironstones can deflect needles noticeably (gated: unconfirmed, source is paywalled or blocked)). If readings jump about on a
   mafic outcrop, sight a bearing from a distance or use a sun compass/known landmark.
6. Phone apps (FieldMove, Rocklogger, StraboSpot) are fast but calibrate the magnetometer
   each day and check against an analogue compass at the first stations — phones can be
   off by several degrees and drift (gated: unconfirmed, source is paywalled or blocked). *Uncertainty note: app accuracy varies a lot by handset.*

## 3. The station record
Each station gets: ID, grid ref/GPS (with datum, e.g. WGS84), time, rock type and
description (colour fresh/weathered, grain size, texture, minerals, fossils, sedimentary
structures), all orientations with type labels (`S0` bedding, `S1` cleavage, `L` lineation),
**way-up evidence** (graded beds, cross-bed truncations, load casts), samples taken with
bag numbers, photos with a scale and a note of direction, and a sketch. Write facts and
interpretation separately ("contact not exposed; inferred from slope break").

## 4. From stations to map
- Plot outcrops as you go, inking only what you saw; **draw contacts in the field**, not in
  the evening — you need the topography in front of you.
- Use the **rule of Vs**: where a dipping contact crosses a valley, the V points down-dip; if the dip is steeper than the valley gradient and the beds dip downstream, the V points downstream, and if the dip is shallower than the gradient the V points upstream. Horizontal beds follow contours; vertical ones
  cut straight across (checked against university map-pattern pages). If your contact disobeys topography, your dip or your contact is wrong.
- Symbol every reading with its strike line and dip number; mark inferred contacts dashed.

## 5. Cross-section
Choose a line roughly perpendicular to strike. Draw the topographic profile with **no
vertical exaggeration** (exaggeration distorts dips). Where the section is oblique to
strike, use **apparent dip**: tan(apparent) = tan(true) × sin(angle between section and
strike; recomputed: a 35 degree true dip with the section perpendicular to strike gives 35). Project nearby readings onto the line along strike, not perpendicularly.

## Gotchas
- Reading on a joint face thinking it's bedding — check for layering on more than one face.
- Overturned beds: note way-up, use the overturned symbol.
- Forgetting to set or record declination; using a borrowed compass already set for somewhere else.
- GPS on a cliff base or in a gorge can be tens of metres off; check against the map.

## Verify
- [ ] Notebook page 1 states the orientation convention and declination (true vs magnetic).
- [ ] Every reading says what surface it is (S0/S1/joint) and has 3+ repeats.
- [ ] Contacts on the map obey the rule of Vs given the measured dips.
- [ ] A cross-section with no vertical exaggeration reproduces the map pattern.
- [ ] Another person could find each station from its grid ref and description.
