---
id: engineering-technology.biomedical-engineering.biomaterials.scaffold-porosity
name: scaffold-porosity
category: engineering-technology
field: biomedical-engineering
product: biomaterials
tags: [scaffold-porosity, hydrogel, tissue-scaffold, hydrogels-scaffolds, pore-size, interconnectivity, micro-ct, gibson-ashby, bone-ingrowth]
level: practitioner
status: draft
description: "Design and measure tissue-scaffold porosity: porosity fraction, pore size, interconnectivity, mechanical trade-off, micro-CT and porosimetry methods."
sources: ["Karageorgiou and Kaplan, Porosity of 3D biomaterial scaffolds and osteogenesis (Biomaterials 2005)", "Hollister, Porous scaffold design for tissue engineering (Nat Mater 2005)", "Gibson and Ashby, Cellular Solids: Structure and Properties"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Scaffold porosity and pore size

**Goal:** balance cell infiltration, nutrient transport and mechanical strength.

## Targets (bone, indicative)
- **Porosity:** commonly 60-90% for bone scaffolds; higher improves ingrowth but weakens the structure.
- **Pore size:** at least about 100 microns for cell migration and nutrient diffusion, with 200-500 microns often cited for bone ingrowth and vascularisation; smaller pores may favour cartilage; other tissues use other ranges. These are literature trends, not rules; define targets from your tissue and cell data.
- **Interconnectivity:** pores connected by throats large enough for cells (typically above 50-100 microns) so that pores do not form dead ends.

## Mechanics
- For open-cell foams, modulus scales roughly with relative density squared (Gibson-Ashby), so a 90% porous scaffold is about 100 times less stiff than a 100% porous-free one. Check that scaffold stiffness is suitable for the site (load-bearing vs non-load-bearing) and that stiffness changes as the material degrades.

## Fabrication links
- Salt leaching, gas foaming, freeze-drying, electrospinning (small pores), 3D printing (designed pores and lattices).
- Control pore size by porogen size or printing pitch, and strut diameter by nozzle.

## Measurement
1. **Gravimetric:** porosity = 1 - (scaffold density / material density).
2. **Micro-CT** (voxel size at least a few times smaller than the smallest pore): porosity, pore size distribution, connectivity and thickness maps.
3. **Mercury intrusion porosimetry** for pore throat sizes (not for soft hydrogels), **liquid displacement** or capillary flow porometry.
4. **SEM** for surface structure.

## Verify
- [ ] Measured porosity and pore size within targets across batches.
- [ ] Cell seeding efficiency and penetration depth confirmed in vitro.
- [ ] Compression modulus measured hydrated at 37 C.
