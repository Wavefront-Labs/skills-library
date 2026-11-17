---
id: engineering-technology.biomedical-engineering.biomedical-instrumentation.biphasic-defibrillation-waveform
name: biphasic-defibrillation-waveform
category: engineering-technology
field: biomedical-engineering
product: biomedical-instrumentation
tags: [biphasic-waveform, defibrillator, electrosurgery, defibrillation, truncated-exponential, rectilinear-biphasic, transthoracic-impedance, iec-60601-2-4]
level: advanced
status: verified
description: "Understand biphasic defibrillator waveforms: truncated exponential versus rectilinear, tilt, energy and impedance compensation, and verification against IEC 60601-2-4."
sources: ["IEC 60601-2-4 Particular requirements for the basic safety and essential performance of cardiac defibrillators (confirm edition)", "Resuscitation guideline documents (AHA and ERC) for clinical energy recommendations (confirm current)", "Kerber et al., Energy current and success in defibrillation and cardioversion (Circulation 1988)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Biphasic defibrillation waveform

**Goal:** deliver a waveform that terminates ventricular fibrillation effectively at lower energy than monophasic, adapted to patient impedance.

Safety-critical device; clinical energy settings come from current resuscitation guidelines and the manufacturer's evidence, not from this note.

## Waveform types
- **Biphasic truncated exponential (BTE):** capacitor discharges through the patient; positive phase, then the polarity is reversed and the second phase is truncated. The shape is defined by capacitance, voltage, impedance and the truncation time.
- **Rectilinear biphasic (RLB):** a controlled-current phase that stays near constant, then reverses.
- **Pulsed biphasic:** series of short pulses.
- Typical capacitors are in the order of 100-200 microfarad charged to a few kilovolts, with the energy stored E = 1/2 C V^2.

## Impedance compensation
Transthoracic impedance varies widely among patients (roughly 25-180 ohms, average about 70-80) (gated: unconfirmed, source is paywalled or blocked). The device measures impedance during a low-energy test pulse or the first phase and adjusts phase durations or voltage (a "tilt" target) to keep delivered energy and current appropriate.

## Design and test
1. Define waveform parameters (voltages, durations, tilt) and the energy accuracy at defined loads (for example 25, 50, 75, 100, 125, 150, 175 ohms; confirm the load set in IEC 60601-2-4).
2. Verify with a defibrillator analyser or tester with a specified load; compare energy, peak current and phase timing against specifications.
3. Charge time from battery to full energy and after a discharge cycle; battery capacity for a set number of shocks.
4. Safety: output isolation, no discharge into the operator, patient leakage, selection of internal versus external paddles, and fault-state behaviour.
5. IEC 60601-2-4 sets requirements for energy accuracy, charge time, output safety and ECG synchronisation (for cardioversion).

## Gotchas
- Energy delivered depends on impedance; the nominal setting is not the value at the patient.
- Capacitor leakage and battery ageing lengthen charge time.

## Verify
- [ ] Delivered energy accuracy across the load range per the standard.
- [ ] Synchronisation timing for cardioversion mode.
- [ ] Charge-time and shock-count tests with a low battery.
