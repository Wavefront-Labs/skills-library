---
id: engineering-technology.biomedical-engineering.medical-imaging-systems.acoustic-output-safety
name: acoustic-output-safety
category: engineering-technology
field: biomedical-engineering
product: medical-imaging-systems
tags: [mechanical-index, ultrasound-transducer, piezoelectric, thermal-index, acoustic-output, alara, hydrophone, iec-62359, fda-ultrasound-limits]
level: advanced
status: gated
description: "Verify diagnostic ultrasound acoustic output: mechanical index, thermal indices, intensity limits, ALARA, display requirements and measurement with a hydrophone per IEC 62359."
sources: ["IEC 62359 Ultrasonics - Field characterization - Test methods for the determination of thermal and mechanical indices related to medical diagnostic ultrasonic fields (confirm edition)", "IEC 60601-2-37 Particular requirements for ultrasonic medical diagnostic and monitoring equipment (confirm edition)", "FDA, Marketing Clearance of Diagnostic Ultrasound Systems and Transducers (guidance; confirm current text)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Acoustic output and mechanical index

**Goal:** keep diagnostic ultrasound output within accepted safety limits and display indices to users.

Safety-critical; limits come from FDA guidance and IEC standards in your market, and may change (confirm).

## Indices
- **Mechanical index (MI)** = peak rarefactional pressure p_r (MPa, derated by 0.3 dB/cm/MHz attenuation to the focus (gated: unconfirmed, source is paywalled or blocked)) divided by the square root of the centre frequency (MHz). It relates to cavitation risk.
- **Thermal indices:** TIS (soft tissue), TIB (bone near focus), TIC (cranial bone) estimate the ratio of the transmitted power to the power needed to raise tissue temperature by 1 degree Celsius (gated: unconfirmed, source is paywalled or blocked).
- **Intensities:** spatial-peak temporal-average (Ispta.3) and spatial-peak pulse-average (Isppa.3), derated.

## Limits (FDA, Marketing Clearance of Diagnostic Ultrasound Systems and Transducers, issued 21 Feb 2023, Track 3; confirmed in the guidance text)
- General (non-ophthalmic): Ispta.3 up to 720 mW/cm2, Isppa.3 up to 190 W/cm2 or MI up to 1.9.
- Ophthalmic: Ispta.3 up to 50 mW/cm2, TI = max(TIS_as, TIC) up to 1, MI up to 0.23. Track 1 (no output display) uses application-specific limits instead, for example cardiac Ispta.3 94 mW/cm2 and fetal imaging and other 17 mW/cm2, both with Isppa.3 190 W/cm2 or MI 1.9, and ophthalmic 17 mW/cm2 with Isppa.3 28 W/cm2 or MI 0.23.
- Systems must **display** MI and TI when they can exceed 1.0 (the FDA guidance treats a system that cannot exceed TI 1.0 or MI 1.0 in any mode differently, reporting global maxima only; exact IEC 60601-2-37 display rules (gated: unconfirmed, source is paywalled or blocked)), so that the user can follow ALARA (as low as reasonably achievable).

## Measurement
1. Use a calibrated hydrophone (PVDF membrane or needle) in a water tank with a positioning system; measure the acoustic pressure waveform at the focus and in the field for each transducer, mode, depth, and focus setting.
2. Determine p_r, centre frequency, pulse intensity integral, and beam dimensions; compute MI, TI and intensities per IEC 62359, with derating.
3. Test worst-case settings (maximum output, mode combinations, Doppler, harmonic modes).
4. Compare the displayed indices to measured values (display accuracy within the standard's tolerance).

## Design controls
- Hardware limits on transmit voltage, power-on defaults, output control by mode and preset, and software checks that the displayed index follows actual drive.
- Higher output in neonatal and obstetric presets is limited.

## Verify
- [ ] Hydrophone calibration traceable and uncertainty budget calculated.
- [ ] Output across all combinations remains within limits or flagged by index display.
- [ ] Thermal behaviour of the transducer surface temperature tested (IEC 60601-2-37 limits (gated: unconfirmed, source is paywalled or blocked)).
