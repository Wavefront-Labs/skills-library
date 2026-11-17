---
id: engineering-technology.biomedical-engineering.biomechanics.motion-segment-testing
name: motion-segment-testing
category: engineering-technology
field: biomedical-engineering
product: biomechanics
tags: [motion-segment, spine-biomechanics, spinal-loads, functional-spine-unit, pure-moment, range-of-motion, neutral-zone, cadaver-testing]
level: advanced
status: draft
description: "Test spinal motion segments with pure moments: specimen prep, fixtures, pre-load, moment limits, range of motion and neutral zone outputs, and test-standard links."
sources: ["Panjabi, Biomechanical evaluation of spinal fixation devices (Spine 1988 and related papers)", "Wilke, Wenger and Claes, Testing criteria for spinal implants: recommendations for the standardization of in vitro stability testing of spinal implants (Eur Spine J 1998)", "ISO 18192-1 Implants for surgery - Wear of total intervertebral spinal disc prostheses (check edition)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Spinal motion segment testing

**Goal:** measure the three-dimensional stiffness and range of motion of a functional spinal unit, intact and after instrumentation.

Cadaver and clinical work need ethics approval and tissue-handling procedures; this is bench-engineering guidance.

## Method
1. **Specimens:** fresh-frozen human or animal spines, screened for fractures and tumours by imaging; record age, sex and bone density. Thaw slowly, keep moist with saline.
2. **Potting:** embed the end vertebrae in PMMA or low-melting alloy in fixtures aligned to the disc mid-plane; protect facet joints.
3. **Loading:** apply **pure moments** in flexion-extension, lateral bending and axial rotation using a spine tester or a cable-and-pulley rig. Moments up to about 7.5 Nm are common for lumbar segments (some protocols use 10 Nm); an optional compressive follower preload (a few hundred newtons) simulates muscle load.
4. **Preconditioning:** 2-3 cycles before the recorded cycle; record the third.
5. **Measurement:** optical markers or rotary sensors on each vertebra give angular displacement. Report range of motion at peak moment and neutral zone (displacement at low moment).
6. **Conditions:** intact, injured/destabilised, instrumented; use repeated measures on the same specimen.
7. **Analysis:** non-parametric stats on small samples and normalise to the intact condition to remove inter-specimen variability.

## Gotchas
- Dehydration alters disc stiffness within hours; spray with saline and limit test time.
- Constraints at the fixtures create shear and artefact unless the rig is free to translate.

## Verify
- [ ] Load cell and angular sensors calibrated.
- [ ] Hysteresis loops repeatable between cycles.
- [ ] Intact range of motion consistent with published ranges for the level.
