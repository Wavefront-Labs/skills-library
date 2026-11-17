---
id: computing-software.firmware-embedded-development.low-power-design.dynamic-voltage-and-frequency-scaling
name: dynamic-voltage-and-frequency-scaling
category: computing-software
field: firmware-embedded-development
product: low-power-design
tags: [power-supply-design, voltage-scaling, dvfs, vos, regulator-range, smps-mode, race-to-sleep, frequency-switching, firmware-embedded-development]
level: advanced
status: draft
description: "Lower MCU active power with core voltage scaling and clock switching: STM32 voltage ranges, flash wait-state ordering, SMPS vs LDO mode, and race-to-sleep vs run-slow."
sources:
  - https://www.st.com/resource/en/application_note/an4621-stm32l4-and-stm32l4-ultralowpower-features-overview-stmicroelectronics.pdf
  - https://www.st.com/resource/en/reference_manual/rm0351-stm32l47xxx-stm32l48xxx-stm32l49xxx-and-stm32l4axxx-advanced-armbased-32bit-mcus-stmicroelectronics.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Dynamic voltage and frequency scaling

**Goal:** run the core at the lowest voltage/frequency that meets the workload, switching
safely between performance levels.

## Dynamic power basics
Dynamic power ~ C x V^2 x f. Halving frequency halves power but doubles run time, so energy
per task is the same; lowering **voltage** is what saves energy per operation. Static
(leakage) power favours finishing quickly and sleeping ("race to sleep").

## STM32L4 example: voltage ranges
| Range | VCORE | Max SYSCLK | Typical |
|---|---|---|---|
| Range 1 | 1.2 V | 80 MHz | ~100 uA/MHz |
| Range 2 | 1.0 V | 26 MHz | ~80 uA/MHz |
| Low-power run | regulator LP mode | 2 MHz | lowest |
L4+, U5, G4 have a "boost" Range 1 for top speed; H7 has VOS0..3. Same pattern everywhere.

## Safe switching order
Going **faster**: raise voltage first, wait for `VOSF` = 0, increase flash wait states, then
raise clock. Going **slower**: lower clock, decrease wait states, then lower voltage.
```c
/* up: Range 2 -> Range 1, 26 -> 80 MHz */
HAL_PWREx_ControlVoltageScaling(PWR_REGULATOR_VOLTAGE_SCALE1);   /* waits for VOSF */
__HAL_FLASH_SET_LATENCY(FLASH_LATENCY_4);
while (__HAL_FLASH_GET_LATENCY() != FLASH_LATENCY_4) { }
/* then switch SYSCLK to PLL at 80 MHz */
```
Wrong order = hard fault or flash read errors on the first instruction after the switch.

## Things that break when the clock changes
- UART baud rates, timer prescalers, SysTick reload: recompute (`SystemCoreClockUpdate()`,
  `HAL_InitTick`, re-init peripherals) or clock peripherals from an independent source (HSI16
  for UART/LPUART, LSE for LPTIM).
- USB requires 48 MHz and typically Range 1.
- ADC max clock and sampling time change with voltage range.
- RTOS tick: re-program the tick timer.

## SMPS vs LDO
Parts with an internal SMPS (STM32U5, L4 "SMPS" variants, nRF52 DC/DC `REG1`) cut active
current 30-50 % vs the LDO but need an external inductor; enable it in firmware
(`NRF_POWER->DCDCEN = 1`, `HAL_PWREx_ConfigSupply(PWR_SMPS_SUPPLY)`). Enabling DC/DC without
the inductor fitted stops the chip.

## Choosing a policy
- Bursty work + deep sleep available: run fast in Range 1, finish, sleep (race to sleep).
- Continuous low workload (e.g. audio filter at 10 % CPU at 80 MHz): run at 8-16 MHz in a
  lower voltage range.
- Measure energy per task with a power analyser for both, the answer varies per chip.

## Verify
- [ ] Each transition stress-tested in a loop for hours without faults.
- [ ] Peripherals keep correct baud/timing after switching (loopback tests).
- [ ] Measured energy per job compared between policies.
