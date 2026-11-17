---
id: engineering-technology.biomedical-engineering.biomedical-instrumentation.eeg-amplifier-noise
name: eeg-amplifier-noise
category: engineering-technology
field: biomedical-engineering
product: biomedical-instrumentation
tags: [eeg-noise, eeg, eeg-acquisition, noise-budget, input-referred-noise, cmrr, electrode-offset, iso-80601-2-26]
level: advanced
status: gated
description: "Build an EEG amplifier noise budget: thermal and amplifier noise, electrode impedance contribution, bandwidth, CMRR and offset handling to reach sub-microvolt input noise."
sources: ["IEC 80601-2-26 Particular requirements for the basic safety and essential performance of electroencephalographs (confirm edition)", "Webster (ed.), Medical Instrumentation: Application and Design", "Huigen, Peper and Grimbergen, Investigation into the origin of the noise of surface electrodes (Med Biol Eng Comput 2002; confirm citation)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# EEG amplifier noise budget

**Goal:** an input-referred noise well below the 10-100 microvolt EEG signal, in the 0.5-70 Hz band, with realistic electrodes.

## Contributions (RMS, combine as root-sum-square)
1. **Electrode thermal noise:** v = sqrt(4 k T R B). For R = 10 kOhm, B = 100 Hz, T = 300 K: v is about 0.13 microvolts rms. A 50 kOhm electrode gives about 0.29 microvolts.
2. **Amplifier voltage noise:** with e_n = 10 nV/rtHz over 100 Hz, v = 0.1 microvolts rms. Choose instrumentation amplifiers or AFEs with low 1/f corners, since EEG sits at low frequency.
3. **Amplifier current noise:** i_n x R_source; at 1 pA/rtHz and 10 kOhm, 10 nV/rtHz, which adds to the voltage noise.
4. **Electrode and skin noise:** electrode-skin interface noise rises at low frequency; gel Ag/AgCl is lower than dry electrodes.
5. **ADC and reference noise** and quantisation (see biosignal-adc-selection).

Total rms in quadrature; peak-to-peak is about 6.6 times rms for Gaussian noise.

## Target
Many clinical EEG amplifiers specify input noise below about 1 microvolt peak-to-peak (0.1-70 Hz); check the target in the standard and your product requirements. (gated: unconfirmed, source is paywalled or blocked)

## Other design points
- **Input impedance** of 100 MOhm or more and low input capacitance so that electrode impedance mismatch does not reduce CMRR.
- **CMRR** above about 100 dB at mains frequency (gated: unconfirmed, source is paywalled or blocked); use a driven reference (common-mode feedback).
- **DC offset tolerance:** electrode offsets up to hundreds of millivolts; AC-couple or use high-resolution ADCs (24-bit) and digital high-pass filtering.
- **Anti-aliasing** and sampling at 256-1000 Hz or more.
- **Shielding and layout:** short leads, guard, away from digital noise; battery or isolated supply.

## Verify
- [ ] Short the inputs through resistors equal to the electrode impedance and measure noise in band.
- [ ] CMRR test with imbalance, per the standard.
- [ ] Alpha test with eyes open and closed shows clean 8-12 Hz rhythm.
