---
id: engineering-technology.biomedical-engineering.biomaterials.plga-degradation
name: plga-degradation
category: engineering-technology
field: biomedical-engineering
product: biomaterials
tags: [plga, bioresorbable, biodegradable-polymers, polylactic-acid, plla, hydrolysis, molecular-weight, degradation-profile, iso-13781, astm-f1635]
level: advanced
status: verified
description: "Predict and test PLGA and PLA implant degradation: hydrolysis, copolymer ratio, molecular weight loss, autocatalysis, sterilisation effects and ISO 13781 style in-vitro methods."
sources: ["ASTM F1635 Standard test method for in vitro degradation testing of hydrolytically degradable polymer resins and fabricated forms for surgical implants (confirm edition)", "ISO 13781:2017 Implants for surgery - Homopolymers, copolymers and blends on poly(lactide) - In vitro degradation testing", "Middleton and Tipton, Synthetic biodegradable polymers as orthopedic devices (Biomaterials 2000)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# PLGA and PLA degradation

**Goal:** know when a polyester implant loses molecular weight, strength and mass, so the degradation matches the healing timeline.

## Mechanism
- Ester bonds hydrolyse in water to give lactic and glycolic acid; rate depends on temperature, pH, crystallinity, molecular weight and device thickness.
- **Bulk erosion:** water penetrates the entire part; molecular weight falls first, then strength, then mass. Acidic products trapped in thick parts accelerate degradation inside (**autocatalysis**), so thick sections can degrade faster in the centre.
- **Copolymer ratio:** PLLA (crystalline) degrades slowest and PDLLA (amorphous) faster; 50:50 PLGA degrades fastest of the family (reported as about 1-2 months, rising to several months at 75:25 and 85:15). Take PLLA timescales from grade data. Glycolide-rich copolymers absorb water faster.
- Tg of PLGA is roughly 40-50 C depending on grade and molecular weight (a supplier datasheet lists 45-50 C for 50:50), so it is near body temperature and mechanical creep can occur.

## Test plan
1. Immerse samples in phosphate-buffered saline pH 7.4 at 37 C (ISO 13781, ASTM F1635), volume to mass ratio specified, with buffer renewal.
2. At intervals (for example weekly to monthly) remove replicates and measure: **molecular weight** by gel permeation chromatography, **mass loss**, **mechanical properties** (tensile or bending), pH of medium, thermal properties (DSC for crystallinity), and morphology (SEM).
3. Plot Mw versus time (often exponential decay with first-order hydrolysis) and strength versus Mw.
4. Real-time degradation is slow; accelerated testing at elevated temperature (for example 50-60 C, below Tg) must be justified, as mechanism and Arrhenius assumptions can break near Tg.

## Process effects
- Sterilisation: EO preferred over gamma for many polyesters (gamma lowers Mw); electron beam at low dose possible; check Mw after sterilisation.
- Storage: moisture-barrier packaging and desiccant (hydrolysis starts in the package).
- Processing (extrusion, injection moulding) lowers Mw through thermal and hydrolytic degradation; dry resin before processing.

## Verify
- [ ] Mw, strength and mass profile matches the clinical requirement window.
- [ ] Degradation products and local tissue response addressed in biological evaluation (ISO 10993-13 is scoped to non-resorbable polymers, so plan the product analysis with a toxicologist and ASTM F1635 and ISO 13781).
- [ ] Shelf life of the packaged device verified for Mw.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
