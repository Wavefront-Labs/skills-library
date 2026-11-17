---
id: repair-maintenance.reliability-engineering-failure-analysis.vibration-analysis.spectrum-fault-diagnosis-and-alarm-limits
name: spectrum-fault-diagnosis-and-alarm-limits
category: repair-maintenance
field: reliability-engineering-failure-analysis
product: vibration-analysis
tags: [vibration-analysis, condition-monitoring, predictive-maintenance, fft, spectrum, waveform, accelerometer, velocity-rms, iso-20816, iso-10816, unbalance, misalignment, looseness, bearing-defect-frequencies, bpfo, bpfi, bsf, ftf, envelope-analysis, demodulation, gear-mesh, sidebands, field-balancing, alarm-limits, route-based-monitoring]
level: advanced
status: draft
description: "Collect good vibration data, read FFT spectra for unbalance, misalignment, looseness, bearing and gear faults, calculate bearing defect frequencies, and set ISO and statistical alarm limits."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Spectrum fault diagnosis and alarm limits

**Goal:** turn route vibration readings on rotating machines (motors, pumps, fans,
gearboxes) into a diagnosis — which fault, how bad, how urgent — and alarms that
flag change early without crying wolf.

> Draft: rules of thumb below are standard teaching patterns (e.g. Category II/III
> analyst material); real machines combine faults. Confirm with phase, waveform and
> a second technology (oil, thermography) before big decisions.

## 1. Collect data you can trust
- **Sensor:** 100 mV/g ICP accelerometer, **stud or strong flat magnet** on a clean
  flat spot on the bearing housing, as close to the load zone as possible. Handheld
  probes are unrepeatable above ~1 kHz.
- **Points:** each bearing, H/V/A (horizontal, vertical, axial). Mark spots with
  paint or fit mounting pads — same place every time.
- **Settings (typical):** Fmax 40–60× running speed (or ~1 kHz for velocity overall,
  plus a separate high-frequency/envelope measurement); 1600–3200 lines; 2–4 averages;
  Hanning window. Record running speed (strobe/tach) every time.
- Units: **velocity mm/s RMS** for general machine condition (10 Hz–1 kHz);
  **acceleration/envelope (gE)** for early bearing and gear faults.

## 2. Read the spectrum (in orders of running speed, 1× = shaft speed)
| Pattern | Likely fault | Confirm with |
|---|---|---|
| High **1× radial**, little axial, sinusoidal waveform | **Unbalance** | phase H vs V ~90° apart; steady phase |
| High **1× and 2× axial**, 2× often > 1× | **Angular misalignment** | axial phase ~180° across coupling |
| High **2× radial** (and 1×, 3×) | **Parallel misalignment** | radial phase ~180° across coupling |
| Many harmonics 1×–10×, sometimes ½× | **Mechanical looseness** | truncated/erratic waveform; phase unstable |
| Non-synchronous peaks with harmonics, sidebands at 1× | **Rolling bearing defect** | envelope spectrum, defect freq calc |
| Gear mesh (teeth × rpm) with **sidebands** at gear speeds | **Gear wear/eccentricity** | waveform impacts once per rev |
| 2× line frequency (100/120 Hz) | **Electrical** (stator) | disappears instantly when power cut |
| Vane/blade pass (vanes × rpm) high | flow/recirculation, clearance | changes with flow rate |

## 3. Bearing defect frequencies
With n = rolling elements, Bd = ball dia, Pd = pitch dia, θ = contact angle, fr = shaft Hz:
```
BPFO = (n/2) * fr * (1 - (Bd/Pd)*cos θ)     # outer race
BPFI = (n/2) * fr * (1 + (Bd/Pd)*cos θ)     # inner race
BSF  = (Pd/(2*Bd)) * fr * (1 - ((Bd/Pd)*cos θ)**2)   # ball spin
FTF  = (fr/2) * (1 - (Bd/Pd)*cos θ)         # cage
```
Rule of thumb without geometry: BPFO ≈ 0.4·n·fr, BPFI ≈ 0.6·n·fr. Most software
bearing libraries give these by part number.
Signs of progression: envelope peaks at defect frequency → harmonics → sidebands
(BPFI sidebanded by 1× because inner race rotates through the load zone) →
raised noise floor ("haystack") → defect peaks *drop* late-stage as damage smooths out
(don't misread that as improvement).

## 4. Severity and alarm limits
- **ISO 20816-3** (replacing 10816-3) gives zone boundaries for industrial machines
  by size and foundation. Example for medium machines (15–300 kW) on rigid foundations,
  velocity RMS: A/B ≈ 1.4, B/C ≈ 2.8, C/D ≈ 4.5 mm/s. Zone C = restricted operation,
  D = damage likely. Check the table for your machine class.
- **Statistical alarms** once you have ≥ 8–10 readings per point:
  alert = baseline mean + 2σ (or 2–2.5× baseline), danger = mean + 3σ
  (or ~4× baseline / ISO zone D, whichever lower).
- **Trend beats absolute level:** a doubling since last reading is significant even
  in zone B.
- Set narrowband alarms on bearing defect bands and gear mesh, not just overall.

## 5. Field balancing (single plane, quick method)
1. Measure 1× amplitude and phase (O).
2. Add a trial weight Wt at a marked angle; re-measure (O+T).
3. Effect vector T = (O+T) − O. Correction = −O/T × Wt (magnitude and angle).
4. Fit, re-measure, trim. Instruments automate the vector maths.
Confirm it's unbalance first (step 2 table) — balancing a misaligned machine fails.

## Gotchas
- Magnet on a painted curved surface kills high-frequency data.
- Running speed wrong by 2% puts defect frequency labels on the wrong peaks.
- VFD machines: record speed each time; alarms in orders, not Hz.
- One reading is a snapshot; diagnosis needs trend.

## Verify
- [ ] Same mount, point, settings and speed recorded each survey.
- [ ] Diagnosis states the pattern, supporting phase/waveform and confidence.
- [ ] Bearing frequencies calculated for the actual bearing.
- [ ] Alarm limits set (ISO zone + statistical) per point and band.
- [ ] Recommendation has urgency and a re-check date.
