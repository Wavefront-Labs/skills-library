---
id: engineering-technology.biomedical-engineering.biomechanics.wall-shear-stress
name: wall-shear-stress
category: engineering-technology
field: biomedical-engineering
product: biomechanics
tags: [wall-shear-stress, cardiovascular-biomechanics, hemodynamics, wss, tawss, osi, poiseuille, cfd-hemodynamics]
level: advanced
status: gated
description: "Compute and interpret wall shear stress in vessels and devices: Poiseuille estimates, CFD outputs TAWSS and OSI, blood viscosity, and thresholds for low and high WSS."
sources: ["Malek et al., Hemodynamic shear stress and its role in atherosclerosis (JAMA 1999)", "Ku, Blood flow in arteries (Annu Rev Fluid Mech 1997)", "Fung, Biomechanics: Circulation"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Wall shear stress (WSS)

**Goal:** quantify the frictional force blood applies to the vessel wall to judge device and anatomy effects on endothelium and thrombosis.

## Quick estimate
For steady Newtonian Poiseuille flow in a rigid tube: tau = 4 mu Q / (pi R^3), where mu is viscosity, Q flow rate and R radius.
Example: mu = 3.5 mPa s, Q = 5 mL/s = 5e-6 m3/s, R = 3 mm gives tau = 4 x 3.5e-3 x 5e-6 / (pi x (3e-3)^3) = 0.83 Pa (computed; an earlier figure of 2.5 Pa was wrong).

## Typical ranges (literature, approximate)
- Arterial-level shear above about 15 dyn/cm2 (1.5 Pa) is described as atheroprotective and low shear below 4 dyn/cm2 (0.4 Pa) as atherogenic, prevalent at atherosclerosis-prone sites (Malek et al. 1999 abstract, Europe PMC 10591386); very high WSS (above roughly 10 Pa, and far higher in stenoses and devices) can activate platelets and damage cells. Veins are lower (0.1-0.6 Pa (gated: unconfirmed, source is paywalled or blocked)).
- Thresholds are context dependent; treat them as flags for further analysis, not limits.

## CFD workflow
1. Image-derived geometry; inlet flow waveform from phase-contrast MRI or Doppler; outlet Windkessel boundaries (see windkessel-models).
2. Blood is shear-thinning; use Newtonian with about 3.5 mPa s in large arteries or Carreau/Casson models in small vessels and low shear.
3. Mesh with boundary-layer inflation (several layers; check y+ equivalent and wall-gradient convergence).
4. Run enough cardiac cycles to remove start-up effects (2-3).
5. Report **TAWSS** (time-averaged), **OSI** (oscillatory shear index, 0 to 0.5) and relative residence time, plotted on the wall.

## Gotchas
- Rigid-wall assumption raises WSS slightly; FSI is the check.
- WSS is a gradient, so mesh-sensitive; do a grid convergence study.
- Image segmentation smoothing changes WSS noticeably.

## Verify
- [ ] Mesh independence on mean and peak WSS.
- [ ] Mass conservation across outlets.
- [ ] Compare with the Poiseuille estimate in a straight segment.
