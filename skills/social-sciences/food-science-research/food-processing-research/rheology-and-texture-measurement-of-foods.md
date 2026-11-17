---
id: social-sciences.food-science-research.food-processing-research.rheology-and-texture-measurement-of-foods
name: rheology-and-texture-measurement-of-foods
category: social-sciences
field: food-science-research
product: food-processing-research
tags: [food-processing-research, food-engineering, rheology, rheometer, texture-analyser, texture-analyzer, tpa, texture-profile-analysis, ta-xt, viscosity, flow-curve, shear-thinning, power-law, herschel-bulkley, yield-stress, oscillatory-rheology, saos, amplitude-sweep, frequency-sweep, storage-modulus, loss-modulus, g-prime, linear-viscoelastic-region, wall-slip, process-structure-property, high-pressure-processing, gels, emulsions]
level: practitioner
status: draft
description: "Measure food rheology and texture for processing research: rotational flow curves, oscillatory sweeps (G', G'', LVR), TPA on a texture analyser, geometry choice, wall slip and reporting."
sources:
  - "Steffe, Rheological Methods in Food Process Engineering (2nd ed., free PDF from the author)"
  - "Bourne, Food Texture and Viscosity: Concept and Measurement (2nd ed.)"
  - "Peleg (2019), The instrumental texture profile analysis revisited, J. Texture Studies"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Rheology and texture measurement of foods

**Goal:** quantify how a process (heating, high-pressure processing, homogenisation,
extrusion, an ingredient swap) changes a food's flow and mechanical behaviour, with
measurements that are reproducible and physically meaningful.

## 1. Pick the right measurement
| Question | Instrument / test |
|---|---|
| How thick is it, how does it flow when pumped/poured? | Rotational rheometer, **flow curve** |
| Gel/network strength without breaking it | Rheometer, **small-amplitude oscillatory shear (SAOS)** |
| How firm, springy, cohesive is a solid food? | Texture analyser, **TPA** or puncture/compression |
| Gelation or melting with temperature | Oscillatory **temperature ramp** |

## 2. Rotational flow curves
- Geometry: cone-plate (homogeneous fluids, small gap), parallel plate (particulates,
  gap ≥ ~10× largest particle), concentric cylinder/cup-and-bob (low viscosity, beverages),
  vane (pastes with yield stress, avoids slip).
- Pre-shear then rest (e.g. 1–5 min) to give a reproducible starting structure; control
  temperature (Peltier) and use a solvent trap to stop drying.
- Run up and down shear-rate ramps (e.g. 0.1–100 s⁻¹ or across process-relevant
  rates); a gap between them = **thixotropy**.
- Fit models: Newtonian, power law (σ = Kγ̇ⁿ; n < 1 shear-thinning), Herschel–Bulkley
  for yield-stress materials. Report fit range and R², and apparent viscosity at a stated
  shear rate (e.g. 50 s⁻¹, often used for "mouth" comparisons — a convention, not a law).

## 3. Oscillatory tests
1. **Amplitude (strain) sweep** at fixed frequency (e.g. 1 Hz) to find the **linear
   viscoelastic region (LVR)** — where G′ and G″ are flat.
2. **Frequency sweep** within the LVR (e.g. 0.1–10 Hz): G′ > G″ and both nearly flat →
   strong gel; crossover/frequency dependence → weak gel or entangled solution.
3. Temperature or time sweeps for gelation/setting, within the LVR.
Report G′, G″ and tan δ (G″/G′) at a stated frequency and strain.

## 4. Texture analysis (TA.XT and similar)
- **TPA**: two compression cycles (commonly 50–75% strain for soft gels, lower for
  brittle foods), giving hardness, cohesiveness, springiness, adhesiveness, chewiness
  (for solids) / gumminess (semisolids).
- Standardise **sample geometry** (cork borer cylinders, e.g. height = diameter),
  temperature, probe diameter (larger than the sample for true uniaxial compression),
  speed and strain; all of these change the numbers.
- Peleg (2019) cautions that several TPA parameters depend strongly on test settings and
  are not intrinsic properties; compare only within an identical protocol and consider
  reporting fundamental stress–strain data (true stress, Hencky strain, fracture point).

## 5. Linking to process and structure
Pair rheology with microstructure (confocal, SEM), particle size (laser diffraction) and
composition to build process → structure → property arguments, and with sensory
descriptors where texture perception is the outcome.

## Gotchas
- **Wall slip** in emulsions, gels and pastes gives artificially low viscosity —
  use roughened/serrated plates or a vane, and check by changing gap (slip makes results
  gap-dependent).
- Sample loading damages structure: trim consistently, wait to equilibrate, or form
  gels *in situ* on the plate.
- Inertia artefacts at high frequency for low-viscosity samples; check the instrument's
  raw phase angle/torque limits.
- Uncertain: specific strain/speed values above are common starting points; adjust and
  report for your matrix.

## Verify
- [ ] Geometry justified for the material; temperature controlled; solvent trap used.
- [ ] Oscillatory tests run inside the measured LVR.
- [ ] Slip checked (two gaps or roughened geometry).
- [ ] TPA settings (strain, speed, probe, sample size) fully reported.
- [ ] ≥ 3 independent samples per treatment, with variability shown.
