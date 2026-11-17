---
id: computing-software.firmware-embedded-development.low-power-design.load-switch-peripheral-power-gating
name: load-switch-peripheral-power-gating
category: computing-software
field: firmware-embedded-development
product: low-power-design
tags: [power-supply-design, load-switch, power-gating, back-powering, inrush-current, sensor-power-cycle, gpio-powered-sensor, firmware-embedded-development]
level: advanced
status: draft
description: "Cut power to sensors, radios and SD cards between uses with load switches or GPIO power: sizing, inrush, back-powering through I/O pins, and power-up sequencing in firmware."
sources:
  - https://www.ti.com/lit/an/slva716/slva716.pdf
  - https://www.ti.com/lit/an/slvae36/slvae36.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Load switches and peripheral power gating

**Goal:** peripherals that consume zero (not "sleep mode") current while the device sleeps,
switched on only when needed, without glitches or phantom powering.

## Options
| Method | When |
|---|---|
| Dedicated load switch IC (TPS22916, TPS22917, SiP32431) | anything > a few mA, or needing controlled rise |
| P-MOSFET high-side switch | cheap, needs gate pull-up and care with Vgs |
| Powering directly from an MCU GPIO | small sensors < ~5-10 mA (check GPIO current spec and total port limit) |
A load switch's own quiescent current (10 nA..1 uA) must be smaller than what it saves.

## Firmware sequence
```c
sensor_power(true);              /* enable load switch */
delay_ms(SENSOR_TPU_MS);         /* rail rise (switch slew) + sensor power-up time from datasheet */
i2c_pins_to_af();                /* only now drive bus pins */
sensor_init();                   /* registers were lost: re-init every time */
read();
i2c_pins_to_analog();            /* before cutting power */
sensor_power(false);
```

## Back-powering (the classic leak)
With the sensor unpowered, any MCU pin driven high (or an I2C pull-up to the always-on rail)
feeds current through the sensor's ESD diodes into its VDD: the sensor half-powers, draws
hundreds of uA, may latch up or corrupt the bus. Rules:
- Set all signal pins to the unpowered peripheral to **analog/hi-Z or low** before switching off.
- Pull-ups for a gated device go to the **gated** rail, not the always-on rail.
- Shared buses (I2C with other always-on devices): an unpowered device must not clamp SDA/SCL;
  check its datasheet for "I/O tolerant when VDD = 0" (power-off protection) or use a bus
  switch.

## Inrush and droop
Switching on a peripheral with large input capacitance (SD card ~10 uF, radio module 100 uF)
draws a spike that can brown out the MCU. Use a load switch with controlled rise time
(or the CT pin), or add RC on the MOSFET gate. Measure the rail droop on the MCU side.

## Turn-on time budget
Load switch rise (100 us-1 ms) + device boot (sensor 1-100 ms, SD card init up to ~1 s, GNSS
cold start seconds to minutes). Power gating only pays if the off-time saving exceeds the
energy spent re-initialising: compute energy per cycle, not just sleep current.

## Verify
- [ ] Sleep current with peripherals off equals MCU sleep current + switch quiescent.
- [ ] Measure current into the gated rail with peripheral "off": ~0 (no back-powering).
- [ ] MCU rail droop at switch-on stays above BOR threshold.
