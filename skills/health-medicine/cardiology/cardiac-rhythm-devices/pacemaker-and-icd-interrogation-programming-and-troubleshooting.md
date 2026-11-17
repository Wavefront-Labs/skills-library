---
id: health-medicine.cardiology.cardiac-rhythm-devices.pacemaker-and-icd-interrogation-programming-and-troubleshooting
name: pacemaker-and-icd-interrogation-programming-and-troubleshooting
category: health-medicine
field: cardiology
product: cardiac-rhythm-devices
tags: [cardiology, cardiac-rhythm-devices, cied, pacemaker, icd, implantable-cardioverter-defibrillator, crt-d, crt-p, leadless-pacemaker, s-icd, implantable-loop-recorder, ilr, device-interrogation, pacing-threshold, sensing, lead-impedance, battery-longevity, eri, nbg-code, ddd, vvi, mode-switch, undersensing, oversensing, loss-of-capture, inappropriate-shocks, atp, magnet-response, remote-monitoring, perioperative-cied-management, mri-conditional-device]
level: practitioner
status: draft
description: "Cardiac implantable device follow-up: interrogation routine, thresholds/sensing/impedance, pacing modes, diagnosing under/oversensing, inappropriate shocks, magnets, surgery/MRI, remote monitoring."
sources: [HRS/EHRA expert consensus on CIED follow-up and remote monitoring (2015, 2023 update), HRS expert consensus on perioperative management of CIEDs 2011 and later updates, HRS consensus on MRI and radiation exposure in patients with CIEDs 2017, NASPE/BPEG generic pacemaker code]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Pacemaker and ICD interrogation, programming and troubleshooting

> General clinical/professional reference, not patient-specific advice. Programmer menus, magnet behaviour and MRI conditions are manufacturer- and model-specific; always check the device's documentation.

**Goal:** a device that paces when needed, senses correctly, treats true ventricular
arrhythmias, doesn't shock otherwise, and lasts as long as possible.

## 1. Know the device
- Manufacturer, model, leads (and their ages/recalls), implant date, indication,
  pacing dependence, programmed mode. Patient ID card and records.
- **NBG code:** chamber paced / chamber sensed / response to sensing / rate response
  (e.g. DDDR, VVI, AAI). ICD: tachy zones, therapies (ATP, shock), detection criteria.

## 2. Interrogation routine
1. Presenting rhythm and **underlying rhythm** (carefully reduce rate if not dependent).
2. **Battery:** voltage/longevity estimate; ERI/EOS → replacement planning.
3. **Leads:** pacing **impedance** (typical ~200–1500 Ω; trends matter more than one
   value — sudden fall suggests insulation break, sudden rise fracture), **sensing**
   amplitudes (P and R waves), **capture thresholds** with safety margin
   (commonly 2× voltage or 3× pulse width), high-voltage shock impedance for ICDs.
4. **Events/diagnostics:** stored arrhythmias with electrograms, mode switch episodes
   (AF burden — consider anticoagulation), ventricular high-rate episodes, % pacing
   (high RV pacing → pacing-induced cardiomyopathy risk; **CRT aim ≥ ~98% BiV pacing**).
5. Programme changes, re-interrogate, print/save the final report.

## 3. Troubleshooting
| Problem | ECG/EGM clue | Common causes |
|---|---|---|
| **Loss of capture** | Pacing spike without capture | Rising threshold, lead dislodgement, electrolyte/drug effect, battery depletion |
| **Undersensing** | Spikes in inappropriate places (competing with intrinsic beats) | Low intrinsic signal, sensitivity too low (number too high), lead problem |
| **Oversensing** | Pauses (pacing inhibited); ICD: spurious VF detection | Myopotentials, lead fracture noise, T-wave oversensing, EMI |
| No spike, no output | Pause | Oversensing, battery, connection issue |
| Pacemaker-mediated tachycardia | Tracked fast V pacing at upper rate | Retrograde P waves tracked → extend PVARP/PMT algorithm |

**Inappropriate ICD shocks:** most from AF/SVT with fast ventricular response, T-wave or
noise oversensing, or lead fracture. Review EGMs; adjust discriminators, zones, add
beta-blocker, address lead. A shocked patient needs EGM review the same day; multiple
shocks/storm → urgent admission.

## 4. Magnet response
- Pacemaker: magnet usually triggers **asynchronous pacing** at a magnet rate (rate also
  indicates battery status in some models).
- ICD: magnet typically **suspends tachy detection/therapy** without changing pacing
  (so a pacing-dependent patient may need reprogramming to asynchronous mode for surgery).
- Behaviour varies by manufacturer and can be programmed off — confirm.

## 5. Perioperative and MRI
- Surgery with monopolar diathermy above the umbilicus or near the device: plan for EMI —
  magnet or reprogramming, use bipolar/short bursts, return pad away from device,
  external defibrillation pads on, re-interrogate afterwards when settings were changed.
- **MRI:** only MR Conditional *systems* (generator + leads) under stated conditions; set
  MRI mode, monitor, restore settings after. Abandoned leads/non-conditional systems
  need specialist protocols.

## 6. Remote monitoring
Enrol everyone; it reduces in-person visits and detects lead/battery alerts and AF
earlier. Define who reviews alerts, how fast, and how the patient is contacted.

## Gotchas
- Reading "normal threshold" from one test without checking output safety margin.
- Missing pacing dependence before reprogramming for surgery.
- ICD therapies left off after a procedure.

## Verify
- [ ] Device, leads, indication and dependence documented.
- [ ] Battery, impedance trends, sensing and thresholds with margins recorded.
- [ ] Stored events and EGMs reviewed; AF burden acted on.
- [ ] Peri-procedure plan and post-procedure check completed; therapies re-enabled.
- [ ] Remote monitoring active with alert ownership defined.
