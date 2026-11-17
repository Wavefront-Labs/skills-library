---
id: health-medicine.critical-care-medicine.mechanical-ventilators.ventilator-waveform-and-alarm-troubleshooting
name: ventilator-waveform-and-alarm-troubleshooting
category: health-medicine
field: critical-care-medicine
product: mechanical-ventilators
tags: [mechanical-ventilators, critical-care-medicine, mechanical-ventilation, ventilator-setup, ventilator-waveforms, pressure-time, flow-time, volume-time, patient-ventilator-asynchrony, auto-peep, intrinsic-peep, plateau-pressure, driving-pressure, inspiratory-hold, high-pressure-alarm, low-tidal-volume-alarm, dopes, lung-protective-ventilation, ardsnet, hamilton, drager, servo-u, pb980, pre-use-check]
level: practitioner
status: draft
description: "Set up an ICU ventilator, read pressure/flow/volume waveforms for asynchrony and auto-PEEP, and troubleshoot high-pressure and low-volume alarms with DOPES."
sources:
  - "Tobin MJ (ed), Principles and Practice of Mechanical Ventilation, 3rd ed. (McGraw-Hill)"
  - "Cairo JM, Pilbeam's Mechanical Ventilation: Physiological and Clinical Applications, 7th ed. (Elsevier)"
  - "ARDS Network, Ventilation with lower tidal volumes compared with traditional tidal volumes, N Engl J Med 2000"
  - "Amato MBP et al., Driving pressure and survival in ARDS, N Engl J Med 2015"
  - "Thille AW et al., Patient-ventilator asynchrony during assisted mechanical ventilation, Intensive Care Med 2006"
  - "Manufacturer operator manuals for Hamilton, Draeger Evita/V-series, Getinge Servo and Medtronic Puritan Bennett 980 ventilators"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Ventilator setup, waveform reading and alarm troubleshooting

*General clinical/professional reference, not a substitute for independent clinical judgement, current guidelines, or verified dosing references.*

**Goal:** any ICU ventilator (Hamilton C-series/G5, Dräger Evita/V500, Getinge Servo-i/u,
Medtronic PB980 and similar) checked, configured to lung-protective settings, its
waveforms read for problems before they alarm, and alarms resolved by a fixed sequence.
Mode names differ by vendor (e.g. PRVC, VC+, AutoFlow, APV are all adaptive pressure-
regulated volume modes); learn your device's names, not the brand.

## 1. Pre-use and setup
1. Run the manufacturer **pre-use check/self-test** (leak, compliance, sensor and O2 cell
   calibration) with the actual circuit, humidifier and filter attached. Recalibrate flow
   sensor after changing it.
2. Confirm gas/power supply and battery; bag-valve-mask and suction at bedside.
3. Initial settings (adult, then adjust to gases and mechanics):
   - Tidal volume 6 mL/kg **predicted** body weight (PBW: male 50 + 0.91 × (height cm − 152.4); female 45.5 + 0.91 × (height cm − 152.4)); range 4-8.
   - RR 14-20 (higher in acidosis); PEEP 5-10 (ARDS: PEEP/FiO2 table); FiO2 to SpO2 92-96% (88-95% in ARDS).
   - I:E ~1:2; trigger sensitive but not auto-triggering (flow trigger ~1-3 L/min).
4. Set alarms deliberately: Ppeak ~10 cmH2O above observed, exhaled VT and MV low limits
   ~20-30% below target, apnoea time 20 s.
5. Measure mechanics after a few minutes: inspiratory hold 0.5 s → **plateau ≤ 30** (≤ 28 preferred);
   **driving pressure (Pplat − PEEP) ≤ 15**; expiratory hold → total PEEP.

## 2. Reading waveforms
| Finding | Where | Meaning |
|---|---|---|
| Expiratory flow does not return to zero before next breath | Flow-time | **Auto-PEEP** / air trapping: lower RR, shorten Ti, treat bronchospasm |
| Peak rises, plateau unchanged | Pressure (hold) | Resistance problem: tube kink, secretions, bronchospasm, biting |
| Peak and plateau both rise | Pressure (hold) | Compliance problem: pneumothorax, mainstem intubation, oedema, abdominal pressure |
| Scooped/concave inspiratory pressure in volume control | Pressure-time | **Flow starvation**: increase flow or switch to pressure-targeted mode |
| Patient effort (flow dip, pressure drop) without a breath | Flow/pressure | **Ineffective triggering**, often from auto-PEEP or oversedation/weak effort |
| Two breaths stacked, double VT | Volume/flow | **Double triggering**: Ti too short for neural demand; lengthen Ti or raise VT |
| Breaths without patient effort, oscillating flow | Flow-time | **Auto-triggering**: circuit leak, condensate, cardiac oscillation; desensitise trigger |
| Volume curve does not return to baseline | Volume-time | Leak (cuff, circuit, chest drain air leak) |

## 3. Alarm troubleshooting
- **First rule:** if the patient is unstable and the cause is not obvious in seconds,
  **disconnect and hand-ventilate with 100% O2** (clamp the tube first in high-PEEP or ARDS
  patients if possible). If bagging is easy, the problem is the ventilator/circuit; if hard, it is the patient or tube.
- **DOPES:** **D**isplacement (ETCO2 waveform, tube depth at teeth), **O**bstruction
  (pass suction catheter, kink, biting, secretions), **P**neumothorax (asymmetric chest,
  lung ultrasound no sliding), **E**quipment (circuit, humidifier, O2 supply, valve),
  **S**tacked breaths (auto-PEEP: disconnect briefly to let the chest deflate).
- **Low VT/low MV/low pressure:** leak or disconnection; check cuff pressure (20-30 cmH2O),
  every connection, and that the tube has not migrated into the pharynx.
- **High MV/high RR:** pain, anxiety, acidosis, fever, auto-triggering.

## Gotchas
- Silencing an alarm is not fixing it; reset limits only after a reason is found.
- Heat-and-moisture exchanger plus heated humidifier together causes obstruction: never combine.
- Flow sensors fail with nebulised drugs and condensate; inaccurate VT readings follow.
- Plateau readings need a relaxed patient; active breathing makes them meaningless.
- After switching vendors, check what "PEEP" and "Pinsp" mean: some devices set inspiratory pressure above PEEP, others above zero.

## Verify
- [ ] Pre-use check passed with the actual circuit; result logged.
- [ ] VT based on PBW; plateau and driving pressure measured and within targets.
- [ ] Alarm limits individualised and audible.
- [ ] Waveforms scanned each review for auto-PEEP and asynchrony.
- [ ] Bag-valve-mask, PEEP valve, suction and ETCO2 available at bedside.
