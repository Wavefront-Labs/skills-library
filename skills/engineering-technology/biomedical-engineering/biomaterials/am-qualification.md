---
id: engineering-technology.biomedical-engineering.biomaterials.am-qualification
name: am-qualification
category: engineering-technology
field: biomedical-engineering
product: biomaterials
tags: [am-qualification, additive-manufacturing-validation, powder-bed-fusion-validation, build-qualification, witness-coupons]
level: advanced
status: verified
description: "Qualify an additive manufacturing process for implants: machine and powder control, parameter freeze, witness coupons, repeatability, process validation and change control."
sources: ["FDA, Technical Considerations for Additive Manufactured Medical Devices (December 2017; confirm current text)", "ASTM F3001 and ASTM F2924 Ti-6Al-4V powder bed fusion specifications (confirm editions)", "ISO 13485 clause 7.5 process validation (confirm edition)", "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/technical-considerations-additive-manufactured-medical-devices"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# AM qualification and guidance

**Goal:** show the AM process makes parts that consistently meet specification, and keep it in control.

## Elements
1. **Design and software:** model checks, support strategy, build orientation and nesting with documented software versions; geometry-driven properties (thin features, overhangs).
2. **Material and powder control:** powder specification (chemistry, particle size distribution, flowability), supplier certification, lot acceptance, storage, reuse policy and blending limits with oxygen and nitrogen monitoring.
3. **Machine qualification:** installation, calibration of laser power and scan alignment, gas flow, build plate levelling and maintenance schedule; periodic performance builds.
4. **Parameter set freeze** after development with design of experiments; changes are controlled.
5. **Process validation (IQ OQ PQ):** build worst-case geometries and positions across the plate and over several builds; test mechanical properties, density, dimensions, microstructure, surface and cleanliness against specifications; show repeatability.
6. **Witness coupons** built with each batch (tensile, fatigue, density) for lot acceptance and monitoring; mapping of properties across the build volume.
7. **In-process monitoring** (melt pool, layer imaging) as additional evidence where used.
8. **Post-processing validation** (see powder-removal-post-processing) and non-destructive testing (micro-CT) for critical parts.
9. **Regulatory:** regulators publish guidance on AM devices (design, manufacturing, testing); patient-matched devices add design controls for the matching process.

## Verify
- [ ] Qualification report covers worst-case geometry and plate positions.
- [ ] Powder lot and reuse records traceable.
- [ ] Machine requalification triggers defined.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
