---
id: engineering-technology.biomedical-engineering.medical-imaging-systems.focal-spot-and-anode-heel
name: focal-spot-and-anode-heel
category: engineering-technology
field: biomedical-engineering
product: medical-imaging-systems
tags: [focal-spot, x-ray-tube, x-ray-generation, line-focus-principle, anode-heel-effect, geometric-unsharpness, blooming]
level: practitioner
status: gated
description: "Understand X-ray focal spot size, line-focus principle, blooming, geometric unsharpness and the anode heel effect, and how to measure and use them in system design."
sources: ["Bushberg et al., The Essential Physics of Medical Imaging (x-ray production chapter)", "IEC 60336:2020 Medical electrical equipment - X-ray tube assemblies for medical diagnosis - Focal spot dimensions and related characteristics (https://webstore.iec.ch/en/publication/62504)", "Curry, Dowdey and Murry, Christensen's Physics of Diagnostic Radiology"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Focal spot and the anode heel effect

**Goal:** choose and verify focal spot size and orientation to balance image sharpness against tube loading.

## Line-focus principle
The electron beam strikes a larger **actual** focal area on an angled anode; the **effective** focal spot seen from the patient is smaller: effective size = actual size x sin(anode angle). Diagnostic anode angles are typically 7-15 degrees. A smaller angle gives a smaller effective spot for the same loading, but the field coverage shrinks and the heel effect is stronger.

## Typical sizes
Nominal focal spot sizes are set by the standard's tolerances (for example small spot around 0.3-0.6 mm for fine detail, large spot around 1.0-1.2 mm for high power in general radiography; mammography 0.1-0.3 mm (gated: unconfirmed, source is paywalled or blocked)). The measured size is allowed to be larger than nominal by tolerance bands in IEC 60336 (edition 5.0, 2020; retitled Focal spot dimensions and related characteristics, with nominal focal spot values from 0.1 to 3.0 per the IEC abstract).

## Geometric unsharpness
Ug = f x OID / (SID - OID), f = effective focal spot size, OID object-image-distance and SID source-image distance. Keep OID small and SID long for sharpness; magnification mammography uses a micro-focal spot.

## Blooming
Focal spot grows with tube current (space-charge) and shrinks slightly with kVp; vendors give blooming curves. Check at the highest current used.

## Anode heel effect
X-ray intensity is lower on the anode side of the beam because photons produced deeper in the target travel a longer path in the anode. The variation can reach tens of percent across the field. Practical use: put the thicker body part toward the cathode side.

## Measurement
- Pinhole camera, slit camera or star-pattern test tools at specified geometry; use the standard's procedure.
- Dose across the field with a dosimeter or flat-field detector image.

## Verify
- [ ] Focal spot measured at stated kV and mA matches tolerance.
- [ ] Anode orientation documented on installation drawings.
- [ ] Unsharpness estimate included in the image-chain budget.
