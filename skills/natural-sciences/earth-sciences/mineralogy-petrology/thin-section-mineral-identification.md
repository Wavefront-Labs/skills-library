---
id: natural-sciences.earth-sciences.mineralogy-petrology.thin-section-mineral-identification
name: thin-section-mineral-identification
category: natural-sciences
field: earth-sciences
product: mineralogy-petrology
tags: [mineralogy-petrology, petrography, thin-section, optical-mineralogy, polarizing-microscope, petrographic-microscope, ppl, xpl, crossed-polars, birefringence, interference-colours, michel-levy-chart, extinction-angle, pleochroism, relief, twinning, plagioclase, quartz, feldspar, pyroxene, amphibole, olivine, modal-analysis, point-counting]
level: practitioner
status: draft
description: "Identify common rock-forming minerals in a 30 µm thin section with a polarizing microscope: relief, colour, pleochroism, birefringence, extinction, twinning, then name the rock."
sources: ["Nesse, Introduction to Optical Mineralogy (OUP)", "MacKenzie & Adams, A Colour Atlas of Rocks and Minerals in Thin Section"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Thin-section mineral identification

**Goal:** go from an unknown thin section to a confident mineral list, texture
description and rock name, using a fixed observation order rather than pattern-matching.

## 0. Set up the microscope
- Centre the objectives (rotate the stage; if a grain wanders in a circle, adjust the
  centring screws) — otherwise extinction angles are meaningless.
- Check the polars are crossed: with no slide, XPL should be fully black.
- Start at low power to see texture; go higher for individual grains.
- Standard section is **30 µm** thick. Quartz should show first-order grey-white at most;
  if quartz shows yellow or higher, the section is too thick and every birefringence
  estimate shifts up.

## 1. Plane-polarized light (PPL), one polar
1. **Colour and pleochroism:** rotate the stage. Biotite goes brown ↔ pale; hornblende
   green/brown ↔ paler; most clinopyroxene is near-colourless to pale green; olivine
   colourless; opaques stay black (oxides/sulphides — need reflected light to tell apart).
2. **Relief** (how much the grain stands out from the mounting medium, n ≈ 1.54):
   quartz and feldspar low; pyroxene, olivine, garnet high; calcite changes relief on
   rotation ("twinkling").
3. **Habit and cleavage:** two cleavages at ~87°/93° → pyroxene; ~56°/124° → amphibole.
   You only see the angle in sections cut roughly perpendicular to the c-axis.
4. **Alteration:** cloudy feldspar (sericite/clay), olivine rimmed by serpentine/iddingsite.

## 2. Crossed polars (XPL)
1. **Interference colour / birefringence:** find the *highest* colour of that mineral
   across many grains (most grains are not optimally oriented) and read it on the
   Michel-Lévy chart. Quartz/feldspar: 1st-order grey-white; pyroxene: up to 2nd-order;
   olivine: 2nd–3rd-order bright colours; calcite: very high-order pastel/creamy.
2. **Extinction:** parallel (orthopyroxene, sillimanite) vs inclined. Clinopyroxene
   extinction ~35–45° to cleavage; hornblende ~15–25° (*check a table; ranges vary by
   composition*).
3. **Twinning:** polysynthetic (multiple parallel stripes) → plagioclase; tartan
   cross-hatching → microcline; simple two-part Carlsbad → K-feldspar or plagioclase.
4. **Zoning:** concentric extinction bands in plagioclase record changing melt
   composition.
5. Use the **accessory plate** (gypsum, λ) for sign of elongation and, with conoscopic
   light, optic sign — the decisive test when quartz and untwinned feldspar look alike
   (quartz uniaxial +, feldspars biaxial).

## 3. Quick discriminators
- Quartz vs untwinned feldspar: feldspar often clouded by alteration; quartz clear with
  undulose extinction if strained; interference figure settles it.
- Orthopyroxene vs clinopyroxene: parallel vs inclined extinction; opx lower birefringence.
- Olivine vs pyroxene: olivine no good cleavage, irregular fractures, higher birefringence.
- Muscovite vs biotite: muscovite colourless in PPL with bright 2nd–3rd-order colours;
  both show "bird's-eye" mottled extinction.

## 4. Texture and rock name
Describe grain size, crystal shapes (euhedral/subhedral/anhedral), relationships
(ophitic, poikilitic, porphyritic with groundmass, foliation). Estimate mode with
comparison charts or **point counting** (300–500 points for a defensible mode), then
classify (e.g. QAPF for plutonic rocks). Recalculate to 100% on the classification minerals.

## Gotchas
- Judging birefringence from one grain. Survey dozens.
- Sections too thick or wedge-shaped (colours rise toward one edge).
- Bubbles and plucked holes in the epoxy mimic low-relief minerals.
- Calling all twinned feldspar plagioclase — check for tartan twinning.

## Verify
- [ ] Objectives centred, polars crossed, quartz checked for section thickness.
- [ ] Each mineral identified with at least three independent properties.
- [ ] Interference figure used where two candidates remain.
- [ ] Mode from point count or chart sums to 100% before classification.
