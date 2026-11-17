---
id: engineering-technology.biomedical-engineering.biomedical-instrumentation.infrared-thermometry
name: infrared-thermometry
category: engineering-technology
field: biomedical-engineering
product: biomedical-instrumentation
tags: [infrared-thermometer, ir-thermometer, emissivity, ear-thermometer, forehead-thermometer]
level: practitioner
status: gated
description: "Design and verify infrared clinical thermometers: radiation physics, emissivity, ambient compensation, field of view, calibration with blackbody sources, and accuracy standards."
sources: ["ISO 80601-2-56 Clinical thermometers for body temperature measurement (confirm edition)", "ASTM E1965-98(2016) Infrared thermometers for intermittent determination of patient temperature (listed as withdrawn 23 Feb 2023 by BSI Knowledge)", "https://www.iso.org"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Infrared thermometry

**Goal:** an accurate, repeatable body temperature estimate from thermal radiation, with known sources of error.

## Physics
- A sensor (thermopile) receives radiation that depends on the target temperature and emissivity (skin and eardrum are close to blackbody, emissivity about 0.98 (gated: unconfirmed, source is paywalled or blocked)) and on the sensor's own temperature; the Stefan-Boltzmann law gives power proportional to the fourth power of absolute temperature.
- Because the reading depends on ambient and sensor temperature, devices compensate with an internal temperature sensor and ambient testing across the operating range.

## Design and verification
1. **Optics:** field of view and distance spot size (for non-contact forehead types); for ear types, probe geometry and tip warmth.
2. **Calibration:** against a blackbody reference source at several temperatures in the body range, in an environment with controlled ambient (laboratory accuracy requirement in ISO 80601-2-56 is of the order of 0.2 C over about 35 to 42 C (gated: unconfirmed, source is paywalled or blocked)).
3. **Clinical bias:** forehead and ear readings differ from core temperature; devices display an adjusted mode with an offset or algorithm; clinical accuracy needs a clinical study versus reference method.
4. **Use errors:** sweat, cold ambient, earwax and probe placement; instructions and training.
5. Cleaning and cross-infection control for probes; disposable probe covers.

## Verify
- [ ] Laboratory accuracy across ambient range using a blackbody.
- [ ] Clinical accuracy study planned and reported.
- [ ] Instructions address common user errors.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
