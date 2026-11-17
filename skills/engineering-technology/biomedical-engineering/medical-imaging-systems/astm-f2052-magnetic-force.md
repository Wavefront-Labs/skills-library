---
id: engineering-technology.biomedical-engineering.medical-imaging-systems.astm-f2052-magnetic-force
name: astm-f2052-magnetic-force
category: engineering-technology
field: biomedical-engineering
product: medical-imaging-systems
tags: [astm-f2052, mri-safety, mr-conditional-testing, magnetic-force, deflection-angle, mr-conditional, astm-f2213, spatial-field-gradient]
level: advanced
status: gated
description: "Measure magnetically induced displacement force on implants in MRI per ASTM F2052: deflection angle method, test location, criteria, torque test link and labelling."
sources: ["ASTM F2052 Standard Test Method for Measurement of Magnetically Induced Displacement Force on Medical Devices in the Magnetic Resonance Environment (confirm current edition)", "ASTM F2213 Standard Test Method for Measurement of Magnetically Induced Torque on Medical Devices in the Magnetic Resonance Environment", "ASTM F2503 Standard Practice for Marking Medical Devices and Other Items for Safety in the Magnetic Resonance Environment", "FDA, Testing and Labeling Medical Devices for Safety in the Magnetic Resonance (MR) Environment, https://www.fda.gov/media/74201/download"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# ASTM F2052 magnetic displacement force test

**Goal:** show that magnetic attraction to an implant in the static field of an MR scanner is small relative to its weight, as part of an MR safety assessment.

The assessment is led by a qualified MR safety expert and an accredited lab; this is the technical outline.

## Principle
The magnetic force depends on the device's magnetisation and the spatial gradient of the field. The test checks that the force is below the device's own weight so that it is not a projectile or a risk of migration.

## Deflection angle method (the usual approach)
1. Hang the device on a light, thin string (or place it on a low-friction platform) at the position in the MR scanner bore (or in an equivalent test magnet) where the **product of field strength and spatial field gradient is greatest**; this location is determined by field mapping of the specific magnet.
2. Measure the angle at which the device deflects from the vertical.
3. A deflection angle **less than 45 degrees** means the magnetic force is smaller than the gravitational force (computed: F = m g tan(theta) and tan 45 = 1; whether the standard sets 45 degrees as its acceptance criterion is (gated: unconfirmed, source is paywalled or blocked)); angles near 90 degrees mean force exceeds many times the weight.
4. Test several orientations (and the relevant field strengths, typically 1.5 T and 3 T with the scanner's maximum spatial gradient (gated: unconfirmed, source is paywalled or blocked)).
5. Repeat with attention to the string length, size and placement; use a protractor or camera and record the field mapping data.

## Other tests in the set (standard titles confirmed in FDA, Testing and Labeling Medical Devices for Safety in the MR Environment, reissued 10 Oct 2023)
- **Magnetically induced torque** (ASTM F2213): torque on the device in the field, measured with a torsion apparatus or by qualitative comparison to gravity.
- **RF heating** (see astm-f2182-rf-heating).
- **Image artefact** (ASTM F2119; see astm-f2119-image-artifact).
- **Labelling** (ASTM F2503): MR Safe, MR Conditional, or MR Unsafe, with conditions on field strength, gradient and SAR.

## Gotchas
- Non-ferromagnetic devices can still be MR Conditional; the tests decide on force, torque, heating and artefact together.
- Test in the position of maximum gradient, not at the centre of the bore.
- Device mass matters, since the criterion compares force to weight.

## Verify
- [ ] Field mapping documents the location of maximum product of B and its gradient.
- [ ] Deflection angle measured for all orientations and reported.
- [ ] MR safety report supports the label wording.
