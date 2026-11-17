---
id: engineering-technology.biomedical-engineering.medical-imaging-systems.imaging-phantoms
name: imaging-phantoms
category: engineering-technology
field: biomedical-engineering
product: medical-imaging-systems
tags: [imaging-phantom, qa-phantom, catphan, acr-phantom, routine-qc]
level: practitioner
status: draft
description: "Select and use imaging phantoms for routine QA: uniformity, resolution, contrast and geometric accuracy phantoms, schedules, tolerances and trending."
sources: ["ACR CT and MRI accreditation phantom documentation (confirm current versions)", "AAPM reports on QC for CT and other modalities (confirm)", "https://www.acr.org"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Phantoms and routine QA

**Goal:** a repeatable test that detects performance drift before it affects patients.

## Phantom types
- **CT:** water uniformity and noise phantom; multi-module phantoms (such as the Catphan and the ACR accreditation phantom) with CT number linearity, low-contrast detectability, high-contrast resolution, slice thickness and geometric accuracy modules.
- **MRI:** phantoms with uniformity regions, resolution inserts, slice thickness and geometric distortion grids; ACR MRI phantom used for accreditation.
- **Ultrasound:** tissue-mimicking phantoms with wire targets, cysts and attenuation; speed of sound near 1540 m/s.
- **X-ray, fluoroscopy and mammography:** step wedges, resolution test patterns, contrast-detail phantoms.
- **Nuclear medicine:** uniform flood sources, bar and Jaszczak phantoms with hot and cold spheres.

## Practice
1. Use the same phantom, position and protocol each time; mark set-up.
2. Define metrics and **action limits** from the standard or accreditation requirement and your baseline.
3. Daily quick checks (for example CT water number and noise), monthly or annual detailed tests.
4. Trend values on control charts and investigate drift before it exceeds limits.
5. Keep phantoms safe (temperature-sensitive materials, ageing of gels).

## Verify
- [ ] Test schedule and tolerances defined in the QA programme.
- [ ] Baseline values from acceptance testing used.
- [ ] Out-of-tolerance results have a documented response.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
