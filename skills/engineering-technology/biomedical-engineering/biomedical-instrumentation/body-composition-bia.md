---
id: engineering-technology.biomedical-engineering.biomedical-instrumentation.body-composition-bia
name: body-composition-bia
category: engineering-technology
field: biomedical-engineering
product: biomedical-instrumentation
tags: [body-composition-bia, bia, bioimpedance-analysis, total-body-water, fat-free-mass]
level: practitioner
status: draft
description: "Design and use bioimpedance body composition devices: single and multi-frequency BIA, electrode configuration, prediction equations, sources of error and contraindications."
sources: ["Kyle et al., Bioelectrical impedance analysis, parts I and II (ESPEN guidelines, Clin Nutr, 2004; confirm current guidance)", "Webster (ed.), Medical Instrumentation: Application and Design (bioimpedance)", "https://www.espen.org"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Body composition by BIA

**Goal:** estimate body water and fat-free mass from impedance with known error and clear limits.

## Method
- **Single-frequency BIA (often 50 kHz):** measures impedance (resistance and reactance) along the body. Total body water is predicted from the impedance index (height squared divided by resistance) with population equations; fat-free mass follows from a hydration assumption.
- **Multi-frequency and bioimpedance spectroscopy:** low frequencies reflect extracellular water, higher frequencies total water, with fitted Cole models (see cole-model).
- **Electrode setup:** hand-to-foot (tetrapolar) with fixed placement; foot-to-foot or hand-to-hand devices measure part of the body and rely on equations.

## Error sources
- Hydration state, recent exercise, meals and alcohol, skin temperature, posture and electrode placement; ethnicity and age differences in the equations' validity.
- Predictive equations are population-specific; validate against a reference such as DXA or dilution methods for the intended population.
- Device accuracy at individual level is lower than at group level.

## Safety
- Low current well within patient auxiliary limits; manufacturers commonly contraindicate use with implanted electronic devices such as pacemakers unless validated; confirm labelling.

## Verify
- [ ] Equation validation population and reference method stated.
- [ ] Standardised measurement protocol written.
- [ ] Precision (repeat measurement) and bias reported.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
