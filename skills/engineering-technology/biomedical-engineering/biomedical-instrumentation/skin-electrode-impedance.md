---
id: engineering-technology.biomedical-engineering.biomedical-instrumentation.skin-electrode-impedance
name: skin-electrode-impedance
category: engineering-technology
field: biomedical-engineering
product: biomedical-instrumentation
tags: [skin-impedance, biopotential-electrodes, electrode-skin-interface, electrode-impedance, stratum-corneum, impedance-imbalance, cmrr]
level: practitioner
status: gated
description: "Understand and measure skin-electrode impedance: stratum corneum model, frequency behaviour, skin preparation effects, typical values and effect on noise and CMRR."
sources: ["Webster (ed.), Medical Instrumentation: Application and Design (biopotential electrodes chapter)", "AAMI/ANSI EC12 Disposable ECG electrodes (confirm current edition)", "https://www.aami.org"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Skin-electrode impedance

**Goal:** know what impedance an electrode presents, how to measure it, and what it does to your amplifier.

## Model
- The stratum corneum (dead skin layer) dominates impedance at low frequency: a resistance Rs (gel and deeper tissue) in series with a parallel combination of Rp (skin) and Cp (skin capacitance), plus the electrode half-cell potential (see half-cell-potential).
- Impedance falls with frequency: dry skin can be hundreds of kilohms to megohms near 10 Hz; abraded and gelled skin falls to tens of kilohms (gated: unconfirmed, source is paywalled or blocked).
- Variation: sweat, hair, skin dryness, applied pressure, movement and electrode area.

## Measurement
1. Use a small AC current at a stated frequency (10 Hz is common for ECG; 30 Hz or higher for EEG impedance checks (gated: unconfirmed, source is paywalled or blocked)), well below patient auxiliary current limits.
2. Measure between electrode pairs on the subject or a skin-model test circuit.
3. Compare pair imbalance as well as absolute values.

## Why it matters
- **Thermal noise:** sqrt(4kTR) rises with resistance.
- **Interference:** mains current flowing through unequal electrode impedances makes a differential voltage, so mismatch of 10 kOhm values can turn into large interference; the amplifier's input impedance must be far larger than skin impedance, and CMRR is degraded by imbalance.
- **Motion artefact:** mostly from changes in the electrode-skin potential and impedance.

## Reducing it
- Clean with alcohol; light abrasion; conductive gel; larger contact area; firmer and stable fixation; shorter, shielded leads; active electrodes (a buffer at the electrode) for dry types.

## Verify
- [ ] Impedance pairs recorded and matched.
- [ ] Amplifier input impedance at least 100 times electrode impedance (rule of thumb (gated: unconfirmed, source is paywalled or blocked)).
- [ ] Signal-to-noise confirmed with a known test signal.
