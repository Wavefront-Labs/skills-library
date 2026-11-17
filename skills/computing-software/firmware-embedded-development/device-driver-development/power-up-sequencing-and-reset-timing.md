---
id: computing-software.firmware-embedded-development.device-driver-development.power-up-sequencing-and-reset-timing
name: power-up-sequencing-and-reset-timing
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [power-up-sequence, reset-timing, power-on-reset, brown-out-reset, supply-sequencing, enable-pin, startup-delay, peripheral-reset, firmware-embedded-development]
level: practitioner
status: draft
description: "Meet power-up sequencing and reset timing from datasheets: rail order and ramp rates, POR/BOR thresholds, reset pulse widths, device ready times, and firmware delays for peripherals."
sources:
  - https://www.st.com/resource/en/application_note/an4488-getting-started-with-stm32f4xxxxx-mcu-hardware-development-stmicroelectronics.pdf
  - https://www.ti.com/power-management/sequencers-supervisors/overview.html
  - https://www.nxp.com/docs/en/user-guide/UM10204.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Power-up sequencing and reset timing

**Goal:** every device on the board starts in a defined state because rails, resets and
first accesses follow the order and delays the datasheets demand.

## What datasheets specify
- **Rail order** for multi-supply parts (core before I/O, or "VDDIO must not exceed VDDCORE +
  0.3 V"), FPGA/SoC sequencing tables, analog before digital.
- **Ramp rate / rise time** limits: POR circuits may not trigger on very slow ramps (e.g.
  supercap-backed rails) or the part requires monotonic rise.
- **POR/BOR thresholds** and hysteresis: the MCU holds reset until VDD > V_POR; brown-out reset
  (BOR) level selectable on many MCUs (option bytes) - set it above the minimum operating voltage
  of everything the MCU talks to.
- **Reset pulse width** min (e.g. 1 µs-10 ms for external parts) and **time from reset release to
  first access** (tREADY, tPU).
- **I/O state before power**: no signals driven into an unpowered device (injected current, see
  `absolute-maximum-vs-recommended-ratings`).

## Hardware enforcement
Voltage supervisors / reset ICs, regulator enable chains (PGOOD -> EN), sequencer ICs for
complex SoCs. Firmware cannot fix sequencing for rails that come up before it runs.

## Firmware responsibilities
- Drive peripheral reset and enable pins to a defined state as early as possible in startup
  (before slow init like clocks or RTOS start); configure safe default with pull resistors in
  hardware as well.
- Honour ready times with explicit, commented delays or ready polling:
```c
gpio_clear(SENSOR_RST); delay_us(10);      /* tRST_min 1 us (DS 7.5), margin x10 */
gpio_set(SENSOR_RST);   delay_ms(25);      /* tPU max 20 ms before first I2C access */
if (!sensor_probe()) retry_or_fail();
```
- Peripherals powered via load switches: wait the rail's rise plus device tPU after enabling;
  reinitialise them after every power-gating cycle.
- Flash and EEPROM: block writes during brown-out (check BOR / PVD) - a write during a sagging
  supply corrupts data.
- On warm reset the MCU restarts but external devices may not: reset them explicitly or
  re-probe (I2C bus recovery for a slave stuck mid-transfer).

## Measuring
Scope all rails, reset lines and an early-boot GPIO toggle on one capture triggered on the
first rail; check order, ramp and delays against the datasheet table at cold and hot.
Also test slow power-up (bench supply turned up by hand) and fast power cycling (brownout dips).

## Verify
- [ ] Capture showing each sequencing requirement met with margin.
- [ ] 1000 power-cycle soak with varying off-times: every boot enumerates all peripherals.
