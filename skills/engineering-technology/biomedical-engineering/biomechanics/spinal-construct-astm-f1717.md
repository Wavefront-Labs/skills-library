---
id: engineering-technology.biomedical-engineering.biomechanics.spinal-construct-astm-f1717
name: spinal-construct-astm-f1717
category: engineering-technology
field: biomedical-engineering
product: biomechanics
tags: [astm-f1717, vertebrectomy-model, spinal-construct, spinal-fixation, construct-fatigue]
level: advanced
status: gated
description: "Run ASTM F1717 style vertebrectomy-model tests of spinal fixation constructs: block design, loading modes, yield and ultimate definitions, fatigue run-out and reporting."
sources: ["ASTM F1717 Standard Test Methods for Spinal Implant Constructs in a Vertebrectomy Model (scope and significance read at https://www.astm.org/f1717-21.html; confirm current edition)", "https://www.astm.org"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Spinal implant construct testing (F1717)

**Goal:** a repeatable mechanical comparison of spinal fixation constructs using a standard worst-case model.

## Setup
- The construct is mounted on two ultra-high molecular weight polyethylene test blocks representing vertebrae with a gap simulating a vertebrectomy (no anterior support), so the implant carries the whole load.
- **Loading modes:** three static load types and one fatigue test (ASTM scope); the specific modes are static compression bending, tension bending and torsion, with compression bending fatigue (sinusoidal load at a set frequency and R ratio) (gated: unconfirmed, source is paywalled or blocked).
- ASTM notes fatigue is first run dry at ambient conditions, that fluid testing should be considered, and that cyclic frequency should not exceed 5 Hz; results compare designs and do not predict in vivo performance.
- Fixtures allow rotation and translation at the load points so only the construct stiffness resists.

## Outputs
- Stiffness from the linear region of the load-displacement curve; yield load by a defined offset method; ultimate load; for fatigue, cycles to failure at each load, with run-out defined by the standard (commonly cited as 5 million cycles (gated: unconfirmed, source is paywalled or blocked)).
- Plot an S-N type load versus cycles chart with failures and run-outs identified.

## Practice
1. Test worst-case configurations (shortest rod, largest offset); test at least the sample sizes required, and several load levels for fatigue.
2. Record environmental conditions (usually dry at room temperature unless specified) and failure modes (rod fracture, screw bending, set-screw slip).
3. Report all deviations from the standard.
4. Use the same procedure for the predicate when claiming equivalence.

## Verify
- [ ] Block and fixture dimensions comply with the standard drawings.
- [ ] Yield and fatigue definitions reported as in the standard.
- [ ] Failure analysis photographs retained.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
