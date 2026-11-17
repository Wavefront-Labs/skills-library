---
id: engineering-technology.aerospace-engineering.aircraft-structures.corrosion-and-stress-corrosion-cracking
name: corrosion-and-stress-corrosion-cracking
category: engineering-technology
field: aerospace-engineering
product: aircraft-structures
tags: [stress-corrosion, scc, galvanic-corrosion, exfoliation, corrosion-control, aerospace-materials]
level: practitioner
status: draft
description: "Control corrosion and stress-corrosion cracking in airframe design by material and temper selection, galvanic isolation, sealants, and sustained-stress limits."
sources:
  - "MMPDS (corrosion and SCC guidance)"
  - "ASTM G47"
  - "ASTM G34"
  - "Niu, Airframe Structural Design"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Corrosion and stress corrosion

**Goal:** design out the common airframe corrosion failures.

## Stress corrosion cracking (SCC)
Needs three together: a susceptible alloy and temper, sustained tensile stress (applied plus residual), and a corrosive environment. It strikes high-strength aluminium (7xxx-T6 in the short-transverse direction), some steels and titanium.
- Choose resistant tempers (7xxx in T73-class or T76-class tempers, 2xxx in T8 tempers).
- Avoid sustained short-transverse tensile stress in thick plate and forgings, including from assembly (press fits, shimming, forced fit-up).
- Use shot peening and stress-relief to cut residual stress.
- ASTM G47 is a test method for SCC susceptibility of 2xxx and 7xxx products.

## Other forms
- **Exfoliation**: grain-boundary attack in rolled and extruded 2xxx and 7xxx; ASTM G34 (EXCO) is a susceptibility test.
- **Galvanic**: dissimilar metals in contact with electrolyte; carbon-fibre composites are noble against aluminium, so isolate with a glass ply or sealant and use compatible fasteners (titanium or corrosion-resistant steel).
- **Crevice and pitting**: avoid water traps, seal faying surfaces, provide drainage.
- **Fretting and intergranular attack**: protect lug and joint interfaces.

## Practice
1. Specify finishes: anodise, chromate-free primer systems where required by environmental rules, topcoat and sealant.
2. Define faying surface treatment and wet installation of fasteners.
3. Include corrosion in maintenance programme tasks.

## Gotchas
- Regulations on hexavalent chromium and cadmium vary by region; confirm current rules for your programme.
- Corrosion pits become fatigue initiation sites.

## Verify
- [ ] Every dissimilar-material interface on the drawing shows its isolation method.
