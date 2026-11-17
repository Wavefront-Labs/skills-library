---
id: engineering-technology.biomedical-engineering.medical-imaging-systems.cone-beam-artifacts
name: cone-beam-artifacts
category: engineering-technology
field: biomedical-engineering
product: medical-imaging-systems
tags: [cone-beam, cone-beam-ct, cone-beam-artifacts, feldkamp, scatter-artifact]
level: advanced
status: draft
description: "Recognise and reduce cone-beam CT artefacts: Feldkamp errors at large cone angle, scatter cupping, truncation, detector lag, motion and the data sufficiency condition."
sources: ["Feldkamp, Davis and Kress, Practical cone-beam algorithm (J Opt Soc Am A, 1984)", "Bushberg et al., The Essential Physics of Medical Imaging (CT chapter)", "https://www.aapm.org"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Cone-beam artefacts

**Goal:** know which artefacts come from cone-beam geometry and how to reduce them.

## Sources
- **Feldkamp (FDK) approximation:** the standard filtered back-projection for circular cone-beam scans is exact only in the central (mid) plane. Errors grow with cone angle: shading and streaks near high-contrast edges away from the mid-plane, and loss of accuracy in CT numbers.
- **Data insufficiency:** the Tuy-Smith condition says exact reconstruction needs every plane through the object to intersect the source trajectory; a single circle fails this, so a missing region exists. Helical or multi-circle trajectories fix it.
- **Scatter:** large irradiated volume with flat-panel detectors gives high scatter-to-primary ratios, which causes cupping, reduced contrast and streaks. Use anti-scatter grids, air gap, collimation, and scatter correction (measured beam-stop, kernel-based or Monte Carlo estimates).
- **Truncation:** field of view smaller than the object leaves lateral truncation artefacts (bright rim); use extrapolation or larger offset-detector scans.
- **Detector lag, ghosting and nonlinearity** from flat panels; corrections and warm-up.
- **Motion, beam hardening and ring artefacts** also occur, with the common CT mitigations (see beam-hardening-artifacts).

## Mitigation
1. Choose a trajectory and cone angle matching the clinical target; keep important detail near the mid-plane when using circular scans.
2. Apply scatter, beam hardening, lag and ring corrections.
3. Use iterative or model-based reconstruction for incomplete data.
4. Verify with phantoms with high-contrast edges and a fine resolution insert.

## Verify
- [ ] Phantom scan shows acceptable shading and uniformity over the volume.
- [ ] Artefact severity versus cone angle documented.
- [ ] Corrections validated and their parameters under change control.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
