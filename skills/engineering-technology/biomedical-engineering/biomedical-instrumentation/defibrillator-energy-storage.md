---
id: engineering-technology.biomedical-engineering.biomedical-instrumentation.defibrillator-energy-storage
name: defibrillator-energy-storage
category: engineering-technology
field: biomedical-engineering
product: biomedical-instrumentation
tags: [defib-capacitor, defibrillator, electrosurgery, energy-storage, high-voltage-capacitor, flyback-charger, charge-time, iec-60601-2-4]
level: advanced
status: verified
description: "Size defibrillator energy storage and charging: capacitor energy equations, voltage for delivered energy, flyback charger design, charge time targets and safe discharge."
sources: ["IEC 60601-2-4 Particular requirements for the basic safety and essential performance of cardiac defibrillators (confirm edition)", "Webster (ed.), Medical Instrumentation: Application and Design", "Capacitor manufacturer application notes for pulse discharge capacitors"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Defibrillator energy storage and charging

**Goal:** store and deliver the specified energy within charge-time limits while remaining safe for the operator and patient.

Safety-critical; follow IEC 60601-2-4 (confirm edition) and the device's risk file.

## Energy sizing
- Stored energy E = 1/2 C V^2. For a truncated biphasic waveform, the delivered energy is less than the stored energy because the capacitor is not fully discharged and some energy is lost in the circuit; model the delivered energy via the pulse waveform (V(t) across the patient impedance).
- Example for a rough sizing: to store 300 J on a 200 microfarad capacitor needs V = sqrt(2 x 300 / 200e-6) = about 1.7 kV (recomputed: 1732 V). Choose capacitance and voltage to meet delivery to 25-175 ohm loads.
- Capacitor type: high-voltage film or specialised defibrillator capacitors with low ESR and rated for pulse discharge and voltage reversal; derate voltage and consider cycle life.

## Charging
- A **flyback or resonant converter** steps battery voltage up to the capacitor voltage; control by feedback on capacitor voltage and primary current limit; transformer isolation for patient safety.
- **Charge time:** IEC 60601-2-4 sets limits (of the order of 15 seconds to full energy with a fully charged battery, and longer after a number of shocks or from low battery) (gated: unconfirmed, source is paywalled or blocked). Battery chemistry (lithium primary or rechargeable) and its internal resistance at low temperature limit power; size the pack accordingly.
- Hold-off: charging stops at target voltage, monitors leakage and discharge if not delivered within a hold time.

## Safety circuits
- **Dump (internal discharge) path** that safely dissipates stored energy after disarm, power-off or fault, via resistor or the patient circuit isolated; time to a safe voltage specified.
- Redundant voltage monitoring; fault detection of the switching bridge; interlocks; no live voltage at paddles or pads before the shock button.
- Isolation barrier and creepage distances for the voltages involved.

## Verify
- [ ] Delivered energy accuracy across load range with a calibrated analyser.
- [ ] Charge time from a fully charged and from a depleted battery, after repeated shocks.
- [ ] Dump circuit discharge time and failsafe on power loss.
