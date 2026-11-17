---
id: engineering-technology.biomedical-engineering.biomaterials.lattice-structures
name: lattice-structures
category: engineering-technology
field: biomedical-engineering
product: biomaterials
tags: [lattice-structure, porous-lattice, am-lattice, gyroid, trabecular-structure]
level: advanced
status: draft
description: "Design lattice structures for AM implants: unit cell types, pore and strut size, stiffness and strength prediction, fatigue notches, powder entrapment and testing."
sources: ["ASTM F3001 Additive manufacturing Ti-6Al-4V ELI with powder bed fusion (confirm edition)", "FDA, Technical Considerations for Additive Manufactured Medical Devices (confirm current text)", "https://www.astm.org"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Lattice structures

**Goal:** a porous structure that encourages bone ingrowth and tunes stiffness while remaining strong and manufacturable.

## Design variables
- **Unit cell:** strut-based (diamond, octet, cubic) or triply periodic minimal surface types (gyroid) with smooth curvature; bending-dominated cells are compliant and stretch-dominated cells are stiffer.
- **Pore size:** commonly cited ranges for bone ingrowth are roughly 300 to 600 micrometres, with porosity often 50 to 80 percent; treat as literature guidance and confirm for the application.
- **Strut or wall thickness:** limited by the process resolution (several hundred micrometres for typical metal powder bed fusion).
- **Gradients:** change density across the implant to match bone stiffness and add a solid core or skin for strength and fixation.

## Prediction and testing
1. **Stiffness and yield:** scale with relative density; use FE of the unit cell or full lattice, and validate with compression tests on built coupons (as-built geometry differs from CAD).
2. **Fatigue:** as-built surface roughness, partly melted particles and notches reduce fatigue strength; test built lattice coupons and the final part; stress relief and surface finishing (chemical etch, hot isostatic pressing) matter.
3. **Dimensional verification** by micro-CT of struts and pores versus design.
4. **Powder entrapment** inside small pores (see powder-removal-post-processing).
5. **Biological performance:** animal studies of bone ingrowth.

## Verify
- [ ] Built strut size and porosity within tolerance by micro-CT.
- [ ] Compression and fatigue properties measured on as-built samples.
- [ ] Cleanliness and powder removal validated.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
