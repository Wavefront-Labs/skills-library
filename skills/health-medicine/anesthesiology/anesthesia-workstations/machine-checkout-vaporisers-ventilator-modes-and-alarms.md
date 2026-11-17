---
id: health-medicine.anesthesiology.anesthesia-workstations.machine-checkout-vaporisers-ventilator-modes-and-alarms
name: machine-checkout-vaporisers-ventilator-modes-and-alarms
category: health-medicine
field: anesthesiology
product: anesthesia-workstations
tags: [anesthesiology, anesthesia-workstations, anaesthetic-machine, anesthesia-machine, machine-check, preanesthesia-checkout, aagbi-checklist, leak-test, circle-system, co2-absorbent, soda-lime, vaporiser, vaporizer, desflurane-vaporiser, fresh-gas-flow, low-flow-anaesthesia, ventilator-modes, volume-control, pressure-control, pcv-vg, psv, alarm-limits, oxygen-failure-alarm, backup-oxygen-cylinder, self-inflating-bag, gas-analysis, draeger, ge-aisys]
level: practitioner
status: draft
description: "Anaesthesia workstation use: daily and pre-case checks, circle leaks and absorbent, vaporiser filling and safety, low-flow technique, ventilator modes, alarm limits and gas-supply failure."
sources: [Association of Anaesthetists checking anaesthetic equipment 2019, ASA recommendations for pre-anesthesia checkout procedures 2008 (and current revisions), vendor operator manuals for anesthesia workstations (Draeger, GE) - generic features only]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Machine checkout, vaporisers, ventilator modes and alarms

> General clinical/professional reference, not a substitute for the manufacturer's operator manual, the institution's checklist or biomedical engineering advice. Features and menu names differ by model.

**Goal:** a machine that can't hypoxically or unexpectedly fail you, and settings you
understand well enough to fix fast.

## 1. Checks
**Start of day (full check)** per national checklist and the machine self-test:
- Power and battery; gas pipelines connected by tug test, pressures normal;
  **backup O2 cylinder** present and adequately full, closed after checking.
- Self-test/automated leak and compliance check passed; review any failures before use.
- Vaporisers: seated and locked, filled, filler closed, one-at-a-time interlock working.
- Breathing system: correct, connections tight, **manual leak test** (occlude patient
  end, pressurise to ~30 cmH2O, pressure holds), APL valve works, two-bag test for
  valve function where relevant.
- CO2 absorbent colour and age; gas analyser calibrated, sampling line connected.
- Alternative oxygenation: **self-inflating bag** in the room.
- Suction working; scavenging connected.
**Before each case:** breathing circuit and filter changed per policy, quick leak test,
monitoring and alarm limits set, vaporiser levels, suction.

## 2. Circle system and absorbent
- CO2 absorption allows rebreathing → **low-flow anaesthesia** saves agent and reduces
  emissions (and environmental impact — desflurane and nitrous oxide are potent
  greenhouse gases; many departments now remove desflurane).
- Rising inspired CO2 (FiCO2 > 0) means exhausted absorbent or a sticking valve —
  change absorbent; check unidirectional valves.
- **Desiccated absorbent** (left with high fresh gas flow over a weekend) can produce
  CO with some agents and heat; turn off gas flows when idle.

## 3. Vaporisers
- Agent-specific; key-filled or Easy-Fil; never fill with the wrong agent.
- Variable-bypass vaporisers are temperature/flow compensated; desflurane vaporisers
  are heated and electronically controlled.
- At low fresh gas flows, the inspired concentration lags the dial — use end-tidal
  agent readings (or end-tidal control modes where available).
- Tipping a vaporiser can cause dangerous output; follow manufacturer instructions.

## 4. Ventilator modes
| Mode | Set | Watch |
|---|---|---|
| Volume control (VCV) | VT, rate, I:E/Ti, PEEP | Peak/plateau pressure |
| Pressure control (PCV) | Inspiratory pressure, rate, Ti, PEEP | VT (changes with compliance) |
| PCV-VG / PRVC | Target VT delivered by adaptive pressure | Pressure limit |
| Pressure support (PSV) | Support level, PEEP, trigger | Apnoea backup set |
| SIMV | Mandatory breaths + support | Matched to patient effort |
Lung-protective defaults: VT 6–8 mL/kg predicted body weight, PEEP ≥ 5.
Fresh gas decoupling and compliance compensation vary by model — know yours.

## 5. Alarms
- Set limits to the patient (not factory defaults): ETCO2 high/low, SpO2, FiO2 low,
  airway pressure high/low (low = disconnection), minute volume, agent concentration
  high/low, apnoea.
- Never silence and walk away; avoid alarm fatigue by setting meaningful limits.

## 6. Failures
- **Oxygen pipeline failure:** alarm sounds; open the backup cylinder, reduce flow,
  move to low-flow, switch to TIVA if needed, call engineering.
- Total machine/power failure: self-inflating bag with oxygen cylinder, TIVA, hand
  ventilate, battery monitoring.
- Unexplained high airway pressure: disconnect at the patient and hand-ventilate to
  separate patient from machine causes.

## Gotchas
- Leaving the APL valve closed during manual ventilation → barotrauma.
- Gas sampling line disconnected → false apnoea or missed hypercarbia.
- Assuming the self-test covers external components (it often doesn't check the
  patient-end circuit you just attached).

## Verify
- [ ] Daily check logged; self-test passed; backup cylinder and self-inflating bag present.
- [ ] Pre-case leak test done after circuit change.
- [ ] Vaporisers seated, filled and interlocked.
- [ ] Alarm limits patient-appropriate before induction.
- [ ] Low-flow technique used where safe; desiccated absorbent avoided.
