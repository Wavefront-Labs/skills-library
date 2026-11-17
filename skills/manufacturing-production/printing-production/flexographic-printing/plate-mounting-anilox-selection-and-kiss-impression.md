---
id: manufacturing-production.printing-production.flexographic-printing.plate-mounting-anilox-selection-and-kiss-impression
name: plate-mounting-anilox-selection-and-kiss-impression
category: manufacturing-production
field: printing-production
product: flexographic-printing
tags: [flexographic-printing, flexo, flexography, narrow-web, wide-web, label-press, mark-andy, nilpeter, gallus, bobst, photopolymer-plate, plate-mounting, mounting-tape, sleeve, video-mounter, anilox, anilox-roll, lpi, line-screen, cell-volume, bcm, cm3-m2, doctor-blade, chambered-doctor-blade, kiss-impression, impression-setting, dot-gain, halo, web-tension, register, uv-ink, water-based-ink, packaging-printing]
level: practitioner
status: draft
description: "Set up a flexo press: mount plates square with the right tape, choose anilox line screen and volume for the work, set kiss impression, and control web tension and register."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Flexo: plate mounting, anilox selection and kiss impression

**Goal:** print clean, sharp flexo with minimal dot gain by getting the three setup
variables right — how the plate is mounted, how much ink the anilox delivers, and how
lightly the plate touches the substrate.

## 1. Plate mounting
- Use a **video/camera mounter** (or pin register system) to align plates to the
  cylinder or sleeve centre line and to each other via mounting marks (microdots or
  crosshairs). Square to within the job's register tolerance — misalignment here
  cannot be fully corrected on press.
- **Mounting tape** compressibility matters: **soft/compressible** tapes for solids
  (better lay-down), **firm** tapes for fine highlights and process (less dot gain).
  Combination plates (solids + fine screens) are a compromise — medium tape, or split
  onto separate stations if the job allows.
- Avoid trapped air (bubbles telegraph as high spots) and lift on the plate edges
  (seal the leading edge with edge-seal tape for water-based/solvent work).
- Check total height: plate + tape must match the press's cylinder/sleeve design so
  print length (repeat) is correct; wrong total thickness distorts length.

## 2. Anilox selection
Anilox **line screen** (cells per inch/cm) and **volume** (BCM = billion cubic microns
per square inch, or cm³/m²) set ink film:
- **Fine screens / low volume** (e.g. ~800–1200 lpi, ~1.0–2.5 BCM) for process and fine
  text — thinner film, less dot gain.
- **Coarse screens / high volume** (e.g. ~250–500 lpi, ~4–8+ BCM) for solids, whites,
  coatings and varnishes.
- A common rule: anilox line screen at least about **4–6× the plate screen ruling** so
  a single cell doesn't bridge or dip into dots.
These are typical ranges; your ink supplier and plate maker give the job-specific aim.
- **Keep aniloxes clean:** plugged cells reduce volume progressively (colour goes
  weak, you add pigment, ink chemistry drifts). Measure volume periodically (e.g.
  volume-check kits or microscope) and clean per supplier (ultrasonic, soda blast,
  laser — not a wire brush on ceramic).
- Inspect for scoring (lines in print = scored anilox or damaged doctor blade).

## 3. Kiss impression
Flexo is a **light-contact** process. Two settings per station:
1. **Anilox-to-plate:** bring in until the plate inks fully, then no further.
2. **Plate-to-substrate (impression):** bring in until the image just prints
   completely — the "kiss" — then perhaps a fraction more for stability.
Over-impression symptoms: **halo** (ink ring round type and dots), squashed/bloated
dots, dirty print, heavy dot gain, plate wear. Set impression at running speed if
possible; some bounce shows only at speed (gear marks, banding — check cylinder
diameter/gear match and use bearer or sleeve systems correctly).

## 4. Ink and doctor blade
- Chambered doctor blade systems: check blade angle, pressure (light, even),
  end-seal condition (leaks), and blade wear.
- Water-based inks: control **pH** and **viscosity** (efflux cup, temperature-noted)
  — drift changes density and drying. UV inks: check lamp output and cure (tape test).

## 5. Web tension and register
- Tension zones (unwind, infeed, print, outfeed, rewind) must be set for the material:
  films stretch (register drift through stations), paper less so. Too high on thin film
  → neck-in and length change; too low → wander and wrinkles.
- Bring register in with the auto-register system after tension is stable; changing
  tension later moves register again.

## Gotchas
- Fixing weak colour by pushing impression instead of checking anilox volume.
- Swapping tape types between plates of one job causes colour mismatch between lanes.
- Dried ink in plate shadows ("fill-in") — clean during stops; adjust ink drying speed.

## Verify
- [ ] Plates mounted square on the mounter; correct tape for each plate's content.
- [ ] Anilox screen/volume matched to the work and recently checked for plugging.
- [ ] Impression set to kiss; no halo under a loupe.
- [ ] Ink pH/viscosity (or UV cure) in range.
- [ ] Register held after tension stabilised, across the full run.
