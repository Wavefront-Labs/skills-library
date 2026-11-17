---
id: natural-sciences.earth-sciences.volcanology.tephra-deposit-description-and-sampling
name: tephra-deposit-description-and-sampling
category: natural-sciences
field: earth-sciences
product: volcanology
tags: [volcanology, tephra, tephrostratigraphy, tephrochronology, pyroclastic, fall-deposit, pdc, pyroclastic-density-current, ignimbrite, isopach, isopleth, maximum-clast-size, grain-size-distribution, componentry, pumice, lapilli, ash, eruption-volume, vei, plume-height, volcanic-hazard, field-safety]
level: practitioner
status: draft
description: "Describe and sample tephra deposits so they support eruption reconstruction: unit logging, fall vs flow criteria, isopach and isopleth mapping, grain size and componentry."
sources: ["Cas & Wright, Volcanic Successions (Springer)", "Bonadonna et al., tephra deposit characterisation guidelines (IAVCEI commission work)", "Pyle 1989, thickness-area volume method"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Tephra deposit description and sampling

**Goal:** field data from pyroclastic deposits that let you reconstruct an eruption —
its sequence, style, volume and column height — and correlate it between sites.

## 1. Safety and context first
Active or recently active volcanoes: check the observatory's alert level, gas hazard
(CO2 pools in hollows, SO2/H2S), and unstable fresh deposits (gully walls collapse).
Hard hat near cliffs, gas monitor in hollows, never alone.

## 2. Log the section
Treat it like a sedimentary log (see natural-sciences.earth-sciences.sedimentology-stratigraphy.logging-a-measured-section):
bed-by-bed thickness, grain size, sorting, structures, contacts. Add for tephra:
- **Componentry**: juvenile (pumice/scoria, crystals, glass shards) vs lithic (accessory
  wall rock, accidental basement) — proportions change with vent widening and eruption phase.
- **Vesicularity** and colour of juvenile clasts.
- **Grading**: reverse grading at the base of a fall unit often records waxing column.
- **Palaeosols and erosion surfaces** between units = time gaps; they're how you separate eruptions.

## 3. Fall vs density current
| Feature | Fall | Pyroclastic density current |
|---|---|---|
| Geometry | mantles topography, even thickness locally | ponds in valleys, thins over ridges |
| Sorting | well sorted | poorly sorted, fine matrix |
| Structures | planar, grading | cross-bedding (surges), massive (ignimbrite), gas pipes |
| Other | — | carbonised wood, welding, fines-depleted pipes |

## 4. Mapping for volume and column height
- Measure **thickness** of a single correlated unit at many sites; avoid reworked or
  eroded tops (look for soil on top, compaction, slope wash).
- Measure **maximum clast size**: average of the 3–5 largest pumices and lithics on a set
  area (commonly ~0.5 m² of the unit); state the method — different conventions give
  different numbers.
- Contour thickness (**isopachs**) and maximum clast size (**isopleths**).
- Volume: integrate thickness vs √area (exponential/Pyle, power-law, or Weibull fits —
  they disagree most for distal ash, so give a range). Distal ash is often under-sampled;
  volumes are commonly underestimates.
- Column height from isopleths with a model such as Carey & Sparks (1986). Lithics are
  preferred (pumice breaks and has variable density).

## 5. Sampling
- Bulk samples per unit (and sub-unit if graded) of a known area/volume, sealed and
  labelled with height in section.
- **Grain size**: dry sieving at 1φ (or ½φ) intervals down to ~63 µm; finer by laser
  diffraction. Report Md φ and σ φ (Inman) or full distributions.
- **Glass chemistry** (EPMA, LA-ICP-MS) on fresh glass shards is the fingerprint for
  correlating tephra between sites (tephrochronology). Clean, unaltered glass; analyse
  with secondary glass standards.

## Gotchas
- Correlating units by colour alone. Use componentry + glass chemistry + stratigraphy.
- Measuring compacted or reworked thickness as primary.
- Sampling across a unit boundary — mixes two eruption phases.
- Wind can shift between phases, so a single isopach map may mix lobes.
- *Uncertainty note:* the field community's recommended clast-measurement protocol has
  changed over time; check the current IAVCEI guidance before a campaign.

## Verify
- [ ] Each unit described with componentry, sorting, grading and contacts.
- [ ] Fall vs PDC criteria applied and stated.
- [ ] Thickness points distinguish primary from reworked deposits.
- [ ] Volume given as a range with the fitting method named.
- [ ] Samples linked to unit and height, with glass separates for correlation.
