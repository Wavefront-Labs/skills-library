---
id: engineering-technology.biomedical-engineering.biomechanics.soft-tissue-artefact
name: soft-tissue-artefact
category: engineering-technology
field: biomedical-engineering
product: biomechanics
tags: [soft-tissue-artefact, skin-marker-error, marker-motion, kinematic-error, motion-capture]
level: advanced
status: draft
description: "Recognise and reduce skin-marker soft tissue artefact in motion capture: where it is largest, cluster placement, and correction by rigid-body fitting or multibody optimisation."
sources: ["Leardini et al., Human movement analysis using stereophotogrammetry Part 3: soft tissue artifact assessment and compensation (Gait and Posture, 2005)", "Cappozo et al. and Lu and O'Connor on global optimisation (journal literature; confirm citations)", "https://www.isbweb.org"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Skin marker soft tissue artefact

**Goal:** know how far skin markers move relative to bone and limit its effect on joint kinematics and kinetics.

## Facts
- Markers on skin move relative to the underlying bone due to muscle contraction, skin sliding and inertial wobble. It is the largest error source in marker-based gait analysis, bigger than camera error, and cannot be removed by filtering because its frequency overlaps real motion.
- It is largest at the thigh (and at the knee for rotations about the long axis), shank, and in fast or impact tasks; smallest at bony-prominence markers (pelvis ASIS, malleoli) though not zero.
- Effects on joint angles can be several degrees; out-of-plane rotations (adduction-abduction, internal-external) suffer most, since these are small signals.

## Reduction
1. Use marker clusters (three or four markers on a rigid plate or shell) on thigh and shank rather than single wand markers; place them on the least-muscle area.
2. Avoid placement over muscle bellies and near joints with skin sliding.
3. Use a rigid-body least-squares fit (singular value decomposition) to estimate segment pose from many markers, which averages noise and some artefact.
4. Use a global (multibody) optimisation with joint constraints (for example a model with a spherical hip and hinge knee) to reduce inconsistent segment motion; constraints can hide real joint translation, so state the model assumption.
5. Report uncertainty: sensitivity to marker placement, repeat placement by two operators.

## Verify
- [ ] Marker placement protocol documented and repeatable.
- [ ] Out-of-plane results flagged as lower confidence.
- [ ] Kinetic outputs checked for sensitivity to the kinematic error.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
