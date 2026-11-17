---
id: engineering-technology.biomedical-engineering.biomechanics.anatomical-coordinate-systems
name: anatomical-coordinate-systems
category: engineering-technology
field: biomedical-engineering
product: biomechanics
tags: [anatomical-coordinate-systems, joint-kinematics, rigid-body-kinematics, isb, joint-coordinate-system, grood-suntay, anatomical-landmarks]
level: practitioner
status: draft
description: "Define segment and joint coordinate systems the ISB way: landmarks, axis conventions, Grood-Suntay joint axes and the checks that stop sign and axis-order mistakes."
sources: ["Wu et al., ISB recommendation on definitions of joint coordinate system - Part I ankle hip and spine (J Biomech 2002)", "Wu et al., ISB recommendation Part II shoulder elbow wrist and hand (J Biomech 2005)", "Grood and Suntay, A joint coordinate system for the clinical description of three-dimensional motions (J Biomech Eng 1983)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Anatomical coordinate systems and ISB recommendations

**Goal:** express segment poses and joint angles in a reproducible, comparable convention.

## Conventions (ISB lower limb)
- Global and segment axes: X anterior, Y superior (up), Z to the right. Joint rotations use the **joint coordinate system (JCS)** of Grood and Suntay: two body-fixed axes (one on each segment) and a floating axis perpendicular to both, giving flexion-extension, ab/adduction and internal-external rotation without gimbal ambiguity in clinical reporting.
- Pelvis frame from ASIS and PSIS landmarks, femur from hip joint centre and epicondyles, tibia from knee centre and malleoli, foot from calcaneus and metatarsal heads. The exact landmarks differ by joint; take them from the ISB papers rather than memory.

## Procedure
1. Palpate and mark landmarks (or use a calibrated pointer) in a static trial; use anatomical landmarks, not just technical cluster markers.
2. Estimate the hip joint centre by regression (for example from pelvic dimensions) or functional method (circumduction); document which.
3. Build each segment's right-handed frame; check orthonormality and handedness.
4. Compute joint angles via the JCS; state the rotation sequence (flexion first for hip and knee).
5. Report ranges relative to a defined neutral/standing posture.

## Gotchas
- Different labs mix Cardan sequences; angles then cannot be compared (see joint-angle-conventions).
- Left-side axes must be mirrored consistently so internal rotation has the same sign on both sides.
- Palpation error of landmarks (often 5-10 mm) is a larger error than most software choices.

## Verify
- [ ] Frames orthonormal and right-handed.
- [ ] Static standing trial gives angles near neutral.
- [ ] Left and right of a symmetric test subject give mirror-consistent signs.
