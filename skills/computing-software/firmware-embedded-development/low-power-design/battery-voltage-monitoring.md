---
id: computing-software.firmware-embedded-development.low-power-design.battery-voltage-monitoring
name: battery-voltage-monitoring
category: computing-software
field: firmware-embedded-development
product: low-power-design
tags: [power-supply-design, battery-voltage-monitoring, vbat-adc, resistor-divider, vrefint-vdd, low-battery-threshold, loaded-measurement, firmware-embedded-development]
level: practitioner
status: draft
description: "Measure battery voltage with almost no drain: switched or high-value dividers, VREFINT-based VDD measurement, sampling under load and low-battery thresholds with hysteresis."
sources:
  - https://www.st.com/resource/en/application_note/an2834-how-to-get-the-best-adc-accuracy-in-stm32-microcontrollers-stmicroelectronics.pdf
  - https://docs.nordicsemi.com/bundle/ps_nrf52840/page/saadc.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Battery voltage monitoring

**Goal:** know the battery state well enough to warn and shut down cleanly, without the
measurement circuit draining the battery.

## Circuits
| Method | Drain | Notes |
|---|---|---|
| Always-on divider 100k+100k | 18 uA at 3.6 V | too much for coin-cell/years devices |
| 1M+1M divider + 100 nF cap at ADC pin | 1.8 uA | cap supplies the ADC sampling charge; slow to settle (tau = 50 ms), sample infrequently |
| Switched divider (P-FET or load switch) | ~0 when off | enable, wait settle, sample, disable |
| No divider: battery = VDD | 0 | measure VDD via internal reference (below) |
| Internal VBAT channel (STM32 VBAT/3 or /4 bridge) | only while enabled | disable the bridge after sampling (it drains) |

## Measuring VDD without any pins (battery feeds VDD directly)
Sample the internal reference **VREFINT** with VDDA as the ADC reference; since VREFINT is
known (factory-calibrated value in system memory), solve for VDDA:
```c
uint16_t cal = *VREFINT_CAL_ADDR;          /* measured at 3.0 V (3.3 V on some parts) */
uint32_t vdda_mv = (uint32_t)VREFINT_CAL_VREF * cal / adc_read(ADC_CHANNEL_VREFINT);
```
Use `__HAL_ADC_CALC_VREFANALOG_VOLTAGE` / `__LL_ADC_CALC_VREFANALOG_VOLTAGE`. nRF52: SAADC
input `VDD` (or `VDDHDIV5`) with internal 0.6 V reference and gain 1/6.
This only works while VDD is unregulated battery voltage; behind an LDO you need a divider.

## Measure under load
Battery voltage at rest overestimates remaining capacity; the **loaded** voltage (during radio
TX or motor run) is what browns out the device. Sample both, or sample right after a known
load and use that for low-battery decisions.

## Thresholds
- Convert voltage to state of charge with the chemistry's discharge curve at your load and
  temperature (flat curves like LiFePO4 and Li-SOCl2 give poor SoC resolution from voltage;
  use coulomb counting or a fuel gauge there).
- Use **hysteresis** and averaging (e.g. 8 samples, 3 consecutive readings below threshold) so a
  TX dip doesn't trigger shutdown, and recovery after temperature rise doesn't toggle states.
- Define levels: warn, stop non-essential functions, save state and shut down above BOR.

## Verify
- [ ] Bench supply sweep: reported voltage within +/-2 % across range.
- [ ] Measurement circuit drain measured (switched off) is negligible.
- [ ] Low-battery shutdown happens before BOR resets at the coldest operating temperature.
