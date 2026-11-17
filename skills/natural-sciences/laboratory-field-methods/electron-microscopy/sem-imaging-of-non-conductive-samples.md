---
id: natural-sciences.laboratory-field-methods.electron-microscopy.sem-imaging-of-non-conductive-samples
name: sem-imaging-of-non-conductive-samples
category: natural-sciences
field: laboratory-field-methods
product: electron-microscopy
tags: [electron-microscopy, sem, scanning-electron-microscope, charging, non-conductive, sputter-coating, gold-palladium, carbon-coating, low-vacuum, variable-pressure, esem, low-kv, accelerating-voltage, beam-current, working-distance, secondary-electrons, backscattered-electrons, bse, eds, edx, energy-dispersive-spectroscopy, carbon-tape, critical-point-drying, biological-sem, sample-preparation, astigmatism]
level: practitioner
status: draft
description: "Image insulating samples in an SEM without charging: mounting, sputter vs carbon coating, low-kV and low-vacuum modes, SE vs BSE detectors, and coating choices that won't spoil EDS analysis."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SEM imaging of non-conductive samples

**Goal:** sharp, artefact-free SEM images of insulating materials (polymers, ceramics,
biological tissue, minerals, paper) without the bright streaks, drift and distortion of
charging — and, where needed, a valid EDS composition.

## 1. Recognise charging
Electrons that land on an insulator have nowhere to go. Symptoms: abnormally bright
or dark patches, horizontal streaks or "tearing" during scan, image drift or jumping,
and, in extreme cases, a distorted mirror image of the chamber. Charging gets worse
with higher beam current, slower scans and higher magnification.

## 2. Mount to give charge a path
- Double-sided **carbon tape** or carbon/silver paint onto an aluminium stub.
- Run a stripe of conductive paint or copper tape **from the sample's top surface down to
  the stub** — coating alone fails if the coated top is isolated from ground.
- Powders: sprinkle lightly on carbon tape, tap off loose material (loose particles
  charge and contaminate the column); blow gently with dry gas away from the instrument.
- Samples must be dry and outgassed. Wet or oily samples ruin the vacuum; biological
  samples need fixation, dehydration and **critical-point drying** (or freeze-drying) to
  avoid collapse by surface tension.

## 3. Coating choices
| Coating | Thickness (typ.) | Good for | Avoid when |
|---|---|---|---|
| Au or Au/Pd sputter | ~5–15 nm | High-SE-yield topography imaging | EDS of light elements; very high-res (grain visible at high mag) |
| Pt or Ir sputter | ~2–5 nm | Finer grain for high-magnification FEG-SEM | Budget/EDS overlaps |
| **Carbon** evaporation | ~10–20 nm | EDS/WDS, EBSD prep, BSE imaging | Pure topography imaging (lower SE yield) |
Thinner is better as long as charging stops: thick coatings hide fine features.
Coat with the sample rotating/tilting if it has deep relief. Carbon peaks interfere least
with most EDS work, but you can't then quantify carbon in the sample itself.

## 4. Uncoated alternatives
- **Low accelerating voltage** (~0.5–2 kV): at some energy (the "E2" crossover, material
  dependent) emitted electrons balance incoming ones and charging vanishes. Modern
  field-emission SEMs image well at low kV; also improves surface detail.
- **Low-vacuum / variable-pressure (VP) / ESEM mode:** gas in the chamber (e.g. ~10–100 Pa)
  is ionised and neutralises surface charge. Uses a gaseous SE or BSE detector; some loss
  of resolution from beam scattering in the gas ("skirt"). Ideal for samples you must not coat.
- Lower beam current (smaller spot size), faster scan with frame integration or line
  averaging, and smaller tilt changes all reduce charging.

## 5. Detectors and imaging settings
- **SE (secondary electrons, Everhart–Thornley/in-lens):** topography, surface detail.
- **BSE (backscattered):** contrast scales with average atomic number — composition
  contrast; less sensitive to charging.
- Shorter **working distance** improves resolution; longer gives depth of field and EDS
  geometry (use the instrument's specified analytical WD for EDS).
- Correct focus and **astigmatism** at higher magnification than you will image, then zoom out.

## 6. EDS on insulators
- Accelerating voltage must be ~1.5–2× the energy of the highest X-ray line you need
  (e.g. ≥ 15 kV for Fe Kα at 6.4 keV) — this conflicts with low-kV anti-charging; carbon
  coat or use VP mode instead.
- Charging lowers the effective landing energy and distorts quantification.
- Flat, polished samples for quantitative EDS; rough surfaces give qualitative results only.

## Gotchas
- Beam damage: polymers and biological samples blister or shrink under high dose. Find
  focus on an adjacent area, then move and capture.
- Gold coating can create nanoscale "island" artefacts mistaken for sample texture.
- Don't touch stubs with bare fingers; skin oils outgas and contaminate.

Uncertain here: coating thicknesses and VP pressure ranges are typical figures; instrument
manuals give the supported ranges.

## Verify
- [ ] Sample grounded from its top surface to the stub.
- [ ] No streaks or drift at the working magnification and scan speed.
- [ ] Coating type compatible with the planned analysis (EDS → carbon or VP).
- [ ] kV adequate for the X-ray lines you report.
- [ ] Imaging conditions (kV, current, WD, detector, coating) recorded with each image.
