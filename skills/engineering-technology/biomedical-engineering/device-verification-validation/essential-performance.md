---
id: engineering-technology.biomedical-engineering.device-verification-validation.essential-performance
name: essential-performance
category: engineering-technology
field: biomedical-engineering
product: device-verification-validation
tags: [essential-performance, iec-60601-testing, hipot, electrical-safety-testing, basic-safety, risk-management, emc-pass-criteria]
level: practitioner
status: gated
description: "Define essential performance for IEC 60601-1: identify clinical functions whose loss creates unacceptable risk, set limits, link to risk file and use it as test pass criteria."
sources: ["IEC 60601-1:2005+AMD1:2012+AMD2:2020 (definition of essential performance and requirement to identify it; confirm edition)", "IEC 60601-1-2 (essential performance as the criterion for immunity tests; confirm edition)", "ISO 14971 Application of risk management to medical devices"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Defining essential performance

**Goal:** a short list of clinical functions that must not be lost or degraded beyond a stated limit, used as pass criteria in testing.

## Definition
**Essential performance** (IEC 60601-1 definition (gated: unconfirmed, source is paywalled or blocked)) is the performance of a clinical function, other than that related to basic safety, where loss or degradation beyond the limits specified by the manufacturer results in an **unacceptable risk**. A device may have none (if no clinical function carries unacceptable risk when lost), but that conclusion needs rationale.

## How to identify it
1. **List the clinical functions** of the device from intended use (monitoring, delivery, measurement, treatment, communication of alarms).
2. For each, ask: **if this function is lost or degraded, what harm can occur and how severe and likely?** Use the ISO 14971 risk analysis.
3. If the resulting risk is unacceptable after other controls, the function is essential; define it with **limits** that are measurable.
4. Examples:
   - Infusion pump: flow accuracy within a tolerance band, occlusion alarm, free-flow prevention.
   - Defibrillator: energy delivery accuracy and charge time, ECG synchronisation.
   - Patient monitor: accuracy of measured parameters within stated limits and alarms for vital signs.
   - Ventilator: delivered tidal volume or pressure accuracy, disconnection alarm.
   - Implantable stimulator: therapy output delivery accuracy and battery status indication.
5. Distinguish from **basic safety** (protection against hazards like shock, fire, mechanical) and from convenience features (display backlight, data export) which are not essential unless their loss causes unacceptable risk.

## Where it is used
- **EMC immunity testing:** pass criteria are that essential performance and basic safety are maintained during and after the test (see emc-immunity).
- **Single fault testing and software verification:** acceptable degraded states are defined.
- Labelling and the test report: state essential performance clearly (the standard requires it to be identified in the risk management file and accompanying documents).

## Gotchas
- Defining essential performance as "device functions normally" without limits.
- Listing too much, making tests impractical, or too little, missing critical risks.
- Forgetting accessories, software and network connections that carry the function.

## Verify
- [ ] Each essential performance item has a measurable limit and a verification method.
- [ ] Link from the risk file to the essential performance list.
- [ ] Test plan pass criteria quote the same limits.
