---
id: engineering-technology.biomedical-engineering.biomechanics.marker-set-conventions
name: marker-set-conventions
category: engineering-technology
field: biomedical-engineering
product: biomechanics
tags: [marker-set, plug-in-gait, helen-hayes, cast-protocol, marker-placement]
level: practitioner
status: draft
description: "Choose and apply a gait marker set (Helen Hayes, Plug-in Gait, CAST, cluster-based) with consistent anatomical landmarks, calibration and joint-centre estimation."
sources: ["Kadaba et al., Measurement of lower extremity kinematics during level walking (J Orthop Res, 1990)", "Davis et al., A gait analysis data collection and reduction technique (Human Movement Science, 1991)", "Cappozzo et al., Position and orientation in space of bones during movement (Clin Biomech, 1995)", "https://www.isbweb.org"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Marker set conventions

**Goal:** a marker set that gives repeatable segment frames and joint centres matched to your question and software.

## Common sets
- **Helen Hayes and Plug-in Gait (Davis) style:** pelvis markers (ASIS and sacrum or PSIS), thigh and shank wand markers, knee lateral epicondyle, ankle malleolus, foot heel and toe. Fast to apply; thigh wand and knee alignment sensitivity cause cross-talk and error.
- **CAST (calibrated anatomical system technique):** technical marker clusters track segments; anatomical landmarks (palpated or via pointer) define the anatomical frame at a calibration pose. More accurate when clusters are well placed.
- **Cleveland Clinic and IOR gait sets:** variants with clusters and extra landmarks, documented in the literature for specific protocols.

## Practice
1. Document landmark definitions (palpation instructions) and train the operators; most variability comes from palpation.
2. Hip joint centre from regression equations on pelvis landmarks or a functional circle-fit method; choose and report.
3. Static calibration trial, then optionally remove anatomical markers for dynamic trials.
4. Apply a consistent segment coordinate convention (see anatomical-coordinate-systems and joint-angle-conventions).
5. Check marker visibility, labelling, gap filling and filtering (see butterworth-data-filtering).

## Verify
- [ ] Marker protocol, landmark definitions and software model version recorded.
- [ ] Repeat-session variability estimated for the main outcomes.
- [ ] Results compared with comparable-set reference data only.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
