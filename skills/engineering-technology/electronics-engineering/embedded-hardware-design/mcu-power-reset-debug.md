---
id: engineering-technology.electronics-engineering.embedded-hardware-design.mcu-power-reset-debug
name: mcu-power-reset-debug
category: engineering-technology
field: electronics-engineering
product: embedded-hardware-design
tags: [embedded-hardware-design, microcontroller, mcu, soc, power-tree, ldo, buck-converter, decoupling, reset-circuit, brown-out, supervisor, boot-strapping, boot-pins, crystal, hse, load-capacitance, swd, jtag, debug-header, tag-connect, esd-protection, stm32, rp2040, esp32, nrf52]
level: practitioner
status: draft
description: "Design the core of an MCU board: power tree and LDO/buck choice, decoupling, reset and boot straps, clock source, SWD/JTAG debug header and protection."
sources:
  - "STMicroelectronics, AN2867 Oscillator design guide for STM8AF/AL/S and STM32 microcontrollers"
  - "STMicroelectronics, AN4488 Getting started with STM32F4xxxx MCU hardware development"
  - "Raspberry Pi Ltd, Hardware design with RP2040"
  - "Arm, CoreSight / Arm Debug Interface architecture documentation"
  - "Horowitz & Hill, The Art of Electronics, 3rd ed."
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# MCU core design — power, reset, clock, debug: the parts that must work first

**Goal:** a microcontroller board that powers up deterministically, boots in the mode
you intended, runs from a stable clock, and can always be reached by a debugger —
including when the firmware is broken.

## 0. Start from the vendor's hardware design guide
Every MCU family has a "getting started with hardware" application note and an
evaluation-board schematic. Read both before drawing anything; they list required
decoupling, strap pins, and errata that are not obvious from the datasheet.

## 1. Power tree
1. **List every rail and its load**: MCU core/IO, analog supply (VDDA), radio, sensors,
   peaks (radio TX bursts, flash writes) as well as averages.
2. **LDO vs buck**: LDO dissipation = (Vin − Vout) × I. 5 V → 3.3 V at 100 mA is
   0.17 W, fine; 12 V → 3.3 V at 300 mA is 2.6 W — use a buck. For battery devices
   look at **quiescent current** (µA-class LDOs/bucks) and dropout at end-of-discharge.
3. **Sequencing and inrush**: check whether IO and core rails need an order; SoCs often
   do. Bulk capacitance on hot-pluggable inputs causes inrush; add a load switch with
   controlled slew if needed.
4. **Input protection**: reverse polarity (P-FET ideal diode or series Schottky), TVS
   sized to the input's surge environment, fuse/PTC for external supplies.
5. Analog supply: feed VDDA through a ferrite bead + local caps (e.g. 1 µF + 100 nF)
   and tie its ground directly to the main plane.

## 2. Decoupling
Per vendor guide; a typical baseline is **100 nF X7R per VDD pin** placed at the pin
with its own via to ground, plus **one 4.7–10 µF bulk** per rail near the MCU. Many MCUs
need a specific capacitor on an internal regulator output (VCAP / VDDCORE, e.g. a
low-ESR 2.2–4.7 µF); missing it causes non-boot or random resets. Remember X5R/X7R
lose a lot of capacitance under DC bias — pick by the derated value.

## 3. Reset and brown-out
- Internal POR/BOR is usually sufficient; set the BOR threshold above the minimum
  voltage your flash and peripherals need.
- Add an external **supervisor** if rails ramp slowly, if a slow-starting regulator
  can leave the MCU in an undefined state, or if other chips must be held in reset.
- Reset pin: follow the guide (often 100 nF to ground, internal pull-up); put a
  test point or button on it, and route it to the debug header.

## 4. Boot straps
Identify every pin sampled at reset (BOOT0, strapping GPIOs on ESP32-class parts,
boot-mode pins on SoCs). Give each a **defined resistor** (10 kΩ typical) to the
intended level — never rely on floating or on an external device's state at power-up.
If a strap pin is shared with a peripheral, check that the peripheral does not drive
it during reset.

## 5. Clock
- Use the internal RC if timing allows (UART at modest baud, no USB/radio).
- External crystal: choose load caps from **CL = (C1·C2)/(C1+C2) + Cstray**, so for
  CL = 10 pF and ~3–5 pF stray, C1 = C2 ≈ 10–14 pF. Check oscillator **gain margin**
  (ST AN2867 method) — a crystal with ESR above the MCU's limit may start on the bench
  and fail cold.
- Layout: crystal within a few mm, guard with ground, no signals under or between.
- 32.768 kHz crystals are especially sensitive: low drive level, very short traces.

## 6. Debug access
- Bring out **SWD (SWDIO, SWCLK, NRST, VTref, GND, optional SWO)** or JTAG on a
  standard footprint: the 10-pin 1.27 mm Arm Cortex Debug header, or a pad-only
  Tag-Connect footprint to save space and cost.
- **VTref** must be the target IO voltage so the probe level-shifts correctly.
- Don't share SWD pins with functions that are driven at boot; keep a way to connect
  under reset (NRST on the header) for firmware that disables debug pins or sleeps.
- Add a UART console test point and an LED on a spare GPIO: cheap bring-up insurance.
- ESD protection on any debug connector exposed to users.

## 7. Peripherals at the board edge
Every pin that leaves the board gets ESD/series protection; USB needs its
specified ESD part and 90 Ω differential routing; long cable I/O needs filtering
(see emc-design skills).

## Verify
- [ ] Every rail's regulator dissipation and dropout checked at worst-case input and load.
- [ ] Decoupling and VCAP/core-regulator capacitors match the vendor guide, using derated values.
- [ ] Every boot/strap pin has a defined resistor and is not driven during reset.
- [ ] Crystal load caps calculated and gain margin checked against the MCU limit.
- [ ] Debug header includes NRST and VTref; connect-under-reset works on the first board.
- [ ] Power-up with a slow-ramping supply resets cleanly (no partial boot).
