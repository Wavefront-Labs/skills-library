---
id: engineering-technology.biomedical-engineering.medical-imaging-systems.cmut-pmut
name: cmut-pmut
category: engineering-technology
field: biomedical-engineering
product: medical-imaging-systems
tags: [cmut, pmut, micromachined-transducer, capacitive-transducer, ultrasound-mems]
level: advanced
status: gated
description: "Compare capacitive and piezoelectric micromachined ultrasound transducers (CMUT, PMUT): operation, bias and collapse, bandwidth, charging, integration, limits versus PZT."
sources: ["Oralkan et al., Capacitive micromachined ultrasonic transducers: next-generation arrays for acoustic imaging? (IEEE Trans Ultrason Ferroelectr Freq Control 2002;49:1596-1610)", "https://www.ieee-uffc.org"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# CMUT and PMUT

**Goal:** understand micromachined ultrasound transducers and when they beat bulk PZT arrays.

## CMUT
- A thin membrane suspended over a gap with electrodes; applying DC bias plus AC drive makes the membrane vibrate. Sensitivity rises as the bias nears the **pull-in (collapse) voltage**, where the membrane snaps to the substrate; operation can be below pull-in (conventional) or in collapse mode with different bandwidth and output behaviour.
- Advantages: very wide fractional bandwidth (often exceeding 100 percent (gated: unconfirmed, source is paywalled or blocked)), good acoustic matching to fluid, fabrication with semiconductor processes, and integration with electronics (CMOS), enabling dense 2D arrays and catheter probes.
- Challenges: high bias voltage (tens to hundreds of volts (gated: unconfirmed, source is paywalled or blocked)), dielectric charging drift, crosstalk through the substrate, fabrication yield and the tendency for lower output pressure than PZT.

## PMUT
- A thin piezoelectric film (aluminium nitride or PZT thin film) on a membrane, giving lower drive voltage and no bias; lower coupling and output than bulk piezo; used in compact, low-power and fingerprint or proximity sensors, and in research arrays.

## Selection
1. Required frequency, bandwidth and output pressure (diagnostic limits; see acoustic-output-safety).
2. Array size and need for ASIC integration.
3. Voltage and power available in the handheld or catheter.
4. Reliability and manufacturing maturity (PZT is the incumbent).

## Verify
- [ ] Measured bandwidth, sensitivity and output pressure per element.
- [ ] Bias drift and lifetime tested.
- [ ] Safety of high-bias electronics for the patient (leakage and isolation).

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
