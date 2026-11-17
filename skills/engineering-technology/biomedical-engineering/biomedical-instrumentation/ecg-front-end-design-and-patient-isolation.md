---
id: engineering-technology.biomedical-engineering.biomedical-instrumentation.ecg-front-end-design-and-patient-isolation
name: ecg-front-end-design-and-patient-isolation
category: engineering-technology
field: biomedical-engineering
product: biomedical-instrumentation
tags: [ecg, ekg, analog-front-end, afe, instrumentation-amplifier, cmrr, right-leg-drive, driven-right-leg, ads1298, ads1292, electrode-offset, defibrillation-protection, iec-60601-1, iec-60601-2-25, iec-60601-2-27, iec-80601-2-86, patient-leakage-current, type-cf, type-bf, mopp, patient-isolation, lead-off-detection, pacemaker-detection]
level: advanced
status: gated
description: "Design an ECG front end: INA/24-bit AFE, CMRR and right-leg drive, 0.05-150 Hz vs 0.5-40 Hz bandwidth, defib-proof input protection, CF/BF leakage limits and 2-MOPP isolation."
sources: ["IEC 60601-1:2005+AMD1:2012+AMD2:2020 Medical electrical equipment - General requirements for basic safety and essential performance", "IEC 60601-2-25 Particular requirements for electrocardiographs", "IEC 60601-2-27 Particular requirements for electrocardiographic monitoring equipment", "IEC 80601-2-86 Particular requirements for electrocardiographs, including diagnostic, monitoring and ambulatory equipment", "Texas Instruments ADS1298 datasheet and ECG application notes", "Webster (ed.), Medical Instrumentation: Application and Design (4th ed.)"]
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# ECG front-end design and patient isolation — clean signal, safe patient

**Goal:** acquire a 0.1-5 mV ECG in the presence of ±300 mV electrode offset and volts of mains common-mode, survive defibrillation, and stay within IEC 60601-1 leakage and isolation limits.

Every standard-derived figure below (bandwidths, offsets, input impedance, leakage, MOPP voltages and distances, CMR test network, defibrillation) is (gated: unconfirmed, source is paywalled or blocked). The IEC 80601-2-86 draft status was confirmed from the ISO listing (iso.org/standard/74456.html, DIS stage) and a prEN IEC 80601-2-86:2026 draft entry at evs.ee; the ADS1298 LSB (0.0477 uV at Vref 2.4 V, PGA 6) was computed.

Engineering guidance; certification requires the current editions of the standards and an accredited test lab.

## 1. Requirements

- **Bandwidth:** diagnostic 0.05-150 Hz (paediatric up to ~250 Hz commonly); monitoring 0.5 (or 0.67)-40 Hz. (gated: unconfirmed, source is paywalled or blocked) The 0.05 Hz high-pass protects ST-segment fidelity; a higher HP corner needs linear-phase (e.g. bidirectional digital) filtering to avoid ST distortion.
- **Electrode offset:** tolerate ±300 mV DC per lead without saturation. (gated: unconfirmed, source is paywalled or blocked)
- **Input impedance:** ≥ 10 MΩ differential (≥ 2.5 MΩ has been the historical minimum; check edition); higher is better for dry electrodes.
- **Noise:** ≤ ~30 µV p-p referred to input in the diagnostic band. (gated: unconfirmed, source is paywalled or blocked)
- **Standards:** IEC 60601-2-25 (diagnostic) and 2-27 (monitoring) are being consolidated into IEC 80601-2-86 (listed by ISO/IEC as a draft, IEC/DIS, edition 1, in 2026; iso.org returned 403 so the stage is unconfirmed (gated: unconfirmed, source is paywalled or blocked)); confirm which your market and notified body currently recognise.

## 2. Architecture

**Classic analog:** per-lead INA with low gain (5-10) so ±300 mV does not clip → AC coupling (HP corner) → gain stage (×100-500) → anti-alias LPF → ADC.

**Modern integrated AFE (ADS1298-class):** 8-channel, 24-bit delta-sigma, PGA per channel, internal RLD amplifier, Wilson central terminal, lead-off detection, up to tens of kSPS. With 24 bits and Vref ≈ 2.4 V at PGA 6, LSB ≈ 0.05 µV, so DC-couple, digitise the offset and do all filtering digitally. Oversample (e.g. 500 SPS-2 kSPS for diagnostic, higher for pace pulse detection) and decimate.

## 3. Common-mode rejection and right-leg drive

Mains couples ~1-10 V common-mode onto the body. CMRR of the INA (> 100 dB) is degraded by **electrode impedance imbalance** with input capacitance: mismatch of Z_e × C_in converts CM to differential. The standard CMR test inserts an imbalance (51 kΩ ∥ 47 nF) in one lead with mains-frequency CM (the test voltage is set by the particular standard; check it); check the current pass limit in the particular standard.

**Right-leg drive:** sense CM (average of inputs), invert, integrate (gain 10-40 dB, rolled off for stability) and drive the RL electrode. Limit the drive current with series resistance (hundreds of kΩ) so a fault cannot exceed patient auxiliary current limits, and verify loop stability with realistic electrode capacitance. Also shield leads, drive shields at CM, and keep input traces symmetric.

## 4. Input protection (defibrillation-proof)

The applied part must survive ~5 kV defib pulses and pass the energy-reduction test (the ECG may divert only a small fraction of energy; ~10% is commonly cited). (gated: unconfirmed, source is paywalled or blocked)
- Series resistors per lead (~10-50 kΩ total, pulse-rated, physically long or several in series for creepage).
- Gas discharge tubes/neon or high-voltage TVS to isolated ground, then low-leakage clamp diodes to the AFE rails.
- Account for resistor thermal noise (√(4kTR)) and the RC with input capacitance against bandwidth.
- Recovery: the trace must return within the time stated in the particular standard (seconds); fast-restore/AC-coupling reset logic helps.

## 5. Leakage and isolation (IEC 60601-1 ed. 3.x)

| Patient leakage (µA) | NC | SFC |
|---|---|---|
| Type BF | 100 | 500 |
| Type CF | 10 | 50 |
| Mains on applied part | BF 5000, CF 50 | |

Touch current 100/500 µA NC/SFC. ECG for direct cardiac use is CF; general ECG usually BF, both normally defibrillation-proof.

Isolate the patient side from mains *and* from accessible ports (USB, Ethernet) with **2 MOPP**: 4000 V ac test, 8 mm creepage, 5 mm clearance at 250 V working voltage (1 MOPP: 1500 V ac, 4 mm / 2.5 mm). (gated: unconfirmed, source is paywalled or blocked) Use medical-rated isolated DC-DC converters with low isolation capacitance (< ~20 pF to keep leakage and CM pickup low) and reinforced digital isolators. Interface ground of the AFE is a floating "patient ground".

## Gotchas

- Isolation capacitance couples mains into the patient circuit and degrades CMRR; budget it.
- Lead-off DC current sources add offset and noise; pick the lowest that works.
- Pacemaker spikes (0.1-2 ms) need high-rate sampling and must not be filtered into the QRS detector.
- Defib resistors at PCB level need creepage around them too.
- PCB slots under the isolation barrier, not just component ratings, set creepage.

## Verify

- [ ] ±300 mV DC offset applied: no saturation, noise within spec.
- [ ] CMR test with 51 kΩ/47 nF imbalance passes current particular-standard limit.
- [ ] Frequency response meets 0.05-150 Hz (or monitoring band) and ST fidelity test.
- [ ] Defibrillation and energy-reduction tests pass with documented recovery time.
- [ ] Patient leakage measured under NC and SFC within BF/CF limits.
- [ ] Isolation barrier passes 4 kV ac dielectric test; creepage/clearance measured on layout.
