---
id: engineering-technology.biomedical-engineering.biomaterials.nitinol-fatigue
name: nitinol-fatigue
category: engineering-technology
field: biomedical-engineering
product: biomaterials
tags: [nitinol-fatigue, nitinol, shape-memory-alloy, superelastic, strain-life, fatigue-design, stent-fatigue, constant-life-diagram]
level: advanced
status: verified
description: "Design nitinol devices against fatigue with strain-based criteria: mean and alternating strain, constant-life diagrams, pre-strain, surface condition and superelastic FEA."
sources: ["Pelton et al., Fatigue and durability of Nitinol stents (J Mech Behav Biomed Mater 2008)", "ASTM F2477 Standard test methods for in vitro pulsatile durability testing of vascular stents (confirm edition)", "FDA guidance on non-clinical engineering tests for intravascular stents (current text on fda.gov)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Nitinol fatigue design

**Goal:** predict and demonstrate fatigue life of superelastic nitinol components under cyclic physiological loads.

Safety-critical implant work; requirements come from FDA guidance, ISO 25539-2 (vascular stents) and applicable standards (confirm editions). This is a technical summary.

## Why strain, not stress
Superelastic nitinol has a stress plateau during the austenite-martensite transformation, so stress changes little with strain; fatigue correlates with **strain amplitude** and **mean strain**, not stress.

## Method
1. **FEA** with a superelastic material model (transformation plateau, hysteresis, asymmetry) through the full life: crimp, deployment, anatomical load (for example radial pulsatile, bending, axial, torsion).
2. For each node, extract **mean strain** and **alternating strain** (half the range) over a loading cycle.
3. Plot on a **constant-life (strain-based Goodman-like) diagram** with a fatigue endurance line (10^7 or 4 x 10^8 cycles) obtained from tests on representative material and surface finish. Published endurance limits in strain amplitude are commonly quoted at about 0.4% for pulsatile conditions (gated: unconfirmed, not found in the Pelton et al. 2008 abstract; confirm in the paper) at typical mean strains, varying with processing; use your own data.
4. **Pre-strain** from crimp and deployment shifts the mean strain; the sequence matters.
5. Derive a fatigue safety factor (distance to the line) and demonstrate with bench tests at accelerated frequency and in the relevant environment (37 C saline or water).

## Material and process drivers
- Inclusions (TiC, Ti2NiO) initiate cracks; low-inclusion melts (VAR) improve life.
- Surface: electropolishing removes the heat-treat oxide and notches; sharp strut corners shorten life.
- Austenite finish temperature and heat treatment set the plateau stress and the transformation (see austenite-finish-temperature).

## Verify
- [ ] FEA convergence and material model calibrated to tensile tests of the actual material.
- [ ] Fatigue test to at least the target cycles (ASTM F2477 describes 10 years of equivalent use at 72 beats per minute, at least about 380 million cycles) with runout rationale.
- [ ] Fractography on any failures.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
