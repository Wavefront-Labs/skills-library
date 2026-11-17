---
id: computing-software.firmware-embedded-development.hardware-debugging.hardware-rework-and-bug-isolation
name: hardware-rework-and-bug-isolation
category: computing-software
field: firmware-embedded-development
product: hardware-debugging
tags: [hardware-rework, bodge-wire, cut-trace, bug-isolation, firmware-vs-hardware, a-b-swap, hardware-debugging, firmware-embedded-development]
level: advanced
status: draft
description: "Decide whether a bug is firmware or hardware and isolate it: A/B board swaps, minimal firmware repro, cut-and-jumper rework, part swaps, and documenting rework for the next spin."
sources:
  - https://www.analog.com/en/resources/analog-dialogue/articles/troubleshooting-tips.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Hardware rework and bug isolation

## Firmware or hardware?
1. **Does it follow the board?** Same firmware on 3-5 boards. One board fails = assembly defect;
   all fail = design or firmware.
2. **Does it follow the firmware?** Known-good minimal firmware (vendor example, bring-up test)
   on the failing board. Still fails = hardware.
3. **Does it follow temperature/voltage?** Freeze spray, heat gun, bench supply at min/max rail.
   Marginal timing, crystals and solder joints react; pure firmware logic bugs do not.
4. **Measure, don't infer:** scope the signal at the pin of the receiving chip, not at the driver.

## Isolation tricks
- Remove or lift a component's supply/enable to see if the problem disappears (a device holding
  I2C SDA low, a chip back-powered through I/O).
- Swap the suspect part between a good and bad board (U5 moves -> fault moves).
- Drive the input from a function generator instead of the real source.
- Disconnect a bus segment with a cut trace or by removing a 0 ohm resistor (good designs place
  them for exactly this).

## Common rework
- **Bodge wire:** 30 AWG Kynar wire, tack to pads/vias, glue down with UV-cure mask or Kapton;
  keep short on fast signals.
- **Cut trace:** scalpel, two parallel cuts and remove the copper between; verify open with a DMM.
- **Pull-up/pull-down additions** on 0402 pads or across pins.
- **Lifted pin:** heat the pin, lift with a fine tip, solder a wire to it.
- **BGA:** needs hot-air station or rework machine; usually do on a spare board.
Follow ESD practice and IPC-7711/7721 methods when boards go to customers.

## Firmware workarounds
Often cheaper than rework for prototype builds: swap pin functions, invert polarity in software,
add delays for slow power-up, bit-bang a bus on spare pins. Mark them with the board revision so
they are removed after the fix (`#if BOARD_REV < 3`).

## Record
Maintain a rework list per revision (what, why, which boards) and an ECO list for the next spin;
mark reworked boards physically (label, sticker colour).

## Verify
- [ ] Fix confirmed on at least two boards, and the original failure reproduces when undone.
- [ ] Next-revision schematic includes the change.
