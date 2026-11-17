---
id: computing-software.firmware-embedded-development.hardware-debugging.signal-integrity-diagnosis-for-firmware
name: signal-integrity-diagnosis-for-firmware
category: computing-software
field: firmware-embedded-development
product: hardware-debugging
tags: [oscilloscope, signal-integrity, ringing, overshoot, crosstalk, series-termination, double-clocking, slow-edges, firmware-embedded-development]
level: advanced
status: draft
description: "Diagnose bus errors caused by signal integrity (ringing, double clocking, crosstalk, slow edges) with a scope, and fix with series resistors, slew settings or pull-ups."
sources:
  - https://www.ti.com/lit/an/scaa082/scaa082.pdf
  - https://www.tek.com/en/documents/primer/xyzs-oscilloscopes-primer
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Signal integrity diagnosis for firmware engineers

**Goal:** tell a firmware bug from an electrical one when SPI/I2C/UART/clock signals
misbehave, and apply the usual fixes.

## Symptoms that point to SI, not code
- Errors depend on cable length, board revision, temperature or which probe is attached.
- SPI reads with **bit shifts** or occasional doubled bits: ringing on SCK crosses the
  threshold twice (double clocking).
- Errors only at higher clock rates, gone when the bus is slowed down 2-4x.
- I2C NACKs/arbitration loss with long wires or many devices: slow rise times.

## What to look at (with a properly grounded probe)
| Observation | Likely cause | Fix |
|---|---|---|
| Overshoot/undershoot > ~0.5 V, ringing on edges | fast driver into unterminated trace | **series resistor 22-47 ohm** at the driver, reduce GPIO speed setting |
| Non-monotonic edge (a step or dip mid-edge) on clock | reflection on long trace / stub | source termination, shorter stubs, point-to-point routing |
| Glitch on a quiet line when a neighbour switches | crosstalk | spacing, ground between, slower edges on aggressor |
| I2C rise time > 300 ns (Fast mode) / 1000 ns (Standard) | pull-up too weak for bus capacitance | stronger pull-up: R <= t_r / (0.8473 x C_bus) |
| Edges fine but data wrong at sample time | setup/hold timing, wrong SPI mode | check against datasheet timing diagram, try other CPHA |
| Supply droop when bus switches | ground bounce / decoupling | add decoupling, reduce simultaneous fast edges |

## Measuring well
- Use the scope's bandwidth limit off and fastest sample rate for edges; trigger on the edge
  of interest (edge or runt trigger for marginal levels).
- Measure at the **receiver** pin, not the driver: reflections look different at each end.
- Eye-ball thresholds: draw cursors at the receiver's VIL/VIH (e.g. 0.3/0.7 x VDD for CMOS);
  ringing that re-crosses them is a real problem.

## Firmware-side mitigations
- Lower GPIO slew (`OSPEEDR`) on clock/data lines.
- Reduce bus clock; add retries with CRC (protocol-level) for marginal links.
- SPI: sample later (higher CPHA mode only if the device supports it), or add delay between
  CS assert and first clock.

## Verify
- [ ] After the fix, a stress test (millions of transfers with CRC/readback) shows zero errors.
- [ ] Scope at the receiver shows clean monotonic edges within threshold margins.
