---
id: engineering-technology.biomedical-engineering.medical-imaging-systems.astm-f2119-image-artifact
name: astm-f2119-image-artifact
category: engineering-technology
field: biomedical-engineering
product: medical-imaging-systems
tags: [astm-f2119, mr-image-artifact, implant-artifact, passive-implant-artifact, mri-artifact-test]
level: advanced
status: gated
description: "Measure MR image artefacts from passive implants per ASTM F2119: phantom setup, spin-echo and gradient-echo sequences, artefact area definition and reporting."
sources: ["ASTM F2119 Standard Test Method for Evaluation of MR Image Artifacts from Passive Implants (confirm current edition)", "ASTM F2503 Standard Practice for Marking Medical Devices and Other Items for Safety in the Magnetic Resonance Environment", "FDA, Testing and Labeling Medical Devices for Safety in the Magnetic Resonance (MR) Environment, https://www.fda.gov/media/74201/download"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# ASTM F2119 image artefact testing

**Goal:** report the size of the signal void and distortion an implant causes so clinicians understand image quality near it. It is separate from the safety tests (see astm-f2052-magnetic-force and astm-f2182-rf-heating).

## Method (summary; use the standard)
1. Place the implant in a phantom of homogeneous solution (typically doped water or gel) in a defined position and orientation relative to the main field.
2. Image with defined sequences: spin echo and gradient echo, with stated TR, TE, bandwidth, slice thickness and field of view, in at least two orientations to the field.
3. Measure the artefact as the region where signal intensity deviates from the background by more than a stated threshold (the standard defines it; commonly described as 30 percent (gated: unconfirmed, source is paywalled or blocked)). Report the maximum extent from the implant edge and the artefact area.
4. Compare to the same phantom without the implant for baseline.
5. State the scanner field strength (1.5 T and 3 T both common) and coil.

## Practice
- (Textbook MR physics (gated: unconfirmed, source is paywalled or blocked)) Artefact grows with susceptibility difference (stainless steel and cobalt chrome worse than titanium or nitinol), field strength and gradient echo sequences.
- Material choice and geometry (design for lower susceptibility) reduce artefact; this is a design consideration for implants near anatomy of interest (spine, brain).
- Report in labelling as the maker's tests; clinical sequences may differ.

## Verify
- [ ] Artefact threshold and measurement method per the standard.
- [ ] Sequence parameters and field strength reported.
- [ ] Orientation relative to B0 documented.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
