---
id: engineering-technology.automotive-vehicle-engineering.nvh.motor-whine-and-electromagnetic-orders
name: motor-whine-and-electromagnetic-orders
category: engineering-technology
field: automotive-vehicle-engineering
product: nvh
tags: [motor-whine, electromagnetic-noise, motor-orders, slot-pole-orders, torque-ripple, ev-nvh]
level: practitioner
status: gated
description: "Predict and treat EV motor whine: electromagnetic force orders from slots and poles, structure-borne and airborne paths, skew and current-harmonic countermeasures."
sources:
  - "Gieras, Wang and Lai, Noise of Polyphase Electric Motors"
  - "Harrison, Vehicle Refinement"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Motor whine and electromagnetic orders

1. Source: radial magnetic forces between rotor and stator vary with time and space; they excite stator modes and the motor housing; torque ripple (tangential) excites driveline.
2. Orders: with p pole pairs and Ns stator slots, important force orders appear at multiples of the electrical frequency `f_e = p*rpm/60`, e.g. 6th and 12th electrical harmonics for torque ripple in a three-phase machine, and slot-harmonic orders (e.g. `Ns/p` related; formula not confirmed (gated: unconfirmed, source is paywalled or blocked)) for radial forces; verify with a spectrum on the dynamometer.
3. Resonances: stator shell modes (ovalisation, higher-order), often cited at 1-4 kHz (gated: unconfirmed, source is paywalled or blocked); if an order crosses a resonance, tonal whine emerges (Campbell diagram).
4. Measures at the source: rotor or stator skew, optimised pole/slot count, rotor notches, current harmonic injection to cancel torque ripple, controlled PWM frequency/spread-spectrum.
5. Path: stiffer stator housing or damped mounts, isolation of the motor to the subframe, decoupling reduction gear, shields and encapsulation.
6. Targets: tonality and loudness limits by order; the lack of engine masking means whine is audible.
7. Verify on a semi-anechoic dyno: noise vs rpm and torque with order tracking, then in vehicle.

**Gotchas:** inverter PWM and control changes can alter tones; validate with final software.

## Verify
- [ ] Order plot shows reduced tonal orders after countermeasure at all torques.
- [ ] Vehicle interior tonality below the target in acceleration and cruise.
