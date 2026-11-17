---
id: computing-software.firmware-embedded-development.hardware-debugging.logic-thresholds-and-level-compatibility
name: logic-thresholds-and-level-compatibility
category: computing-software
field: firmware-embedded-development
product: hardware-debugging
tags: [logic-threshold, vih, vil, level-shifting, 5v-tolerant, 1v8-logic, cmos-ttl, open-drain-level, hardware-debugging, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Check logic-level compatibility: VOH/VIH and VOL/VIL noise margins, TTL to CMOS interfacing with HCT parts or pull-ups, and the limits of each fix."
sources:
  - https://www.ti.com/lit/an/scla011a/scla011a.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Logic thresholds and level compatibility

## The four numbers
For every driver and receiver pair check, with the real supply and load:
- driver `VOH(min)` is above receiver `VIH(min)`, and the difference is the high-level noise margin;
- driver `VOL(max)` is below receiver `VIL(max)`, and the difference is the low-level noise margin.
Keep both margins large and the undefined region between VIL and VIH narrow. If interference
(inductive or ohmic drops, coupling with neighbouring lines) pushes a signal into the undefined
region, the receiver misreads it. Coupling between signal lines is usually the more critical source.

Percentage margin that matters is the margin divided by the signal swing. TI's worked example at
VCC = 5 V (typical output levels, so not datasheet minimums): HC 29.1% high and 18.7% low, HCT 60.4%
and 14.6%, TTL 22.5% and 12.9%. The low-level margin is the critical one in all three families.

## TTL outputs into 5 V CMOS inputs
TI's note describes three ways to fix a TTL VOH that is too low for an HC input VIH:
1. Use HCT devices, whose input threshold is TTL compatible (the note calls this the most convenient).
2. Add pull-up resistors at the TTL outputs (open-collector or otherwise).
3. Use level shifters (the note does not recommend this for this case because shifters add parts and
   board space and have no logic function).

Pull-up sizing from the note:
- Minimum Rp = (VCC(max) - VOL) / IOL (the HC input current is negligible). Example: SN74ALS03 at
  5.5 V, 0.4 V and 8 mA gives 640 ohms.
- Maximum Rp is set by the required rise time and the load capacitance C (driver output capacitance
  about 10 pF, each gate input about 5 pF, line about 1 pF per cm): Rp = t / (C x ln(1 - VIH/VCC)),
  with the sign taken so the result is positive. Example: C = 30 pF, tr = 500 ns, VIH 3.5 V at 5 V
  gives about 14 kohm. A larger resistor means slower edges; a smaller one is faster but uses
  more power.

## HCT cautions (from the note)
- HCT supplies are limited: below 4.5 V the noise margin reduces and TTL compatibility is lost.
- Supply current rises when inputs sit at TTL levels (the data sheet gives an ICC increase for
  VIL = 0.4 V and VIH = 2.4 V); the example shows about 4 mA more at low frequency, less above
  5 MHz.
- HCT adds roughly 1 to 2 ns delay compared with HC.
- Crosstalk: keep lines between HCT devices to about 10 cm to keep crosstalk below critical values.
  Do not use HCT in a pure CMOS system; HC has the wider supply range and better margins.

## Instruments
Analysers and scopes have their own input thresholds: set them to suit the bus voltage being probed,
and suspect a threshold in a slow-ramp region when decodes are glitchy but scope edges look clean.
Check your instrument's manual for its selectable thresholds.

## Verify
- [ ] Margins computed at worst-case supply for every cross-domain signal.
- [ ] Scope confirms high and low levels clear the receiver thresholds with the load attached.

## Checked
Confirmed from TI SCLA011A (SN54/74HCT application note): noise margin definitions, TTL to HC
incompatibility and the three fixes, pull-up equations and worked examples, noise margin table,
HCT supply, current, delay and line-length cautions. Removed as unconfirmed: the table of 3.3 V,
1.8 V, 5 V CMOS and TTL thresholds, 5 V tolerant pin rules, specific parts (74LVC1T45, BSS138,
PCA9306, TXB0108 and others), back-powering through ESD diodes, Schmitt trigger claims, and
Saleae and MSO threshold settings (Saleae root page held no such figures).

Method: docs-checked 2026-11-09 against the TI SCLA011A application note, downloaded as PDF and read in full as text.
