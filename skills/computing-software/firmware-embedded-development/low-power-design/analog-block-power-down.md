---
id: computing-software.firmware-embedded-development.low-power-design.analog-block-power-down
name: analog-block-power-down
category: computing-software
field: firmware-embedded-development
product: low-power-design
tags: [analog-power-down, adc-deep-power-down, vrefbuf, comparator-power, opamp-power, temperature-sensor-disable, bor-pvd-current, low-power, firmware-embedded-development]
level: practitioner
status: draft
description: "Switch off analog blocks that stay powered in sleep: ADC regulator and deep power-down, VREFBUF, comparators, op-amps, temperature sensor, PVD/BOR, external analog."
sources:
  - https://www.st.com/resource/en/application_note/an4621-stm32l4-and-stm32l4-ultralowpower-features-overview-stmicroelectronics.pdf
  - https://docs.nordicsemi.com/bundle/ps_nrf52840/page/saadc.html
  - https://www.st.com/resource/en/datasheet/stm32l476rg.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Powering down analog blocks

Digital clock gating does not switch off analog bias currents. These blocks keep drawing tens to
hundreds of microamps in Stop unless disabled explicitly.

## Usual suspects (STM32L4 figures, check your datasheet)
| Block | Typical current when left on | Off switch |
|---|---|---|
| ADC internal regulator | ~100-200 uA | `ADC_CR.ADVREGEN=0`, then `DEEPPWD=1` |
| VREFBUF | ~15-20 uA | `VREFBUF_CSR.ENVR=0` (and HIZ if external VREF) |
| Temperature sensor / VREFINT channels | few uA | `ADC_CCR.TSEN=0`, `VREFEN=0` |
| COMP (high-speed mode) | 5-10 uA (0.5 uA ultra-low-power mode) | disable or `PWRMODE` low |
| OPAMP | ~100 uA (normal), ~30 uA (low-power) | `OPAMP_CSR.OPAEN=0` |
| DAC | ~200-400 uA per channel with buffer | disable, or buffer off / sample-and-hold |
| PVD / BOR level > 0 | ~0.3-1 uA | configure only as needed |
| USB PHY, LSE CSS, HSI48 | varies | disable when unused |

nRF52 SAADC: stop it with `TASKS_STOP` and disable (`ENABLE=0`); leaving it enabled after a
calibration costs hundreds of uA. Use `nrfx_saadc` uninit between bursts.

## Procedure
1. Measure Stop-mode current with all analog explicitly off: that is your floor.
2. Enable each analog block one at a time and measure the delta; build a table for your board.
3. In firmware, wrap analog usage: power up, wait for startup time (ADC regulator 20 us on L4,
   VREFBUF settling, op-amp startup), use, power down.
4. Re-calibrate the ADC after deep power-down (`ADCAL`) if accuracy matters; calibration data is
   lost in DEEPPWD on some families, keep a copy and rewrite it to save time.

## External analog parts
Resistor dividers for battery measurement (switch them with a MOSFET or use 1-10 MOhm with a
sampling capacitor), sensor bias, microphone preamps, LED drivers' references: put them behind
load switches or use parts with shutdown pins.

## Gotchas
- HAL `HAL_ADC_DeInit` does not always set DEEPPWD; check registers after deinit.
- Pins left in analog mode are the lowest-leakage GPIO state; switching ADC pins to analog mode
  after use is correct, the ADC itself must still be off.

## Verify
- [ ] Per-block current deltas measured and documented.
- [ ] Register dump before sleep shows all analog enables cleared.
