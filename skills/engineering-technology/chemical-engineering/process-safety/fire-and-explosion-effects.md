---
id: engineering-technology.chemical-engineering.process-safety.fire-and-explosion-effects
name: fire-and-explosion-effects
category: engineering-technology
field: chemical-engineering
product: process-safety
tags: [chemical-engineering, process-safety, ps-consequence-modelling, fire-and-explosion-effects, pool-fire, jet-fire, flash-fire, bleve, vapour-cloud-explosion, tnt-equivalency, multi-energy-method, thermal-radiation, overpressure]
level: advanced
status: gated
description: "Estimate effects of process fires and explosions (pool fire, jet fire, flash fire, BLEVE, vapour cloud explosion) for facility siting, with stated uncertainty."
sources:
  - "CCPS Guidelines for Hazard Evaluation Procedures, CCPS Layer of Protection Analysis, API Standards 520 521 526 and 2000, IEC 61511, OSHA 29 CFR 1910.119, EU Seveso III Directive 2012/18/EU, Crowl and Louvar Chemical Process Safety, Lees Loss Prevention in the Process Industries"
  - "https://www.aiche.org"
  - "https://www.osha.gov"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fire and explosion effects

**Goal:** hazard distances from credible accident scenarios for siting, layout and emergency planning (accident prevention and protection). Use validated methods and a competent consequence analyst; the uncertainty is large.

## Fires
- **Pool fire**: burning rate from the liquid's heat of combustion and vaporisation; flame size from correlations (Thomas, Mudan and Croce); received radiation q = tau E F, with tau atmospheric transmissivity, E the surface emissive power and F the view factor.
- **Jet fire**: flame length from the release rate and orifice diameter (for example Chamberlain, API 521 type correlations), radiation from the flame fraction of heat released.
- **Flash fire**: the flammable cloud ignites; the hazard zone is the cloud footprint to the lower flammable limit, with fatality assumed inside.
- **BLEVE** (boiling liquid expanding vapour explosion) and **fireball**: fireball diameter and duration scale with the mass m: for example D about 5.8 m^(1/3) and t about 0.45 m^(1/3) (CCPS style correlations, m in kg; confirm in the reference) (gated: unconfirmed, source is paywalled or blocked), radiation through the fireball emissive power.

## Explosions
- **Vapour cloud explosion (VCE)**: overpressure depends on the fuel reactivity, confinement and congestion, ignition. Methods: TNT equivalency (W_TNT = eta m H_c/E_TNT with yield eta of a few percent and E_TNT about 4.2 to 4.7 MJ/kg (the thermochemical convention is 4.184 MJ/kg, NIST SP 811 Appendix B9; the spread of published blast-equivalent values is gated), scaled-distance overpressure charts), Multi-Energy Method (curve choice from the congestion and ignition strength), and Baker-Strehlow-Tang (flame speed tables); CFD for complex layouts.
- **Confined explosions and vessel burst**: stored energy methods.
- Damage criteria: overpressure and impulse versus damage (for example windows break at a few kPa; severe structural damage at tens of kPa (gated: unconfirmed, source is paywalled or blocked)); thermal radiation versus time to pain and fatality (published tables).

## Practice
1. Choose the scenarios (from the HAZOP/LOPA and release modelling); note frequency.
2. Select method and parameters; run sensitivity to confinement and ignition location.
3. Map the effect distances on the plot plan; compare with occupied buildings; take actions (distance, blast-resistant design, reduced inventory).
4. Cross-check with API RP 752/753 (building siting; confirm titles and current editions (gated: unconfirmed, source is paywalled or blocked)) or the equivalent regulatory siting guidance used by your organisation.

## Gotchas
- The explosion yield and congestion assumptions dominate; document them with the basis.
- Do not use TNT equivalency results as precise predictions.

## Verify
- [ ] Results consistent between at least two methods or with published benchmarks.
- [ ] Effect zones mapped and passed to the siting study.
