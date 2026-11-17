---
id: engineering-technology.biomedical-engineering.biomedical-instrumentation.potentiostat-design
name: potentiostat-design
category: engineering-technology
field: biomedical-engineering
product: biomedical-instrumentation
tags: [potentiostat, biosensor, electrochemical-biosensor, transimpedance-amplifier, three-electrode, cyclic-voltammetry, current-ranging, stability]
level: advanced
status: gated
description: "Design a potentiostat: three-electrode control loop, transimpedance amplifier ranges, compliance, noise and stability with cell capacitance, calibration and safety for biosensors."
sources: ["Bard and Faulkner, Electrochemical Methods: Fundamentals and Applications (instrumentation chapter)", "Horowitz and Hill, The Art of Electronics (transimpedance amplifiers)", "Texas Instruments application notes on potentiostat AFEs (current manufacturer documentation)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Potentiostat design

**Goal:** control the working electrode potential against a reference electrode and measure the resulting current accurately.

## Topology
- **Control amplifier (CA):** drives the counter electrode so that the potential between working (WE) and reference (RE) electrodes equals the setpoint; RE draws almost no current (buffered input).
- **Transimpedance amplifier (TIA):** converts WE current to voltage, Vout = -I x Rf. WE sits at virtual ground (or at a bias).
- **DAC** sets the potential waveform (DC, step, ramp for cyclic voltammetry); **ADC** reads Vout; digital filtering.

## Design decisions
1. **Current range:** from nanoamps (sensors) to milliamps. Choose Rf so full-scale current gives about 1-2 V: Rf = 1 MOhm for 1 microamp, 10 kOhm for 100 microamps. Use switchable Rf for autoranging.
2. **Noise:** Rf thermal noise current = sqrt(4kT/Rf); at 1 MOhm this is 0.13 pA/rtHz, an essential limit for nanoamp sensing. Use low input bias (femtoamp-class) amplifiers, guard rings, clean insulators and shielding; low-frequency 1/f noise and leakage from dirty PCB surfaces dominate in the pA range.
3. **Bandwidth and stability:** the electrochemical cell has capacitance (double layer) at the TIA input, causing instability; add feedback capacitor Cf so that Rf Cf provides a pole and phase margin (typical cutoff from tens of Hz to kHz (gated: unconfirmed, source is paywalled or blocked)). Compensation of the control loop (RC network) avoids oscillation with large cell capacitance.
4. **Compliance voltage:** the CA output must reach the counter electrode potential needed for the current and cell resistance; supply rails of at least a few volts, more for high-resistance cells.
5. **Reference electrode:** high-impedance buffer input; protect from static; avoid leakage from the RE path.
6. **Calibration:** use known resistor dummy cells and an RC dummy cell to check current accuracy and scan fidelity; calibrate gain and offset per range.
7. **Safety and biocompatibility:** limit applied potential and current for in-vivo use; electrode materials chosen for biocompatibility; isolate from mains.

## Verify
- [ ] Dummy cell measurements show gain error and noise within specification at each range.
- [ ] Step response shows stable settling with the maximum cell capacitance.
- [ ] CV of a known redox couple (for example ferricyanide) reproduces literature peak separation.
