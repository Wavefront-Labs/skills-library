---
id: natural-sciences.oceanography.biological-oceanography.plankton-net-tows-and-chlorophyll-sampling
name: plankton-net-tows-and-chlorophyll-sampling
category: natural-sciences
field: oceanography
product: biological-oceanography
tags: [biological-oceanography, plankton, zooplankton, phytoplankton, plankton-net, net-tow, vertical-tow, oblique-tow, bongo-net, mesh-size, flowmeter, filtered-volume, formalin, preservation, chlorophyll-a, extracted-chlorophyll, fluorometry, gf-f-filter, acetone-extraction, welschmeyer, fluorescence-calibration, primary-productivity, niskin]
level: practitioner
status: draft
description: "Quantitative plankton sampling: net choice and mesh, vertical/oblique tows with flowmeters, preservation, and extracted chlorophyll-a by filtration and fluorometry to calibrate sensors."
sources: ["Harris et al. (eds.), ICES Zooplankton Methodology Manual (Academic Press)", "IOCCP/JGOFS protocols for chlorophyll a", "Welschmeyer 1994, fluorometric chlorophyll without phaeopigment interference"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Plankton net tows and chlorophyll sampling

**Goal:** abundance numbers you can compare between stations (per m³, per m²) and
chlorophyll values that can calibrate in-situ fluorometers and satellites.

## 1. Choosing the net
- **Mesh** sets what you catch: ~20 µm for microplankton/phytoplankton (qualitative —
  clogs fast), ~200 µm the standard for mesozooplankton (e.g. WP-2), 333–505 µm for larger
  zooplankton and ichthyoplankton (bongo nets). Fine mesh undersamples fast swimmers
  (avoidance); coarse mesh loses small copepods (extrusion).
- Opening–closing nets (MultiNet, MOCNESS) for depth-stratified sampling.
- Keep **open-area ratio** (mesh area / mouth area) high (≳3) to limit clogging.

## 2. Doing the tow
- **Vertical tow:** lower to depth (wire out × cos(wire angle) = depth; avoid angles over
  ~15–20°), haul at ~0.5–1 m/s. Gives abundance per m² (integrated).
- **Oblique tow:** from the vessel underway at ~2 knots, paying out then hauling evenly
  for a depth-integrated sample; use a depth sensor (TDR) on the frame.
- **Flowmeter** in the mouth (off-centre of the bridle) measures filtered volume:
  V = mouth area × revolutions × calibration factor (m/rev). Calibrate flowmeters in a
  no-net tow each cruise. Without a flowmeter, assume 100% filtration only for short,
  slow vertical tows — and say so.
- Wash the net down from the outside with seawater into the cod end; don't spray through
  the mesh from inside.
- Record: station, time (day/night matters — diel vertical migration), depth, wire
  angle, flowmeter start/end, mesh, mouth diameter.

## 3. Preservation
- Zooplankton: buffered **4% formaldehyde** (formalin) in seawater for morphology;
  95% ethanol for DNA (change ethanol after 24 h). Formaldehyde is a carcinogen — fume
  hood or well-ventilated deck, gloves, labelled containers.
- Phytoplankton counts: acid Lugol's solution, dark bottles.
- Split samples (Folsom or Motoda splitter) before counting; count enough individuals
  (e.g. ≥100 of the dominant taxon per subsample) for usable precision.

## 4. Extracted chlorophyll-a
1. From Niskin bottles at chosen depths (surface, chlorophyll maximum identified from the
   CTD fluorometer, below).
2. Filter a known volume (0.25–2 L depending on biomass) onto **GF/F** (~0.7 µm) filters at
   low vacuum (<~200 mmHg) in dim light.
3. Fold, wrap in foil, freeze (−80 °C or liquid nitrogen preferred; −20 °C for short
   storage).
4. Extract in 90% acetone, ~24 h in the dark at −20 °C (or grind for faster extraction).
5. Measure on a fluorometer calibrated with pure chlorophyll-a standard. Acidification
   method (Holm-Hansen) also gives phaeopigments; the Welschmeyer non-acidification
   method avoids chlorophyll-b interference. HPLC gives full pigment composition.
6. Chl (mg/m³) = fluorometer reading × calibration × extract volume / filtered volume.

## 5. Calibrating sensor fluorescence
Regress extracted chlorophyll against CTD fluorescence at the bottle depths. Exclude
surface daytime samples affected by **non-photochemical quenching** (fluorescence drops
in bright light), or correct for it.

## Gotchas
- Comparing day and night tows of migrating zooplankton.
- Clogged nets: a flowmeter showing far fewer revolutions than expected on a second tow.
- Chlorophyll samples left in light or warm before freezing degrade quickly.
- Filtering too much water from blooms: clogged filters, incomplete extraction.

## Verify
- [ ] Filtered volume known for every net sample (flowmeter calibrated).
- [ ] Tow metadata include time of day, depth, mesh and wire angle.
- [ ] Preservative appropriate to the planned analysis (morphology vs DNA).
- [ ] Fluorometer calibrated against a pure standard this season.
- [ ] Sensor-to-extracted regression reported with quenched points handled.
