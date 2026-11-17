---
id: engineering-technology.biomedical-engineering.biomaterials.bone-cement
name: bone-cement
category: engineering-technology
field: biomedical-engineering
product: biomaterials
tags: [bone-cement, uhmwpe, peek, pmma, implant-polymers, iso-5833, vacuum-mixing, antibiotic-cement, radiopacifier, cement-exotherm]
level: practitioner
status: verified
description: "Specify and handle PMMA bone cement: ISO 5833 requirements, mixing and viscosity phases, porosity and vacuum mixing, exotherm, antibiotic loading and safety issues."
sources: ["ISO 5833 Implants for surgery - Acrylic resin cements (confirm edition)", "ASTM F451 Standard specification for acrylic bone cement (confirm edition)", "Kuhn, Bone Cements: Up-to-Date Comparison of Physical and Chemical Properties of Commercial Materials"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# PMMA bone cement

**Goal:** a cement that cures reliably in the operating theatre and meets strength, setting and thermal requirements.

Clinical use is by surgeons following manufacturer instructions; this is a materials and engineering summary.

## Composition
- **Powder:** PMMA or copolymer beads, benzoyl peroxide initiator, radiopacifier (barium sulphate or zirconium dioxide, about 10% (gated: unconfirmed, source is paywalled or blocked)).
- **Liquid:** methyl methacrylate (MMA) monomer, N,N-dimethyl-p-toluidine accelerator, hydroquinone stabiliser.
- Antibiotic-loaded cements add gentamicin, tobramycin or other powdered antibiotics (heat stable); high doses reduce strength.

## Curing phases
Mixing (powder and liquid combine), waiting (sticky), working (non-sticky dough for application) and setting. Times depend on temperature and humidity (a cold monomer extends the working time) and viscosity class (low, medium, high).

## ISO 5833 requirements (as commonly cited; confirm in the current edition)
- **Compressive strength** at least 70 MPa, **bending strength** at least 50 MPa and **bending modulus** at least 1800 MPa (these three minimums match values quoted in papers testing cements against ISO 5833:2002; confirm in the current edition).
- **Maximum exotherm temperature** not above about 90 C and **setting time** between about 3 and 15 minutes (gated: unconfirmed, source is paywalled or blocked).
- Dough time and liquid and powder packaging requirements.

## Engineering concerns
- **Porosity:** voids lower fatigue life; **vacuum mixing** and centrifugation reduce porosity.
- **Exotherm and monomer:** polymerisation heat and residual monomer can injure tissue; limits on cement thickness and mantle design.
- **Interfaces:** cement-bone interlock and cement-implant debonding (smooth stems versus rough-surfaced designs).
- **Adverse events:** monomer-related cardiovascular reactions during cementation (bone cement implantation syndrome); address in instructions and risk file.
- Radiopacity for imaging; stability on storage and EO sterilisation of powder components.

## Verify
- [ ] Mechanical tests per ISO 5833 on cured specimens at 37 C.
- [ ] Setting time and exotherm measured at defined temperatures.
- [ ] Mixing system validated for porosity in the intended use.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
