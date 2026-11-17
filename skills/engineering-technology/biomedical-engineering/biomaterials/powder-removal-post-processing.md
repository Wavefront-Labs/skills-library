---
id: engineering-technology.biomedical-engineering.biomaterials.powder-removal-post-processing
name: powder-removal-post-processing
category: engineering-technology
field: biomedical-engineering
product: biomaterials
tags: [powder-removal, am-post-processing, depowdering, residual-powder, support-removal]
level: advanced
status: draft
description: "Remove powder and post-process AM implants: depowdering methods, cleaning validation, heat treatment, HIP, surface finishing, residue testing and traceability."
sources: ["FDA, Technical Considerations for Additive Manufactured Medical Devices (confirm current text)", "ASTM F3001 and ISO/ASTM 52900 series (confirm applicable parts and editions)", "https://www.fda.gov"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Powder removal and post-processing

**Goal:** a clean, stress-relieved and dimensionally correct additively manufactured part, with validated cleaning.

## Steps
1. **Depowdering:** remove loose powder by brushing, compressed air, vibration or ultrasonic and fluid flushing; complex lattices and internal channels need designed access holes.
2. **Support and plate removal:** wire EDM or cutting from the plate, mechanical support removal, with dimension checks.
3. **Stress relief and heat treatment:** relieve residual stress before removal from the plate for many titanium builds; follow with annealing; **hot isostatic pressing (HIP)** closes internal porosity and improves fatigue.
4. **Surface finishing:** machining critical features, grit blasting, chemical etching, electropolishing, tumbling; each changes dimensions and fatigue behaviour.
5. **Cleaning:** multi-step aqueous or solvent cleaning, ultrasonic; passivation; final cleaning verification.

## Validation
- Validate cleaning for residual powder and processing aids: gravimetric, particle counting, visual inspection under magnification, micro-CT for hidden powder, and extractables (see chemical-characterization).
- Document traceability of powder lot, build, plate position and post-process sequence per part.

## Risks
- Trapped powder releasing later in the body; contamination from cleaning solvents; dimensional change by etching; reuse of powder alters chemistry (oxygen pick-up).

## Verify
- [ ] Cleaning validation shows residuals below limit on the worst-case geometry.
- [ ] Post-process steps validated and under change control.
- [ ] Records link each part to its build and powder lot.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
