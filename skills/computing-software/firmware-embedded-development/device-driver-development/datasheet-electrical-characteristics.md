---
id: computing-software.firmware-embedded-development.device-driver-development.datasheet-electrical-characteristics
name: datasheet-electrical-characteristics
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [electrical-characteristics, datasheet, min-typ-max, test-conditions, worst-case-design, firmware-embedded-development]
level: practitioner
status: draft
description: "Read datasheet electrical characteristics tables: min/typ/max semantics, test conditions and footnotes, temperature dependence, and designing to worst case instead of typical."
sources:
  - https://www.ti.com/lit/an/szza036c/szza036c.pdf
  - https://www.analog.com/en/resources/technical-articles/understanding-data-sheet-specifications.html
  - https://www.st.com/resource/en/datasheet/stm32l476rg.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Electrical characteristics (min/typ/max)

## What the columns mean
- **Min / Max**: guaranteed limits over the stated conditions, either tested in production or
  "guaranteed by design/characterisation" (a footnote says which). Design to these.
- **Typ**: the median of characterised parts at 25 C and nominal supply. Not guaranteed, often
  absent for exactly the parameter you care about. A design that only works at typical fails on
  some percentage of parts or at temperature extremes.
- **Conditions column**: VDD, temperature range, load, clock frequency, which peripherals are on.
  A sleep current of 1 uA "at 25 C, RTC off" may be 10 uA at 85 C with the RTC on.

## Firmware-relevant parameters and how they bite
| Parameter | Firmware impact |
|---|---|
| GPIO VOH/VOL vs IOH/IOL | driving LEDs or transistor bases: output level sags at high current; total port/package current limits |
| VIH/VIL (often as % of VDD) | interfacing 3.3 V logic to a 1.8 V or 5 V device |
| Internal pull-up range (e.g. 25-55 kOhm) | I2C rise time, button debounce RC |
| HSI/MSI accuracy over temperature (e.g. +-1% 25 C, +-3% full range) | UART baud error, CAN (needs crystal), USB (needs CRS or crystal) |
| ADC: offset, gain, INL/DNL, ENOB, sampling time vs source impedance | real accuracy is far worse than "12-bit" |
| Flash: endurance (cycles) and retention (years) at temperature | logging and EEPROM emulation design |
| Wake-up times from each low-power mode | latency budgets |
| Supply currents per mode and per MHz | battery life model |
| Timing parameters (tSU, tH, tV) for SPI/I2C/FMC | maximum usable bus clock |

## Reading footnotes
Footnotes carry "guaranteed by characterisation, not tested in production", "measured with
pin in analog mode", "excluding I/O switching current", or "at VDD = 3.6 V". Read every footnote
attached to a number you rely on.

## Worst-case analysis practice
- Use min/max across the full temperature and supply range of *your* product.
- Combine tolerances (resistor %, oscillator ppm, ADC error) by worst case, or by RSS when
  justified statistically.
- Record each assumption with the datasheet revision and table number; re-check when the vendor
  revises the datasheet (they do change limits).

## Verify
- [ ] Every critical timing/current/accuracy calculation in the design notes cites min/max, not typ.
- [ ] Product temperature range used in calculations matches the datasheet's conditions column.
