---
id: computing-software.firmware-embedded-development.low-power-design.fuel-gauge-state-of-charge
name: fuel-gauge-state-of-charge
category: computing-software
field: firmware-embedded-development
product: low-power-design
tags: [fuel-gauge, state-of-charge, coulomb-counting, max17048, bq27441, impedance-track, ocv-curve, low-power, firmware-embedded-development]
level: advanced
status: draft
description: "Report battery state of charge accurately: voltage-only vs coulomb counting vs model gauges (MAX17048, BQ27441), learning cycles, configuration and gauge sleep current."
sources:
  - https://www.analog.com/en/products/max17048.html
  - https://www.ti.com/lit/ug/sluuac9a/sluuac9a.pdf
  - https://www.ti.com/lit/an/slua450/slua450.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Fuel gauges and state of charge

## Options
- **Voltage lookup** in firmware (ADC + OCV table): free, but Li-ion OCV is flat between 20-80% and
  load drops voltage, so the reading jumps around. Needs rest-state measurements and filtering.
- **Model-based voltage gauge** (MAX17048/17049 ModelGauge, ~3 uA in hibernate): no sense
  resistor, corrects for load with a cell model; +/-3-5% typical. Good default for small Li-ion.
- **Coulomb counter + model** (TI BQ27441/BQ27220 Impedance Track, MAX17055 ModelGauge m5): sense
  resistor (5-10 mOhm) integrates current, model handles ageing and temperature; +/-1-2%.
- **Primary cells** (alkaline, lithium primary): gauges are not designed for them; use coulomb
  counting from a known full capacity plus a voltage-under-load cutoff.

## Bringing up a MAX17048
- I2C address 0x36. Read `VCELL` (0x02, 78.125 uV/LSB), `SOC` (0x04, 1/256 %), `VERSION` (0x08).
- Set `CONFIG.ATHD` for a low-SOC alert interrupt (ALRT pin) instead of polling.
- Enable hibernate thresholds so it drops to ~3 uA when the load is quiet.
- Loading a custom model for your cell (from Maxim/ADI characterisation) improves accuracy.

## Bringing up a BQ27441
- Configure design capacity, design energy, terminate voltage and taper rate in the data memory
  (unseal `0x8000` twice, `SET_CFGUPDATE`, write block, checksum, `SOFT_RESET`, seal).
- Run a learning cycle: full charge, relax, full discharge to terminate voltage, relax, charge.
  Until then capacity estimates are only the design values.
- Read `StateOfCharge()` (0x1C), `RemainingCapacity()`, `AverageCurrent()`, `StateOfHealth()`.

## Firmware integration
- Show SOC with hysteresis and integer steps; never let it go up while discharging.
- Gate risky operations (OTA, flash erase, motor) on SOC and loaded voltage.
- Gauge registers survive MCU resets but not battery removal; detect `POR` flags and re-configure.
- Temperature: give the gauge a thermistor or the MCU's temperature when the gauge has none.

## Gotchas
- Gauge's own quiescent current (BQ27441 ~ 9 uA sleep, MAX17048 3-23 uA) is part of the budget.
- A sense resistor in the wrong path (charger current bypassing it) breaks coulomb counting.
- Fresh-from-factory gauges ship unconfigured; production must write config per pack.

## Verify
- [ ] Full discharge test: reported SOC tracks measured remaining capacity within spec.
- [ ] SOC is stable (no jumps > 2%) when the load switches on and off.
