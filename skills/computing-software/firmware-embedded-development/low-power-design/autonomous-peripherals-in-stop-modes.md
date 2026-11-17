---
id: computing-software.firmware-embedded-development.low-power-design.autonomous-peripherals-in-stop-modes
name: autonomous-peripherals-in-stop-modes
category: computing-software
field: firmware-embedded-development
product: low-power-design
tags: [autonomous-peripheral, lpbam, ppi, dppi, event-system, peripheral-reflex-system, stop-mode-dma, low-power, firmware-embedded-development]
level: advanced
status: draft
description: "Let peripherals work while the CPU sleeps: STM32U5 LPBAM and autonomous mode, nRF PPI/DPPI, SAM Event System, EFM32 PRS: timer-triggered ADC + DMA without waking the core."
sources:
  - https://www.st.com/resource/en/application_note/an5645-stm32u5-series-lowpower-background-autonomous-mode-lpbam-stmicroelectronics.pdf
  - https://docs.nordicsemi.com/bundle/ps_nrf5340/page/dppi.html
  - https://ww1.microchip.com/downloads/en/DeviceDoc/SAM-D21DA1-Family-Data-Sheet-DS40001882G.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Autonomous peripherals in stop modes

**Idea:** waking the CPU costs wake-up time, clock restore and active current. If a peripheral can
trigger another and DMA can move the result, the CPU only wakes when a buffer is full or a threshold
is crossed.

## Mechanisms by vendor
- **Nordic PPI/DPPI:** connect any peripheral EVENT to any TASK in hardware.
  `NRF_TIMER->EVENTS_COMPARE[0]` -> `NRF_SAADC->TASKS_SAMPLE`, SAADC EasyDMA fills a buffer, CPU
  wakes on `EVENTS_END`. nrfx: `nrfx_gppi_channel_endpoints_setup()`.
- **STM32U5/H5 autonomous mode + LPBAM:** in Stop 2, LPDMA, LPTIM, LPUART, ADC4, I2C3, SPI3 keep
  running on a kernel clock (MSIK/HSI16) requested on demand. LPBAM queues (built with CubeMX LPBAM
  tool) chain DMA transfers that reconfigure peripherals. Set `RCC_SRDAMR` (autonomous mode enable
  per peripheral) and keep SRAM4 powered for the DMA buffers.
- **STM32L4/G0 "wake-up from Stop" peripherals:** LPUART, I2C address match, LPTIM, COMP can run in
  Stop and wake the core on a match only (not full DMA chains).
- **Microchip SAM Event System + SleepWalking:** peripherals run on demand clocks in standby; an
  event triggers ADC, the ADC window compare generates an interrupt only when out of range.
- **Silicon Labs PRS + LDMA / LESENSE:** LESENSE scans sensors/capacitive inputs in EM2 and wakes
  on a condition.

## Example design (nRF52)
RTC compare every 10 ms -> PPI -> SAADC SAMPLE; SAADC EasyDMA with buffer of 100 samples;
`EVENTS_END` interrupt once per second -> CPU processes 100 samples and goes back to System ON idle.
CPU wakes 1/s instead of 100/s.

## Gotchas
- Clocks: the peripheral's kernel clock must remain available in the chosen stop mode; otherwise
  it silently stops. Check the "peripheral availability in low-power modes" table in the RM.
- DMA buffers must be in a RAM bank retained and accessible in that mode (SRAM4 on U5).
- Errors (overrun) still need the CPU; enable their interrupts.
- Debug is hard: use GPIO events (GPIOTE task toggle via PPI) to observe hardware chains on a
  logic analyser.

## Verify
- [ ] CPU wake count (GPIO marker in ISR) matches the designed rate.
- [ ] Average current drops by the predicted amount vs the CPU-polling version.
