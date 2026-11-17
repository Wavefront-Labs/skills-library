---
id: engineering-technology.biomedical-engineering.biomaterials.passivation-astm-f86
name: passivation-astm-f86
category: engineering-technology
field: biomedical-engineering
product: biomaterials
tags: [passivation, implant-corrosion, fretting-corrosion, astm-f86, astm-a967, nitric-acid-passivation, citric-acid-passivation, surface-preparation]
level: practitioner
status: draft
description: "Passivate implant metals: cleaning, nitric or citric acid process parameters, titanium and stainless differences, rinse and verification tests with ASTM F86 and A967."
sources: ["ASTM F86 Standard practice for surface preparation and marking of metallic surgical implants (confirm edition)", "ASTM A967 Standard specification for chemical passivation treatments for stainless steel parts (confirm edition)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Passivation of implant metals

**Goal:** remove free iron and contaminants and restore a continuous chromium or titanium oxide film so the implant resists corrosion.

Quality-critical process; parameters are validated per process validation (see process-validation-iq-oq-pq) and specified by the standards in force.

## Sequence
1. **Machining finish:** deburr, polish and clean; surface roughness and burrs set crevices.
2. **Alkaline or solvent cleaning** to remove oils and cutting fluid; ultrasonic with a rinse.
3. **Acid passivation** (examples; confirm parameters in the standards and validate):
   - Stainless steel and cobalt-chromium: nitric acid solution (roughly 20-40% by volume) at about 50-60 C for about 20-30 minutes, or citric acid solutions (about 4-10 wt%) at about 50-70 C for several minutes, per ASTM A967 options.
   - Titanium and its alloys: nitric acid (about 20-40%) at room temperature for about 30 minutes per ASTM F86 (hydrofluoric acid is not used in passivation; an etch with HF-nitric is a separate pickling step).
4. **Rinse** in deionised water until neutral and free of residue; dry.
5. **Marking:** laser or electrochemical marks are made before passivation or are passivated again, since marking disturbs the oxide (F86 gives guidance).
6. **Handling and packaging** in clean conditions to avoid iron contamination.

## Verification
- **Water immersion or high-humidity test** for free iron (ASTM A967 tests), **copper sulphate test** for stainless steel (identifies free iron by copper plating), **potassium ferricyanide (ferroxyl) test** (blue stain for iron).
- Surface analysis (XPS, Auger) to show Cr/Fe ratio or oxide thickness in validation.
- Corrosion testing on the final surface (see cyclic-polarization-astm-f2129).

## Gotchas
- Passivating before final machining or welding; heat tint after welding or laser marking needs removal.
- Carry-over of chloride contamination in rinse water.
- Using one bath for stainless and titanium (cross-contamination).

## Verify
- [ ] Batch records show bath concentration, temperature, time and rinse resistivity.
- [ ] Verification test passed for each lot or per the validated frequency.
- [ ] Marks are corrosion tested.
