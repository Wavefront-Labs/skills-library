---
id: engineering-technology.biomedical-engineering.medical-device-design.implant-sizing-anthropometry
name: implant-sizing-anthropometry
category: engineering-technology
field: biomedical-engineering
product: medical-device-design
tags: [implant-sizing, implant-design, implantable-devices, anthropometry, size-range, statistical-shape-model]
level: advanced
status: draft
description: "Size an implant range from anthropometric data: pick landmarks, dimension percentiles, step sizes and overlap, and check fit across populations before design freeze."
sources: ["Pheasant and Haslegrave, Bodyspace: Anthropometry Ergonomics and the Design of Work", "Nordin and Frankel, Basic Biomechanics of the Musculoskeletal System", "ISO 14630 Non-active surgical implants - General requirements", "https://www.iso.org"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Implant sizing and anthropometric data

**Goal:** a size range that fits the intended population with the fewest sizes, using real morphology data rather than a single average anatomy.

Practice guidance; clinical input from surgeons and regulatory rules on intended population remain with qualified staff.

## Procedure
1. **Define the dimension that matters** (for example femoral AP and ML width, tibial plateau width, pedicle diameter, canal width). Pick measurable landmarks that a surgeon can reproduce.
2. **Collect distribution data** from CT/MRI segmentation or published datasets for the intended population (sex, age, ethnicity, paediatric versus adult). Do not assume one population generalises; document the source and sample size.
3. **Choose the coverage target** (for example fit 5th to 95th percentile) and plot the cumulative distribution of the key dimension.
4. **Set size steps.** Step size is a trade-off between fit (undersizing or overhang), inventory cost and surgeon complexity. Common practice is a few millimetres per step in the key dimension, with overlap so that adjacent sizes are both acceptable for borderline anatomy.
5. **Check coupled dimensions.** Anatomy does not scale isotropically: ML-to-AP ratio varies by sex and ethnicity, so a single scaling may cause overhang. Consider narrow variants or dual-width options.
6. **Statistical shape models** can virtually fit the implant across a population sample and report overhang, coverage and gap per size.
7. **Document** coverage, assumptions and residual unfit fraction, and feed into risk file and labelling (indications).

## Gotchas
- Cadaver or one-country datasets bias results; bone shrinks in cadaver prep.
- Cartilage and soft tissue thickness matter for articular implants.
- Revision and deformity cases fall outside the primary range; state that scope.

## Verify
- [ ] Data source, sample size and population stated.
- [ ] Fit simulated across a sample, not a single anatomy.
- [ ] Size steps and overlap justified in the design file.
