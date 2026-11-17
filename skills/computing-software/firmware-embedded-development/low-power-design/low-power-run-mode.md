---
id: computing-software.firmware-embedded-development.low-power-design.low-power-run-mode
name: low-power-run-mode
category: computing-software
field: firmware-embedded-development
product: low-power-design
tags: [low-power-run, lprun, msi-clock, voltage-range-2, regulator-low-power, flash-power-down, low-power, firmware-embedded-development]
level: practitioner
status: draft
description: "Run code at microamp-level active current with STM32 Low-power Run: entry conditions (SYSCLK <= 2 MHz, LP regulator), flash power-down, LPSleep, and when it beats sleep."
sources:
  - https://www.st.com/resource/en/reference_manual/rm0351-stm32l47xxx-stm32l48xxx-stm32l49xxx-and-stm32l4axxx-advanced-armbased-32bit-mcus-stmicroelectronics.pdf
  - https://www.st.com/resource/en/application_note/an4621-stm32l4-and-stm32l4-ultralowpower-features-overview-stmicroelectronics.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Low-power run mode

For firmware that must keep running continuously but slowly (polling a slow sensor, counting
pulses in software, running a simple control loop), Low-power Run (LPR) keeps the core executing
with the main regulator off. STM32L4: ~30-100 uA/MHz class figures drop to tens of uA total at
2 MHz.

## Entry conditions (STM32L4/L4+/G0/G4-L style)
1. Reduce SYSCLK to <= 2 MHz (MSI range 0-5, e.g. MSI 2 MHz) and switch off the PLL.
2. Adjust flash latency for the new frequency (0 WS) **after** lowering the clock.
3. Set `PWR_CR1.LPR = 1` (`HAL_PWREx_EnableLowPowerRunMode()`); regulator switches to low-power
   mode. Peripherals limited by the reduced clock.
4. Optionally power down flash in LPR and run from SRAM (`PWR_CR1.FPDR`/`RCC` flash power-down in
   LPSleep), saving another chunk.

Exit: clear LPR, wait for `PWR_SR2.REGLPF = 0`, then raise the clock (voltage range 1 first if going
above 26 MHz on L4: `HAL_PWREx_ControlVoltageScaling(PWR_REGULATOR_VOLTAGE_SCALE1)` and wait VOSF).

## LPSleep
`WFI` while in LPR enters Low-power Sleep: core stopped, peripherals clocked at the low frequency,
wakes on any interrupt with short latency. Useful for UART RX at low baud or ADC sampling with
interrupts, without the Stop-mode clock restore overhead.

## When LPR wins
- Wake-ups more frequent than ~100-1000 per second where each Stop exit/clock restore costs more
  than staying awake slowly.
- Software that must not lose cycles (bit-banged protocol at low speed).
- Otherwise race-to-sleep (fast clock, then Stop 2) usually wins; measure energy per operation.

## Pitfalls
- Raising the clock without first leaving LPR and setting the voltage range causes hard faults or
  flash read errors.
- Peripherals' baud rates and timer prescalers computed for the full-speed clock are wrong in LPR;
  recompute or use LSE-clocked LPUART/LPTIM.
- Debugger connection at 2 MHz SYSCLK requires slow SWD clock.
- Other families differ: STM32U5 has no LPR (uses SMPS and range 4 instead); nRF has no equivalent
  (constant latency vs low-power sub-modes).

## Verify
- [ ] `PWR_SR2.REGLPF = 1` while in LPR; current matches datasheet for the clock.
- [ ] Exit sequence back to full speed survives 10 000 cycles.
