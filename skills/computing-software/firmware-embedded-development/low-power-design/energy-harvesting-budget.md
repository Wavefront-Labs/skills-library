---
id: computing-software.firmware-embedded-development.low-power-design.energy-harvesting-budget
name: energy-harvesting-budget
category: computing-software
field: firmware-embedded-development
product: low-power-design
tags: [energy-harvesting, power-budget, indoor-solar, supercapacitor, mppt, cold-start, energy-aware-scheduling, bq25570, batteryless, firmware-embedded-development]
level: advanced
status: draft
description: "Budget a solar/thermal/vibration energy-harvesting device: harvest estimates, storage sizing for dark periods, PMIC cold start and thresholds, leakage, and energy-aware firmware duty cycling."
sources:
  - https://www.ti.com/lit/ds/symlink/bq25570.pdf
  - https://www.analog.com/en/products/adp5091.html
  - https://e-peas.com/product/aem10941/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Energy harvesting budgets

**Goal:** a device that runs indefinitely from harvested energy, including through the worst
realistic dark/idle period, with firmware that degrades gracefully instead of brown-out looping.

## 1. Harvest estimate (worst realistic case, not datasheet peak)
| Source | Typical available |
|---|---|
| Indoor PV (amorphous), 200-500 lux office | ~5-20 µW/cm² |
| Outdoor PV, full sun | ~10 mW/cm² (cloudy: 10x less) |
| Thermoelectric, ΔT 5-10 K | tens of µW/cm² |
| Vibration (machine) | µW to low mW, very site-specific |
Multiply by PMIC efficiency (boost/MPPT 50-90 % depending on input voltage and power level;
efficiency collapses at µW inputs) and by the fraction of time the source is present
(office lights ~10 h/day, 5 days/week).

## 2. Load energy per day
Integrate the measured current profile (see `current-profiling-and-duty-cycle-budget`):
sleep current × 24 h + Σ(event charge × events/day). Include **leakage**: storage self-discharge
(supercaps µA-level, LiC and thin-film batteries less), PMIC quiescent current (bq25570 ~0.5 µA),
and divider resistors on monitored voltages.

## 3. Balance
`E_harvest_per_day >= E_load_per_day × margin (1.5-2)` averaged over the design period (a
week for indoor lighting cycles).

## 4. Storage for autonomy
`E_store = 0.5 × C × (V_max² − V_min²)` for capacitors; V_min = the PMIC/load cutoff, not 0.
Size for the longest dark period (weekend, night, winter) at the reduced-activity load.
Supercaps: cheap, unlimited cycles, high leakage at large C. LiC/LiPo/thin-film: more energy,
charge temperature limits, need PMIC protection thresholds set correctly.

## 5. PMIC configuration
- **Cold start**: from an empty store the harvester must bring it up through an inefficient
  cold-start circuit (bq25570 needs ~330 mV/15 µW minimum input to cold start). Test it.
- **Thresholds**: VBAT_OV (max storage), VBAT_OK hysteresis (load enabled above OK_HYST, cut
  below OK) - set them so the MCU only starts with enough energy to complete its boot plus one
  task; otherwise it brown-out loops forever.
- MPPT setting matched to the source (e.g. 80 % Voc for PV).

## 6. Energy-aware firmware
- Read storage voltage (PMIC VBAT_OK pin, ADC with switched divider) before each energy-costly
  action; skip or defer radio transmissions when low.
- Adaptive duty cycle: reporting interval as a function of stored energy.
- Persist critical state before energy runs out (low-voltage interrupt / comparator).
- Boot fast and cheap: avoid long clock-start or calibration routines at every wake.

## Verify
- [ ] Bench test with a programmable light source at the worst-case lux for a week: storage
      voltage trends flat or up.
- [ ] Cold start from 0 V storage at minimum light succeeds.
- [ ] Device recovers cleanly after full depletion.
