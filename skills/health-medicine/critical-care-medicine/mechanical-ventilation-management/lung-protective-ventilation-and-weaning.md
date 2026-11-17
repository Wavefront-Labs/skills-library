---
id: health-medicine.critical-care-medicine.mechanical-ventilation-management.lung-protective-ventilation-and-weaning
name: lung-protective-ventilation-and-weaning
category: health-medicine
field: critical-care-medicine
product: mechanical-ventilation-management
tags: [mechanical-ventilation-management, critical-care-medicine, mechanical-ventilation, lung-protective-ventilation, low-tidal-volume, predicted-body-weight, plateau-pressure, driving-pressure, peep, ardsnet, peep-fio2-table, ards, berlin-definition, prone-positioning, neuromuscular-blockade, ventilator-weaning, spontaneous-breathing-trial, sbt, rsbi, extubation, volume-control, permissive-hypercapnia]
level: practitioner
status: draft
description: "Set lung-protective ventilation (6 mL/kg PBW, plateau ≤30, PEEP-FiO2 table), escalate for ARDS (prone, NMB), then screen daily and run an SBT to extubation."
sources:
  - "ARDS Network, Ventilation with lower tidal volumes as compared with traditional tidal volumes for acute lung injury and ARDS, NEJM 2000"
  - "ARDS Definition Task Force, Acute respiratory distress syndrome: the Berlin Definition, JAMA 2012"
  - "Guérin et al., Prone positioning in severe ARDS (PROSEVA), NEJM 2013"
  - "Amato et al., Driving pressure and survival in ARDS, NEJM 2015"
  - "ATS/ESICM/SCCM, Mechanical ventilation in adult patients with ARDS clinical practice guideline (2017) and 2024 update"
  - "ACCP/ATS, Liberation from mechanical ventilation in critically ill adults guideline (2017)"
  - "Tobin, Principles and Practice of Mechanical Ventilation (McGraw-Hill)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Lung-protective ventilation and weaning to extubation

*General clinical/professional reference, not a substitute for independent clinical judgement, current guidelines, or verified dosing references.*

**Goal:** ventilate every intubated patient with lung-protective settings from the first hour, escalate systematically if ARDS is severe, and liberate the patient from the ventilator as soon as they pass a daily screen and spontaneous breathing trial.

## 1. Initial settings (volume control, assist-control)
1. **Calculate predicted body weight (PBW)** from height, never actual weight: male 50 + 0.91 × (height cm − 152.4); female 45.5 + 0.91 × (height cm − 152.4).
2. **Tidal volume 6 mL/kg PBW** (range 4-8; start at 8 and reduce to 6 within hours if starting higher).
3. **Rate 16-30/min** to meet minute ventilation; check for auto-PEEP at high rates.
4. **PEEP 5-8 cmH2O** initially, then titrate with FiO2 to target **SpO2 88-95% / PaO2 55-80 mmHg** (ARDSnet; many units now target 92-96% outside ARDS — verify locally).
5. **Measure after every change:** plateau pressure (0.5 s inspiratory hold) **≤30 cmH2O**; driving pressure (plateau − PEEP) ideally **≤15 cmH2O**.
6. **Accept permissive hypercapnia:** pH ≥7.20-7.25 is generally tolerated (avoid in raised ICP or severe pulmonary hypertension).

## 2. Recognise and stage ARDS (Berlin)
Onset within 1 week, bilateral opacities not fully explained otherwise, not primarily cardiac, with PEEP ≥5: P/F 200-300 mild, 100-200 moderate, ≤100 severe. (The 2023 global definition adds SpO2/FiO2 and non-intubated patients — check which your unit uses.)

## 3. Escalation ladder for refractory hypoxaemia
| Step | Trigger (typical) | Action |
|---|---|---|
| 1 | Any ARDS | 6 mL/kg PBW, plateau ≤30, conservative fluids once shock resolved |
| 2 | FiO2 >0.6 | Higher-PEEP table (ARDSnet low or high PEEP-FiO2 table); assess recruitability |
| 3 | P/F <150 on FiO2 ≥0.6, PEEP ≥5 | **Prone ≥16 h/day** (PROSEVA); start early, within 12-24 h |
| 4 | Severe dyssynchrony or P/F <150 early | Neuromuscular blockade, e.g. cisatracurium infusion ≤48 h (mixed trial evidence; not routine) |
| 5 | P/F <80 for >6 h or pH <7.25 with PaCO2 >60 for >6 h despite above | Refer for VV-ECMO (EOLIA criteria) |

Avoid routine high-frequency oscillation and prolonged high-pressure recruitment manoeuvres (harm signals in OSCILLATE and ART).

## 4. Daily liberation screen (every morning)
All of: underlying cause improving; FiO2 ≤0.4-0.5 and PEEP ≤8; haemodynamically stable on no or low-dose vasopressor; able to initiate breaths; RASS -1 to +1 after a spontaneous awakening trial (see the sedation skill `health-medicine.critical-care-medicine.sedation-analgesia-and-delirium.analgesia-first-sedation-and-delirium-bundle`).

## 5. Spontaneous breathing trial
- **30-120 min** on pressure support 5-8 cmH2O with PEEP ≤5, or a T-piece.
- **Fail if:** RR >35 sustained, SpO2 <90%, HR >140 or ±20% change, SBP >180 or <90, agitation, diaphoresis, accessory-muscle use.
- **RSBI** (RR / VT in litres) <105 supports success but should not replace the trial.
- **Before extubation check:** cough strength, secretion volume/suction frequency, GCS, and a cuff leak test in high-risk airways (leak <110 mL or <10-25% of VT suggests laryngeal oedema; consider steroids ≥4 h before).
- **High-risk patients** (age >65, heart failure, COPD, failed prior SBT): extubate to NIV or high-flow nasal oxygen.
- Failure of extubation within 48-72 h: reintubate early rather than persisting with rescue NIV.

## Gotchas
- Tall men and short women are the classic overdose cases when actual weight is used.
- Plateau ≤30 can still be injurious if driving pressure is high; with obesity or abdominal hypertension, oesophageal pressure helps separate chest-wall from lung stiffness.
- High PEEP can drop cardiac output; watch MAP after every PEEP increase.
- A failed SBT means find the reason (fluid overload, weakness, ischaemia, secretions, sedation), fix it and retry next day; do not repeat SBTs hourly.

## Verify
- [ ] PBW and VT/kg documented; VT ≤8 mL/kg PBW.
- [ ] Plateau and driving pressure measured and recorded after each change.
- [ ] ARDS severity staged; prone considered when P/F <150.
- [ ] Daily SAT/SBT screen done and outcome recorded.
- [ ] Post-extubation support plan for high-risk patients.
