---
id: engineering-technology.automotive-vehicle-engineering.nvh.inverter-switching-noise
name: inverter-switching-noise
category: engineering-technology
field: automotive-vehicle-engineering
product: nvh
tags: [inverter-noise, pwm-noise, switching-frequency, spread-spectrum, magnetostriction, ev-whine]
level: practitioner
status: gated
description: "Control inverter PWM noise: switching frequency choice, side-band harmonics, spread-spectrum and random PWM, and the audible effects on the motor and passives."
sources:
  - "Gieras, Wang and Lai, Noise of Polyphase Electric Motors"
  - "Mohan, Undeland and Robbins, Power Electronics"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Inverter switching noise

1. Mechanism: PWM voltage at switching frequency `f_sw` (commonly 8-20 kHz for IGBT; higher for SiC (gated: unconfirmed, source is paywalled or blocked)) causes current ripple; magnetic forces at `f_sw` and sidebands `f_sw +/- k*f_e` excite the motor structure and passive components (inductors, capacitors) leading to audible tones.
2. Audibility: tones in 2-8 kHz are very audible (gated: unconfirmed, source is paywalled or blocked); moving `f_sw` above 16-20 kHz makes the fundamental inaudible to most listeners (hearing range is nominally 20 Hz-20 kHz and falls with age (gated: unconfirmed, source is paywalled or blocked)), though sidebands and sub-harmonics can still be audible.
3. Switching frequency choice: higher fsw reduces current ripple and audible noise but raises switching loss (IGBT) so SiC helps; optimise by operating point.
4. Spread-spectrum / random PWM: dither the switching frequency to spread tonal energy into broadband noise (reduces tonality; a small loudness increase).
5. Variable fsw vs speed/torque to keep sidebands away from stator resonances.
6. Components: ceramic capacitor "singing" from piezoelectric effect and inductor magnetostriction; choose damped mounting and different components.
7. Measure: microphone near inverter and on the motor, narrow-band spectrum with sweeps.

**Gotchas:** control software updates can move PWM; include in release checks.

## Verify
- [ ] Narrow-band spectrum shows no tones above the target at any operating point.
- [ ] Tonality metric within the vehicle-level target.
