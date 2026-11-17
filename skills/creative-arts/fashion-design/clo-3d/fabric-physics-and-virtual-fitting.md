---
id: creative-arts.fashion-design.clo-3d.fabric-physics-and-virtual-fitting
name: fabric-physics-and-virtual-fitting
category: creative-arts
field: fashion-design
product: clo-3d
tags: [clo-3d, clo, marvelous-designer, browzwear, vstitcher, 3d-fashion, digital-fashion, virtual-fitting, virtual-sampling, garment-simulation, fabric-physics, fabric-properties, particle-distance, arrangement-points, sewing, avatar, fit-map, strain-map, stress-map, fabric-kit, digital-twin, digital-showroom, lookbook, fashion-design]
level: practitioner
status: draft
description: "Get a trustworthy virtual fit in CLO 3D: arranging and sewing patterns, real fabric physics vs presets, particle distance, reading strain and fit maps, and what virtual fitting can't tell you."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Fabric physics and virtual fitting in CLO 3D

**Goal:** use CLO 3D to replace some physical samples with virtual ones — which only
works if the simulated fabric and avatar behave like the real ones. A pretty render with
default fabric is a sketch, not a fitting.

Menu names below are from recent CLO versions and may move between releases; the
concepts are stable. Marvelous Designer (same vendor, aimed at animation/games) shares
much of the workflow; Browzwear VStitcher is the main competing tool.

## 1. Patterns in, arranged, sewn
1. Import production patterns (DXF-AAMA/ASTM from pattern CAD, or draw in CLO's 2D
   pattern window). Check scale and units on import — a mm/inch mix-up is common.
2. Choose or load the **avatar** matching the brand's fit model measurements (edit
   avatar size by measurement). A generic avatar gives a generic fit.
3. Place pieces on the avatar with **arrangement points** (body-location snaps), so they
   start close to the body without intersecting.
4. **Sew** with segment or free sewing; check sewing direction (crossed lines = twisted
   seams) and that seam lengths match where they should.
5. Simulate (toggle simulation; the spacebar is the default shortcut) and let the garment settle.

## 2. Fabric physics: the part that decides truth
- Each fabric has properties such as stretch (weft/warp/bias), bending, buckling,
  density/weight and thickness. **Presets** ("Cotton_Twill" etc.) are generic.
- For fit decisions, use **measured** fabric: CLO sells a fabric measurement kit and
  works with digitising services that produce physics files from a physical swatch. Many
  mills now supply digital fabric files (often U3MA or the mill's CLO-ready format) — ask.
- Set the **grain direction** on each piece to match the real cut; bias-cut pieces on a
  straight-grain setting simulate completely wrong.
- Set **thickness** for display and collision; set **layer order** for multi-layer garments
  so the lining and shell don't swap.

## 3. Particle distance (mesh resolution)
Lower particle distance = finer mesh, more accurate drape and wrinkles, slower simulation.
Practical habit: work at a coarse setting (CLO's default is 20 mm) while arranging,
then drop to roughly 5–10 mm for fitting checks and final renders. Very fine values on a
whole garment can make simulation crawl; refine only the pieces that need it.

## 4. Reading the fit
- **Strain map** — how much the fabric is stretched; hot spots mean the garment is too
  small or a seam is short there.
- **Stress / fit map** — how hard the garment presses on the body. Red at bust, hips or
  armholes = tight; check both at rest and in a pose.
- Animate or pose the avatar (sitting, arms raised) — a garment that fits standing can
  bind when seated.
- Compare against the fit model's physical fitting notes the first few times to calibrate
  how much to trust CLO's results for that fabric.

## 5. Beyond fitting
- Colourways and prints: apply textures with correct scale (real-world size) and repeat.
- Renders and turntables for lookbooks and digital showrooms; export glTF/FBX/OBJ for
  e-commerce viewers or game engines.
- Version every change; CLO files (.zprj) grow large — keep them under version naming.

## What virtual fitting can't tell you (yet)
- Hand-feel, comfort, breathability and how a fabric sounds or moves in wind.
- Exact behaviour of unmeasured or very complex fabrics (heavy embellishment, very
  loose knits) — simulation accuracy drops.
- Construction details like interfacing choice and pressing are approximated.
Keep at least one physical sample for any new fabric or block until results are proven.

## Verify
- [ ] Avatar sized to the brand's fit model, not left at default.
- [ ] Fabrics measured or supplier-provided, not generic presets, for fit decisions.
- [ ] Grain direction and layer order set per piece.
- [ ] Fit checked at fine particle distance with strain/fit maps, standing and posed.
- [ ] Results cross-checked against a physical sample for any new fabric.
