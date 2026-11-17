---
id: engineering-technology.technical-authentication-testing.nondestructive-testing.ultrasonic-flaw-detection-and-sizing
name: ultrasonic-flaw-detection-and-sizing
category: engineering-technology
field: technical-authentication-testing
product: nondestructive-testing
tags: [ultrasonic-testing, ut, ndt, nde, pulse-echo, angle-beam, shear-wave, iiw-block, dsc-block, dac, tcg, 6db-drop, flaw-sizing, paut, phased-array, tofd, couplant, weld-inspection, aws-d1-1, asme-section-v, snt-tc-1a, iso-9712, asnt, snells-law, a-scan]
level: practitioner
status: draft
description: "Manual pulse-echo UT of welds and plate: IIW/DSC calibration, DAC/TCG, angle-beam geometry, 6 dB drop sizing, AWS D1.1/ASME V acceptance, with notes on PAUT/TOFD and SNT-TC-1A/ISO 9712."
sources: ["ASME BPVC Section V Article 4 Ultrasonic Examination Methods for Welds", "AWS D1.1 Structural Welding Code - Steel (UT clause)", "ASNT Recommended Practice SNT-TC-1A", "ISO 9712 Non-destructive testing - Qualification and certification of NDT personnel", "ISO 17640 Non-destructive testing of welds - Ultrasonic testing", "ASNT Nondestructive Testing Handbook Vol. 7 Ultrasonic Testing"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Ultrasonic flaw detection and sizing — calibrate, scan, size, accept or reject

**Goal:** find planar and volumetric flaws in welds and plate with contact pulse-echo UT, size them repeatably, and disposition them against the governing code. Engineering guidance only — the procedure, code edition and a certified Level II/III govern.

## 1. Personnel and procedure

Work to a written procedure approved by a Level III. Qualification is employer-based (ASNT SNT-TC-1A, CP-189) or central (ISO 9712, ASNT ACCP). Level II calibrates, examines and evaluates; confirm the code accepts your scheme.

## 2. Physics you use every day

- Velocities in carbon steel: longitudinal ~5920 m/s, shear ~3240 m/s.
- Snell's law: sin(θ1)/V1 = sin(θ2)/V2. Standard refracted shear angles: 45°, 60°, 70°.
- Near field N = D²·f/(4·V). A 10 mm, 5 MHz longitudinal probe in steel: N ≈ 21 mm. Do not size inside the near field.
- Angle-beam geometry for plate thickness T, probe angle θ: depth (first leg) d = S·cosθ, surface distance = S·sinθ; full skip = 2·T·tanθ. Beyond the first leg, depth = 2T − S·cosθ.
- Use 4-5 MHz for fine-grained steel; 1-2.25 MHz for coarse grains and thick sections.

## 3. Calibration

1. **Range/time base:** IIW Type 1 (or V1) block 100 mm radius gives echoes at 100, 200 mm... for shear probes; set the screen to cover at least the full sound path needed (e.g. 1.5 skip).
2. **Probe index (exit) point** at the 100 mm radius maximum; mark it on the wedge.
3. **Refracted angle** from the 1.5 mm hole (IIW) or the DSC block; reject wedges more than ±2° off nominal (check your code's tolerance).
4. **Sensitivity:** build a DAC curve from side-drilled holes at several depths in a reference block of the same material/thickness range (ASME V basic calibration block), or program TCG so the same reflector gives the same screen height (typically 80% FSH) at all depths. AWS D1.1 instead uses the 1.5 mm hole as reference level and an attenuation correction.
5. **Transfer correction:** compare a back-wall/through-transmission signal on the block vs. the part and add the dB difference for surface and attenuation.
6. Verify calibration at the start, every 4 hours or per procedure, at change of operator/probe/cable, and at the end. If it drifted beyond tolerance (commonly 2 dB / 10% DAC), re-examine everything since the last good check.

## 4. Scanning

- Couplant: same type as at calibration; remove scale and spatter.
- Scan sensitivity is reference plus a scanning gain (commonly +6 dB or +14 dB depending on code).
- Overlap passes ≥10% of transducer width; raster perpendicular and parallel (for transverse cracks) to the weld; cover the full weld volume plus HAZ from both sides where accessible.
- Lamination check the scan zone with a 0° probe first so laminations do not mask or mimic weld indications.

## 5. Sizing

- **Length — 6 dB drop:** peak the signal, move along the flaw until the amplitude falls to half (−6 dB); the beam centreline marks the end. Valid when the flaw is larger than the beam; for small flaws use 20 dB drop with a measured beam profile, or record as point.
- **Through-wall height:** tip-diffraction or TOFD (accuracy roughly ±1 mm) beats amplitude methods; amplitude does not equal size for planar flaws with poor orientation.
- **Amplitude rating:** ASME V records indications at ≥20% DAC (typical); AWS D1.1 computes indication rating d = a − b − c (indication dB − reference dB − attenuation factor, c = 2 dB per inch of sound path beyond 1 in). Check the edition and table numbers.

## 6. Acceptance

Apply the construction code, not Section V (which says how to examine). Examples: AWS D1.1 tables by weld class (statically vs. cyclically loaded) using d and length; ASME VIII / B31.3 acceptance by flaw type and length or fracture-mechanics-based tables for UT in lieu of RT. Cracks are typically rejectable regardless of size.

## 7. PAUT and TOFD in brief

PAUT: encoded sectorial/linear scans with a permanent record; calibrate every angle with ACG/TCG. TOFD: accurate height from tip diffraction, but near-surface dead zones need supplementary pulse-echo.

## Gotchas

- Geometry echoes (root, cap, mismatch) look like flaws; plot on a cross-section before calling a defect.
- Temperature changes the wedge velocity and so the angle; calibrate at part temperature.
- Austenitic and dissimilar-metal welds skew and attenuate the beam; use dual-element longitudinal-wave probes and a representative mock-up.

## Verify

- [ ] Procedure, technician certification and code edition are recorded.
- [ ] Angle, index point, range and DAC/TCG were verified before and after the exam.
- [ ] Transfer correction and scanning gain were applied.
- [ ] Full weld volume was covered, including transverse scans.
- [ ] Each indication has location, depth, length, amplitude and code disposition.
