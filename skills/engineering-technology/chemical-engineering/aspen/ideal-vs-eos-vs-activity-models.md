---
id: engineering-technology.chemical-engineering.aspen.ideal-vs-eos-vs-activity-models
name: ideal-vs-eos-vs-activity-models
category: engineering-technology
field: chemical-engineering
product: aspen
tags: [chemical-engineering, aspen, aspen-property-method-selection, ideal-vs-eos-vs-activity-models, ideal-property-method, equation-of-state, activity-coefficient, gamma-phi, phi-phi, raoults-law, vle-modelling, aspen-plus]
level: practitioner
status: gated
description: "Contrast ideal, equation-of-state and activity-coefficient property models: what each assumes, where each fails, and what data each needs."
sources:
  - "Aspen Plus and Aspen HYSYS user guides and help (AspenTech), Seider et al. Product and Process Design Principles"
  - "https://www.aiche.org"
  - "AspenTech Aspen Plus certification study guide AT-05198 (learning objectives, aspentech.com)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ideal vs equation-of-state vs activity-coefficient models

**Goal:** know what you are assuming when you pick a model family so you can predict where it breaks.

## The three families
| Family | Equation | Good for | Fails for |
|---|---|---|---|
| Ideal (Raoult/Dalton) | y_i P = x_i P_i^sat | Similar non-polar molecules, low pressure | Any polar mixture, high pressure |
| Activity coefficient (gamma-phi) | y_i phi_i P = x_i gamma_i P_i^sat phi_i^sat (often with Poynting correction) | Polar non-electrolyte liquids at low to moderate pressure (about 10 bar is a rule of thumb (gated: unconfirmed, source is paywalled or blocked)), LLE | Near-critical, supercritical gases, high pressure |
| EoS (phi-phi) | phi_i^V y_i = phi_i^L x_i | Hydrocarbons, light gases, high pressure, near-critical, consistent density | Strongly polar or associating liquids (without special mixing rules) |

## How to decide in practice
1. Ask whether the liquid is non-ideal: estimate gamma_i from a quick UNIFAC run or from literature. If gamma deviates strongly from 1 an ideal model is out; the band 0.7 to 1.5 is only a rough screening rule, not a standard (gated: unconfirmed, source is paywalled or blocked).
2. Ask whether pressure or temperature approaches critical conditions of any component; if yes, you need an EoS (or an activity model with Henry's law for gases).
3. Liquid-liquid splitting needs an activity model fitted to LLE data or an EoS with suitable binaries; ideal models can never predict two liquid phases.

## Data needs
- Ideal: pure-component vapour pressure (Antoine or similar).
- Activity: binary interaction parameters for each pair (see `engineering-technology.chemical-engineering.aspen.binary-interaction-parameter-retrieval`).
- EoS: critical properties, acentric factor, k_ij binaries.

## Gotchas
- A gamma-phi model uses the vapour-phase fugacity coefficient only if you select a vapour model; many default to ideal vapour, wrong for acetic acid or HF.
- Parameters are fitted over a temperature range; extrapolating fitted gamma parameters far outside it is unreliable.

## Verify
- [ ] Model family matches the polarity and pressure window.
- [ ] A pure-component and a binary check against data pass.
