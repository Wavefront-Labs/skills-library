---
id: computing-software.firmware-embedded-development.device-driver-development.i2c-pull-up-resistor-sizing
name: i2c-pull-up-resistor-sizing
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [i2c-pull-up, i2c, bus-capacitance, rise-time, fast-mode-plus, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Size I2C pull-up resistors from bus capacitance and rise-time limits (UM10204), recognise slow-edge failures on a scope, and cope with excess bus capacitance."
sources:
  - https://www.nxp.com/docs/en/user-guide/UM10204.pdf
  - https://www.ti.com/lit/an/slva689/slva689.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pull-up sizing and bus capacitance

I2C lines are open-drain: devices only pull low, resistors pull high. The RC time constant of the
pull-up and the bus capacitance decides whether the bus meets its rise-time limit.

## Limits (UM10204 Rev 7.0, Tables 10 and 11)
| Mode | Max clock | Max rise time tr (30% to 70%) | Max bus C | Min sink current (VOL 0.4 V) |
|---|---|---|---|---|
| Standard | 100 kHz | 1000 ns | 400 pF | 3 mA |
| Fast | 400 kHz | 300 ns | 400 pF | 3 mA |
| Fast-mode Plus | 1 MHz | 120 ns | 550 pF | 20 mA |

## Formulas
UM10204 section 7.1 and TI SLVA689 give the same equations, using VIH = 0.7 VDD and
VIL = 0.3 VDD:
- Rise time between the thresholds: `tr = 0.8473 * Rp * Cb`
- Maximum resistance (rise time): `Rp(max) = tr / (0.8473 * Cb)`
- Minimum resistance (sink current): `Rp(min) = (VDD - VOL(max)) / IOL`

Example, Fast mode, 3.3 V, Cb = 150 pF:
`Rp(max) = 300 ns / (0.8473 * 150 pF) = 2.36 kOhm`, `Rp(min) = (3.3 - 0.4) / 3 mA = 967 Ohm`.
Pick a value between the two. UM10204 notes that supply-current-sensitive designs can use a
value toward the higher end of the range.

## Estimating Cb
Cb is the total capacitance of wire, connections and pins. UM10204 allows up to 10 pF per I/O
pin (Ci). Measure instead: on a scope, the rise time with a known Rp gives
`Cb = tr / (0.8473 * Rp)`.

## Symptoms of wrong pull-ups
- Too weak (Rp above Rp(max)): rise time exceeds the mode's limit, so edges are slow and rounded
  and the bus may fail at higher clock speeds.
- Too strong (Rp below Rp(min)): the low level can rise above the VOL limit because the device
  cannot sink the current, and the current drawn while low is VDD / Rp.
- Pull-ups on several boards sit in parallel, so the effective resistance drops; keep one set of
  pull-ups per bus segment.

## Excess bus capacitance (UM10204 section 7.2)
If the bus exceeds its capacitance limit the options are: lower fSCL, devices with higher drive
current (Fast-mode Plus parts), bus buffers that split the bus into segments each under the limit
(UM10204 names the PCA9517 buffer and the PCA9546A switch), or a switched pull-up circuit that
accelerates rising edges.

## Verify
- [ ] Scope SCL and SDA at the furthest device: 30% to 70% rise time within the mode's limit; low level below 0.4 V.
- [ ] Bus works at the target speed across temperature and supply tolerance.

## Checked
2026-11-09. Read: NXP UM10204 Rev 7.0 (Table 10 sink currents, Table 11 fSCL, tr and Cb rows,
section 7.1 equations and the 3 mA and 20 mA minimum sink current text, section 7.2 strategies)
and TI SLVA689 (equations 1 to 8, worked example and Cb 550 pF row). Removed: per-pin, per-cm
and per-metre capacitance estimates beyond UM10204's 10 pF, internal MCU pull-up values and the
1.5 us estimate, the "4.7k everywhere" remark, NACK and clock-stretching symptoms, the
PCA9515, TCA9517, LTC4311 and TCA9548A part suggestions (UM10204 names PCA9517 and PCA9546A).
Method: docs-checked 2026-11-09 against UM10204 Rev 7.0 and TI SLVA689.
