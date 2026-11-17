---
id: engineering-technology.biomedical-engineering.medical-device-design.radiation-sterilization-materials
name: radiation-sterilization-materials
category: engineering-technology
field: biomedical-engineering
product: medical-device-design
tags: [gamma-irradiation, e-beam, radiation-sterilization, material-compatibility, polymer-degradation]
level: practitioner
status: gated
description: "Assess how gamma and electron-beam dose affects polymers, adhesives, electronics and packaging when choosing radiation sterilisation, including dose range and stabilised grades."
sources: ["ISO 11137-1 Sterilization of health care products - Radiation - Part 1: Requirements for development, validation and routine control of a sterilization process for medical devices (EN ISO 11137-1:2015 with Amd 2:2019 appears in the EU harmonised standards amending decision on EUR-Lex, CELEX 32021D1182; confirm the current edition)", "AAMI TIR17 Compatibility of materials subject to sterilization (confirm current edition)", "https://www.iso.org"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Material effects of gamma and e-beam sterilisation

**Goal:** choose materials that keep function across the sterilisation dose range, including the maximum dose and resterilisation.

## Principles
- Ionising radiation causes chain scission, crosslinking or both. Polyethylene tends to crosslink (gated: unconfirmed, source is paywalled or blocked) (UHMWPE gets oxidative degradation if free radicals remain, see crosslinked-uhmwpe); polypropylene, PTFE, acetal and cellulosics tend to scission and embrittle; PVC discolours.
- Oxygen presence and dose rate affect degradation. Post-irradiation oxidation continues during shelf life, so aged test samples matter.
- Dose has a minimum (to meet the sterility assurance level) and a maximum (what materials must survive). A commonly used minimum dose is 25 kGy (gated: unconfirmed, source is paywalled or blocked) but the validated dose comes from dose setting (see vdmax-dose-setting).
- Gamma (cobalt-60) is penetrating and slow (gated: unconfirmed, source is paywalled or blocked); e-beam is fast with limited penetration and more dose gradient in dense products.

## Method
1. Find vendor data and TIR17-type compatibility tables; treat as screening only.
2. Irradiate representative parts at 2-3 times the maximum validated dose where practical, age them (see accelerated-aging-astm-f1980) and test the critical properties: tensile and impact, colour, adhesion, seal strength, electrical function.
3. Electronics and batteries are usually not radiation compatible; assess early.
4. Use radiation-stabilised grades for polypropylene where needed.

## Verify
- [ ] Every material and component has compatibility evidence at maximum dose plus resterilisation.
- [ ] Aged post-irradiation properties still meet specification.
- [ ] Dose mapping confirms minimum and maximum dose in the product.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
