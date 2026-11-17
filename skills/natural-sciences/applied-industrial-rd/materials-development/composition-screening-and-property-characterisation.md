---
id: natural-sciences.applied-industrial-rd.materials-development.composition-screening-and-property-characterisation
name: composition-screening-and-property-characterisation
category: natural-sciences
field: applied-industrial-rd
product: materials-development
tags: [materials-development, applied-industrial-rd, materials-science, new-materials, composition-screening, high-throughput-screening, combinatorial, polymers, coatings, composites, characterisation, dsc, tga, dma, ftir, xrd, sem, tensile-testing, astm, iso-standards, adhesion-testing, weathering, accelerated-ageing, structure-property, process-property, tech-transfer, materials-informatics]
level: advanced
status: draft
description: "Develop a new material: requirement-led composition screening, a characterisation ladder (thermal, chemical, structural, mechanical), standard tests, ageing, and handover to production."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Composition screening and property characterisation

**Goal:** find a polymer, coating, composite or other material composition that
meets a property target, prove it with standard tests, and hand over a recipe
and process window production can reproduce.

## 1. Start from the requirement, not the chemistry
Write a property specification with the test method for each item:
"tensile strength ≥ 40 MPa (ISO 527), Tg ≥ 80 °C (DSC, midpoint), cross-hatch
adhesion class 0–1 on aluminium (ISO 2409), no cracking after 1,000 h QUV". Add
cost, processing route (extrusion, spray, cure schedule), regulatory limits
(REACH/TSCA status, restricted substances) and sustainability targets. A property
without a defined test is not a requirement.

## 2. Screening strategy
- **Rule out early:** literature, supplier data and simple models (rule of mixtures,
  group-contribution estimates, solubility parameters for compatibility) narrow candidates.
- **Design the screen** with DoE or mixture designs (see
  natural-sciences.applied-industrial-rd.formulation-science.doe-screening-for-new-formulations);
  high-throughput approaches (small-volume arrays, robotic dispensing, thin-film libraries)
  suit many-component spaces if a fast **proxy test** exists.
- **Proxy tests** must correlate with the real test — check correlation on a few
  samples before trusting a screen built on them.
- Materials informatics/ML models help when there's enough consistent historical
  data; they extrapolate poorly outside the training space.

## 3. The characterisation ladder (cheap and fast first)
1. **Chemical identity/cure:** FTIR (functional groups, degree of cure by peak
   disappearance), NMR for structure, GPC/SEC for polymer molecular weight.
2. **Thermal:** DSC (Tg, melting, crystallinity, residual cure), TGA (decomposition
   onset, filler content, moisture/volatiles).
3. **Structure/morphology:** XRD (crystalline phases), SEM/EDS (microstructure,
   dispersion, fracture surfaces), optical microscopy.
4. **Mechanical:** tensile, flexural, impact, hardness; DMA for modulus vs temperature.
5. **Application tests:** adhesion, scratch, chemical resistance, barrier, electrical.
6. **Durability:** accelerated weathering (UV/condensation, xenon arc), humidity,
   thermal cycling, salt spray for coatings on metal, creep and fatigue.

## 4. Test discipline
- Use **standard methods** (ASTM/ISO) and the stated specimen geometry,
  conditioning (often 23 °C/50% RH for a set time), and test speed. Changing any
  of these changes the number.
- Test enough specimens (standards often specify ≥5) and report mean, SD and
  failure mode.
- Include a **reference material** (incumbent product or a control batch) in every
  test series to detect drift.
- **Process history** matters: cure schedule, cooling rate, moisture in
  hygroscopic polymers (dry nylon/PET before moulding), filler dispersion. Record it.

## 5. Structure–process–property thinking
When a property misses target, ask which structure feature controls it (crosslink
density, crystallinity, filler dispersion, interface adhesion, porosity) and which
process step sets that feature. Fix the cause, not the number.

## 6. Handover to production
- A specification with tolerances for raw materials (including grade and supplier)
  and the **process window** (temperatures, times, mixing energy, cure).
- Scale-up batches at pilot scale reproducing key properties.
- Test methods, acceptance criteria and retained samples for QC.
- Safety data and regulatory status of all components.

## Gotchas
- Supplier grade changes silently alter performance; specify grades precisely.
- Accelerated ageing can introduce failure modes that never happen in service, or miss real ones.
- Small lab specimens show fewer defects than large parts — expect a scale penalty.

## Verify
- [ ] Every requirement has a named test method and acceptance value.
- [ ] Screening proxy tests checked for correlation with the real test.
- [ ] Standard specimen prep and conditioning used; reference material in each series.
- [ ] Durability tested under conditions tied to the service environment.
- [ ] Recipe and process window reproduced at pilot scale before handover.

*Draft note:* standard numbers given are examples; confirm the current edition and
the exact method your customer specifies.
