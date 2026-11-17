---
id: computing-software.firmware-embedded-development.hardware-debugging.scope-bandwidth-and-rise-time
name: scope-bandwidth-and-rise-time
category: computing-software
field: firmware-embedded-development
product: hardware-debugging
tags: [scope-bandwidth, rise-time, sample-rate, probe-bandwidth, bandwidth-limit, aliasing, oscilloscope, hardware-debugging, firmware-embedded-development]
level: practitioner
status: draft
description: "Pick scope and probe bandwidth and sample rate for firmware signals: 0.35/tr rule, system rise time, 20 MHz limit for rails, aliasing and why a 1x probe hides edges."
sources:
  - https://www.keysight.com/us/en/assets/7018-01811/application-notes/5989-5733.pdf
  - https://www.tek.com/en/documents/primer/oscilloscope-basics
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Scope bandwidth and rise-time selection

## The rules
- Signal bandwidth from edge speed, not clock rate: `BW ~= 0.35 / t_rise` (10-90%). A 3.3 V GPIO
  with 2 ns edges contains ~175 MHz, even if it toggles at 1 kHz.
- Measure rise time within ~3%: scope BW >= 5x signal BW. For 20% accuracy, 1.5-2x.
- System rise time: `t_sys = sqrt(t_signal^2 + t_scope^2 + t_probe^2)`, scope `t = 0.35/BW`.
  A 100 MHz scope (3.5 ns) shows a 2 ns edge as 4 ns.
- Sample rate >= 2.5-5x bandwidth on the active channels; interleaving halves it when you enable
  more channels on many scopes.

## Typical firmware signals
| Signal | Edge | Needed scope BW |
|---|---|---|
| I2C 400 kHz | 50-300 ns (pull-up RC) | 20-50 MHz |
| UART, PWM, slow GPIO timing | 2-10 ns (MCU pins, fast slew) | 100-200 MHz for edges, 20 MHz for timing |
| SPI 20-50 MHz, SDIO, QSPI | 1-3 ns | 350 MHz-1 GHz |
| Power rails ripple | n/a | enable 20 MHz BW limit |

## Probes
- 10x passive: 10 MOhm, 10-15 pF, rated 200-500 MHz with the short ground spring. Compensate on the
  scope's cal output before trusting edges.
- 1x passive: ~6-20 MHz bandwidth and ~100 pF load; it rounds edges and loads the circuit. Use only
  for millivolt ripple at low frequency.
- Active probes (<1 pF) for fast signals on high-impedance nodes (crystal pins, RC networks).

## Aliasing
Undersampling a fast clock shows a slow false waveform that looks real. Check by changing timebase
or sample rate: a real signal keeps its frequency, an alias changes. Use peak-detect acquisition
to catch narrow glitches at slow timebases.

## Gotchas
- Probing a crystal oscillator with a 10x passive probe adds ~10 pF and may stop or pull it; use an
  active probe or probe the MCO output instead.
- Bandwidth limit (20 MHz) hides switching spikes: off for edges, on for ripple and noise floor.
- "Overshoot" on fast edges is often the ground lead's inductance; switch to a spring ground.

## Verify
- [ ] Measured rise time stable when switching probe ground from lead to spring.
- [ ] Instrument BW choice documented next to the measurement.
