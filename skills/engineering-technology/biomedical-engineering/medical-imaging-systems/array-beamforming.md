---
id: engineering-technology.biomedical-engineering.medical-imaging-systems.array-beamforming
name: array-beamforming
category: engineering-technology
field: biomedical-engineering
product: medical-imaging-systems
tags: [beamforming, delay-and-sum, ultrasound-array, grating-lobes, apodization]
level: advanced
status: gated
description: "Understand ultrasound array beamforming: delay-and-sum focusing, pitch and grating lobes, apodization, dynamic receive focusing, f-number and resolution, plane-wave methods."
sources: ["Szabo, Diagnostic Ultrasound Imaging: Inside Out", "Shung, Diagnostic Ultrasound: Imaging and Blood Flow Measurements", "https://www.ieee-uffc.org"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Array beamforming

**Goal:** form and steer focused beams with arrays, and understand the limits of lateral resolution and artefacts.

## Concepts
- **Delay-and-sum:** each element's signal is delayed so echoes from a chosen focal point add coherently; transmit focusing applies delays to the transmitted pulses; **dynamic receive focusing** updates delays with depth.
- **Element pitch:** for steering, the pitch should be about half a wavelength or less to avoid **grating lobes** (computed: first lobe at sin(theta) = lambda/d + sin(theta0); d = 0.5 lambda gives none at any steering angle, d = 0.6 lambda is clean up to 30 degrees steering, d = lambda gives a lobe at 90 degrees unsteered and at 30 degrees when steered to 30; the limit is d < lambda/(1+sin theta0)); larger pitch is acceptable for non-steered linear arrays but grating lobes still limit contrast.
- **Apodization (weighting):** tapering element weights (for example Hann) lowers side lobes at the cost of a wider main lobe and loss of sensitivity.
- **Resolution** (textbook rules (gated: unconfirmed, source is paywalled or blocked)): lateral resolution is about wavelength times the f-number (focal depth divided by aperture); axial resolution is about half the pulse length.
- **Plane-wave and synthetic aperture methods:** transmit unfocused waves or single elements, then reconstruct by software beamforming and coherent compounding; gives high frame rate for flow and elastography; signal-to-noise and compounding trade-offs.
- **Adaptive beamformers** (minimum variance, coherence-based weights) improve resolution and contrast at computational cost.

## Verify
- [ ] Beam plots (hydrophone or simulation) for transmit focus and steering angles.
- [ ] Grating lobe level versus pitch confirmed.
- [ ] Resolution phantom results match predicted f-number resolution.
- [ ] Acoustic output under limits (see acoustic-output-safety).

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
