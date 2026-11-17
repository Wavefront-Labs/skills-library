---
id: engineering-technology.biomedical-engineering.biomechanics.stent-mechanics-testing
name: stent-mechanics-testing
category: engineering-technology
field: biomedical-engineering
product: biomechanics
tags: [stent-mechanics, radial-force, stent-fatigue, stent-testing, crush-resistance]
level: advanced
status: gated
description: "Characterise stent mechanics on the bench: radial force, crush, flexibility and kink, foreshortening, recoil, pulsatile durability and test setup choices."
sources: ["ISO 25539-2 Cardiovascular implants - Endovascular devices - Vascular stents (confirm edition)", "FDA, Non-Clinical Engineering Tests and Recommended Labeling for Intravascular Stents and Associated Delivery Systems, April 2010 (https://www.fda.gov/regulatory-information/search-fda-guidance-documents/non-clinical-engineering-tests-and-recommended-labeling-intravascular-stents-and-associated-delivery)", "https://www.iso.org"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Stent mechanics testing

**Goal:** show a stent maintains vessel patency, deploys predictably and survives millions of cardiac or pulsatile cycles.

## Tests
- **Radial strength and stiffness:** compress or expand the stent circumferentially and record radial force versus diameter (chronic outward force for self-expanding, collapse pressure for balloon-expandable). Specify method (segmented platens, iris or pressure-based).
- **Crush resistance:** flat-plate compression and recovery.
- **Flexibility and kink:** bend to defined radius; three-point bend stiffness; kink radius.
- **Dimensional:** foreshortening, recoil after deployment, expansion uniformity.
- **Fatigue (durability):** pulsatile loading in a vessel mimic at body temperature for the equivalent of ten years of real-time use (FDA 2010 guidance, section B.11); at 72 beats per minute that is about 380 million cycles (72 x 60 x 24 x 365 x 10 = 378 million, computed; the guidance does not state a cycle count), with diameter strains chosen from the intended vessel; combine with bending, axial and torsion for peripheral stents.
- **Corrosion and fracture:** per applicable standards and metals practice (see cyclic-polarization-astm-f2129, ASTM F2129 cyclic potentiodynamic polarization).
- **Delivery system tests:** tensile strength of joints, deployment force, trackability.

## Analysis support
- FEA of stent fatigue (strain amplitude and mean strain on a constant-life diagram) supports but does not replace bench durability testing; see fea-credibility-asme-vv40.

## Verify
- [ ] Test conditions (temperature, medium, vessel mimic compliance) documented.
- [ ] Fatigue run-outs examined for fractures by microscopy.
- [ ] Sample sizes and reliability justified.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
