---
id: computing-software.firmware-embedded-development.low-power-design.current-profiling-and-duty-cycle-budget
name: current-profiling-and-duty-cycle-budget
category: computing-software
field: firmware-embedded-development
product: low-power-design
tags: [low-power, ultra-low-power, battery-life, power-budget, duty-cycle, average-current, current-profiling, power-profiler-kit, ppk2, joulescope, ucurrent, otii, shunt-resistor, burden-voltage, sleep-current, quiescent-current, ldo, buck-converter, gpio-leakage, floating-inputs, clock-gating, self-discharge, battery-derating, coin-cell, shunt-measurement, firmware-embedded-development]
level: practitioner
status: draft
description: "Estimate and prove battery life: duty-cycle average current maths, derated capacity, PPK2/Joulescope profiling, shunt burden voltage, and hunting GPIO, clock and regulator leakage."
sources:
  - https://www.nordicsemi.com/Products/Development-hardware/Power-Profiler-Kit-2
  - https://www.joulescope.com/
  - https://www.ti.com/power-management/overview.html
  - https://www.eevblog.com/product/ucurrentgold/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Current profiling and duty-cycle budget — battery life you can defend

**Goal:** a spreadsheet-level power budget for a battery device, backed by real current traces,
with the sleep floor driven down to what the datasheets promise.

## 1. The budget maths
Split one period into phases (sleep, wake/boot, sense, compute, radio TX/RX):

`I_avg = Σ(I_phase × t_phase) / T_period`

`Life_hours = C_effective / I_avg`

Example, 60 s period: sleep 4 µA × 59.9 s, sense 1.5 mA × 80 ms, radio 8 mA × 20 ms:
(0.004 × 59.9 + 1.5 × 0.08 + 8 × 0.02) / 60 = (0.2396 + 0.12 + 0.16) / 60 ≈ 8.7 µA.
Note the sleep floor is nearly half the total — at low duty cycles, **sleep current dominates**;
at high duty cycles, active time does. Know which regime you are in before optimising.

## 2. Derate the battery
Nameplate capacity is measured at a gentle load and room temperature. Apply, as a starting point
(check your cell's datasheet curves):
- Cut-off voltage: your circuit's minimum (e.g. brown-out at 2.0–2.4 V) may strand capacity.
- Pulse load: coin cells (CR2032, ~220–240 mAh nominal) lose much of their capacity under
  ~10+ mA pulses due to internal resistance; add a bulk capacitor and spread radio bursts.
- Cold: alkaline and Li-ion lose substantial capacity below 0 °C.
- Self-discharge: roughly 1–3%/month for Li-ion, around 1%/year for Li-SOCl2 primaries.
- Ageing and margin: use 70–80% of nameplate as `C_effective` unless you have curves.

## 3. Measuring tools
| Tool | Strength | Note |
|---|---|---|
| Nordic PPK2 | ~nA to 1 A, 100 kS/s, source or ammeter mode, cheap | specified accuracy varies by range |
| Joulescope (JS110/JS220) | wide dynamic range, fast autoranging, energy integration | higher cost |
| µCurrent Gold + scope | amplifies shunt voltage (mV/nA, mV/µA, mV/mA ranges) | manual ranging |
| Bench DMM | fine for steady sleep current | too slow for bursts; range switching resets devices |
Integrate charge over **whole periods** (many of them), not spot readings.

## 4. Shunts and burden voltage
Any ammeter inserts resistance; `V_burden = I × R_shunt`. A DMM on its µA range may have ~100 Ω+
of shunt: a 50 mA radio burst would drop several volts, browning out the MCU — and the reset looks
like a firmware bug. Autoranging profilers minimise this, but fast transitions from µA to mA can
still glitch on some tools. Power the device the way it ships (battery voltage, same regulator)
and measure on the battery side to include regulator losses. Remove the debug probe: an attached
SWD/JTAG probe and debug-in-sleep bits (e.g. STM32 `DBGMCU` low-power debug) keep clocks running.

## 5. Hunting the sleep floor
Compare measured sleep current with the sum of datasheet values (MCU sleep mode + RTC +
regulator Iq + sensors in standby). Then:
- **Floating inputs:** an unconnected CMOS input sitting mid-rail can draw tens to hundreds of µA.
  Configure unused pins as analog (lowest leakage on STM32) or with a pull, per the vendor's
  low-power app note.
- **Pull-ups fighting loads:** a 10 kΩ pull-up on a line held low by a sleeping peripheral costs
  330 µA at 3.3 V. Check every resistor divider and pull path in sleep state.
- **Peripheral clocks:** disable clocks and peripherals (ADC, timers, UART, comparators,
  reference voltages) before sleep; some ADCs keep an internal reference on.
- **Regulator quiescent current:** an LDO like the classic AMS1117 class draws mA-level Iq;
  nano-power LDOs and bucks are in the sub-µA to µA range. Check light-load efficiency of bucks.
- **Sensors and radios:** confirm each external chip is commanded into its own power-down mode,
  or power-gate it with a load switch (watch back-powering through I/O pins when gated).
- **LEDs and dev-board parts:** power LEDs, USB-UART bridges and level shifters on evaluation boards
  routinely add mA. Profile your own hardware.
Bisect: remove/disable one block at a time and note the delta in a table.

## 6. Shorten active time
Run fast and sleep (race-to-idle), batch radio traffic, cache network state, and use DMA or hardware
triggers so the CPU sleeps during transfers. ESP32 specifics:
computing-software.firmware-embedded-development.esp-idf.deep-sleep-power-budgeting.

## Verify
- [ ] Budget table lists every phase with measured current and duration, and computes `I_avg`.
- [ ] Measured average over at least 10 full periods agrees with the budget within ~10–20%.
- [ ] Sleep current measured with the debugger disconnected and on production hardware.
- [ ] Every unused GPIO has a defined state in sleep; no floating inputs remain.
- [ ] Battery life uses a derated capacity with stated assumptions (temperature, cut-off, pulse load).
- [ ] The device survives the largest current burst through the measurement setup without brown-out.
