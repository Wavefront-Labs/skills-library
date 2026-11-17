---
id: engineering-technology.aerospace-engineering.spacecraft-systems-design.cubesat-design-specification-compliance
name: cubesat-design-specification-compliance
category: engineering-technology
field: aerospace-engineering
product: spacecraft-systems-design
tags: [spacecraft, smallsat-cubesat, cubesat, smallsat, cubesat-design-spec, p-pod, deployer, launch-provider-icd]
level: practitioner
status: verified
description: "Check CubeSat compliance with the CubeSat Design Specification: form factor, deployer interface, deployables, inhibits and testing, with reference to the launch provider ICD."
sources:
  - "CubeSat Design Specification (California Polytechnic State University CubeSat program, current revision)"
  - "Launch provider payload user guides and deployer interface documents"
  - "CubeSat Design Specification Rev 14.1 (February 2022): https://www.nasa.gov/wp-content/uploads/2018/01/cubesatdesignspecificationrev14_12022-02-09.pdf"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# CubeSat Design Specification compliance

**Goal:** a CubeSat that the launch provider and deployer will accept. Always use the current CDS revision and the provider's interface document.

## Checklist (confirm values in the current revision)
- **Form factor:** 1U is 10 cm cube; rails with specified dimensions, surface roughness below 1.6 micrometres (CDS 2.2.6) and hard-anodised rail surfaces that contact the dispenser; envelope for multi-U sizes (1.5U, 2U, 3U, 6U, 12U) in the specification; rails make contact with the deployer.
- **Mass and centre of mass:** CDS Rev 14.1 gives typical maximum masses of 2, 3, 4, 6, 12 and 24 kg for 1U, 1.5U, 2U, 3U, 6U and 12U (larger masses are decided mission by mission with the dispenser provider), and a centre of gravity within +/-2 cm of the geometric centre on X and Y (the Z range grows with size, for example +/-4.5 cm for 3U).
- **Deployables and switches:** deployable items restrained until in orbit; at least one deployment switch and a remove-before-flight pin so the satellite is off during integration and stays off until deployment; CDS Rev 14.1 requires at least three independent inhibits for propulsion activation, for RF transmission and for release of deployables (some launch providers accept fewer for RF, check the ICD).
- **Pyrotechnics and hazardous materials:** pyrotechnics and hazardous materials must conform to AFSPCMAN 91-710 Volume 3 (CDS 2.1.2 and 2.1.6); pressure vessels and propulsion need safety documentation.
- **Testing:** vibration, thermal vacuum and other tests as required by the launch provider and the CDS; shock requirements follow the provider.
- **Documentation:** safety data, orbital debris assessment, frequency licences, and a launch provider interface agreement.

## Procedure
1. Pick the deployer and launcher; get their ICD.
2. Map each CDS and ICD requirement to a verification method (inspection, analysis, test) in a compliance matrix.
3. Plan a fit-check with a deployer or an equivalent test jig.
4. Close safety reviews with the launch provider.

## Gotchas
- Revision differences (mass limits, rail requirements): confirm the revision accepted by your provider.
- Battery safety and inhibits get close scrutiny.

## Verify
- [ ] Compliance matrix covers every CDS and ICD requirement with evidence.
