---
id: health-medicine.critical-care-medicine.icu-monitoring-systems.invasive-pressure-and-cardiac-output-monitoring
name: invasive-pressure-and-cardiac-output-monitoring
category: health-medicine
field: critical-care-medicine
product: icu-monitoring-systems
tags: [icu-monitoring-systems, critical-care-medicine, hemodynamic-monitoring, arterial-line, invasive-blood-pressure, transducer, phlebostatic-axis, zeroing, levelling, square-wave-test, fast-flush-test, damping, cvp, cardiac-output, flotrac, picco, transpulmonary-thermodilution, pulse-contour-analysis, pulmonary-artery-catheter, pulse-pressure-variation, alarm-fatigue, philips-intellivue, ge-carescape]
level: practitioner
status: draft
description: "Set up, level, zero and square-wave test arterial/CVP transducers, validate cardiac-output devices (FloTrac, PiCCO, PAC) and tune ICU alarm limits to cut alarm fatigue."
sources:
  - "Cecconi M et al., Consensus on circulatory shock and hemodynamic monitoring (ESICM task force), Intensive Care Med 2014"
  - "Gardner RM, Direct blood pressure measurement - dynamic response requirements, Anesthesiology 1981"
  - "Saugel B et al., Cardiac output estimation using pulse wave analysis - physiology, algorithms, and technologies, Crit Care 2021"
  - "Michard F, Changes in arterial pressure during mechanical ventilation, Anesthesiology 2005"
  - "AACN Practice Alert, Managing Alarms in Acute Care Across the Life Span"
  - "The Joint Commission, National Patient Safety Goal NPSG.06.01.01 on clinical alarm safety"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Invasive pressure and cardiac-output monitoring

*General clinical/professional reference, not a substitute for independent clinical judgement, current guidelines, or verified dosing references.*

**Goal:** numbers on the bedside monitor (Philips IntelliVue, GE CARESCAPE, Dräger Infinity,
Mindray and similar) that are physiologically true, cardiac-output figures whose limits you
understand, and alarms that fire for real events rather than artefact. Menu paths differ by
vendor; the physics does not.

## 1. Transducer setup
1. Pressure bag inflated to **300 mmHg** with 0.9% saline (heparin per local policy) for
   ~3 mL/h continuous flush. Prime the line with no air bubbles — bubbles overdamp and
   resonate.
2. Use stiff, short tubing (ideally ≤ 120 cm total) with few stopcocks.
3. **Level** the air-fluid interface at the **phlebostatic axis** (4th intercostal space,
   mid-axillary line, approximating the right atrium) for arterial and CVP. Neurosurgical
   patients: some units level the arterial transducer at the tragus for cerebral perfusion (verify local protocol).
   Each 10 cm level error ≈ 7.5 mmHg error.
4. **Zero:** open the transducer to air, press zero on the monitor; repeat after moving,
   re-levelling, at start of each shift, and whenever values look implausible.

## 2. Square-wave (fast-flush) test
Pull the flush tab for ~1 s and release. Read the oscillations:
| Result | Appearance | Effect |
|---|---|---|
| Optimal | 1.5-2 oscillations before returning to baseline | Accurate |
| Overdamped | < 1 oscillation, slurred upstroke, lost dicrotic notch | SBP under-read, DBP over-read |
| Underdamped | > 3 oscillations, spiky systolic peak | SBP over-read |
Fix overdamping: remove air, clot (aspirate, do not flush clot forward), kinks, loose
connections, soft tubing. Fix underdamping: shorten tubing, remove extra stopcocks, add a
damping device. **MAP is the most robust value** even when damping is imperfect.

## 3. Cardiac-output devices
| Device class | Example | Calibration | Use and limits |
|---|---|---|---|
| Uncalibrated pulse contour | FloTrac/Acumen (Edwards), ProAQT, LiDCO rapid | None (demographic algorithm) | Trends; unreliable with severe vasoplegia, arrhythmia, IABP, poor waveform |
| Calibrated pulse contour + TPTD | PiCCO (Getinge), VolumeView/EV1000 | Transpulmonary thermodilution: 3 cold boluses (15-20 mL, < 8 °C) via CVC, femoral thermistor line | CO, GEDVI, EVLWI, PVPI; recalibrate every ~8 h and after major changes |
| Pulmonary artery catheter | Swan-Ganz, continuous CO | Thermodilution | RV/PA pressures, PAOP, SvO2; consider for RV failure, pulmonary hypertension, complex shock |
| Non-invasive | Oesophageal Doppler, bioreactance, echo | — | Spot checks and trends |
- **Fluid responsiveness:** PPV/SVV > 12-13% suggests responsiveness only if fully ventilated,
  VT ≥ 8 mL/kg, sinus rhythm, closed chest. Otherwise use passive leg raise with a real-time
  CO measurement (≥ 10% rise) or a mini-fluid challenge.
- Check device numbers against the patient: a CO of 9 L/min with mottled skin and lactate 6 is a measurement problem until proven otherwise.

## 4. Alarm configuration and trending
- Review unit default profiles; then **individualise** limits at admission and each shift
  (e.g. MAP low limit 5 mmHg below the target MAP rather than an arbitrary default).
- Add short delays (e.g. 10-15 s for SpO2) where the vendor supports it to suppress transient artefact.
- Replace ECG electrodes daily and after sweating; good skin prep cuts false arrhythmia alarms.
- Escalate priorities correctly: life-threatening (asystole, VF/VT, apnoea) never silenced or delayed.
- Use trend screens (6-24 h) at handover; event review on the central station for arrhythmias.

## Gotchas
- Zeroing ≠ levelling: a monitor zeroed with the transducer on the floor is still wrong.
- Femoral vs radial arterial pressure differ in vasoplegia (radial under-reads); compare sites if doubt.
- Inadvertent arterial injection risk: label arterial lines clearly, never inject.
- CVP is a poor predictor of fluid responsiveness; trend it, do not chase a target.
- Alarm fatigue is a patient-safety hazard: most ICU alarms are non-actionable.

## Verify
- [ ] Transducer at phlebostatic axis, zeroed, time documented.
- [ ] Square-wave test optimal (or damping corrected) before acting on SBP.
- [ ] Cardiac-output device calibrated per its type; values plausible against clinical picture.
- [ ] Alarm limits individualised and reviewed each shift; critical alarms never disabled.
