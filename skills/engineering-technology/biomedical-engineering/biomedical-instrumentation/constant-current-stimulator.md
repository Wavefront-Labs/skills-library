---
id: engineering-technology.biomedical-engineering.biomedical-instrumentation.constant-current-stimulator
name: constant-current-stimulator
category: engineering-technology
field: biomedical-engineering
product: biomedical-instrumentation
tags: [constant-current-stimulator, neurostimulation, stimulator-design, howland-current-pump, compliance-voltage, iec-60601-2-10, current-source, stimulation-output-stage]
level: advanced
status: verified
description: "Design a constant-current stimulator output stage: Howland or mirror sources, compliance voltage, accuracy, rise time, protection and monitoring for nerve and muscle stimulation."
sources: ["IEC 60601-2-10 Particular requirements for the basic safety and essential performance of nerve and muscle stimulators (confirm edition)", "Horowitz and Hill, The Art of Electronics (current sources)", "Webster (ed.), Medical Instrumentation"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Constant-current stimulator output stage

**Goal:** deliver a programmed current pulse regardless of electrode and tissue impedance, within safe limits.

Safety-critical; limits and test methods in IEC 60601-2-10 (nerve and muscle stimulators) or the relevant particular standard (confirm edition).

## Why current control
Tissue and electrode impedances vary widely (a few hundred ohms to tens of kilohms) and change with contact; current-controlled stimulation makes the delivered charge predictable.

## Architectures
- **Improved Howland current pump:** op-amp with matched resistors converts a control voltage into a load current; accuracy depends on resistor matching and output impedance; high-voltage op-amps or a discrete output stage extend compliance.
- **Current mirror or transistor source** with DAC-controlled reference, bipolar via H-bridge.
- **Integrated stimulator ASICs** for implants (current DAC and switch matrix).

## Compliance voltage
Required supply = I x R_max + electrode polarisation + headroom. For 10 mA into 5 kOhm: 50 V (I x R, recomputed) plus polarisation and headroom, so a 60-100 V rail may be needed. Higher voltage raises risk and isolation demands; limit maximum current, pulse width and charge.

## Performance
- **Accuracy and linearity** of the current DAC, offset error causing DC (see charge-balanced-waveforms).
- **Output impedance** very high versus load to hold current; check at frequency.
- **Rise and fall time** compatible with pulse widths of 50 microseconds and up.
- **Protection:** current limit, over-voltage clamp, open-circuit detection (compliance reached; alarm), short-circuit tolerance, monitoring of delivered current by a sense resistor, independent hardware limits on amplitude and charge, fail-safe off state.
- **Isolation** of the patient circuit; output capacitor to block DC.

## Test
Use a load box with resistances covering the range (for example 100 ohm to 10 kOhm) and measure waveform fidelity, accuracy and compliance behaviour (including at the open-circuit).

## Verify
- [ ] Current accuracy within spec at all loads and amplitudes.
- [ ] Hardware limits cannot be exceeded by software faults.
- [ ] Waveforms and charge measured for each program.
