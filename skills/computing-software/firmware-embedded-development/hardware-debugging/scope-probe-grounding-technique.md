---
id: computing-software.firmware-embedded-development.hardware-debugging.scope-probe-grounding-technique
name: scope-probe-grounding-technique
category: computing-software
field: firmware-embedded-development
product: hardware-debugging
tags: [oscilloscope, probe-ground-lead, ground-spring, probe-compensation, x10-probe, loading, ground-loop, mains-earth, firmware-embedded-development]
level: practitioner
status: draft
description: "Probe digital and power signals without measuring artefacts: ground spring vs 15 cm lead, probe compensation, 1x vs 10x loading, and safe grounding to avoid shorts."
sources:
  - https://www.tek.com/en/documents/primer/abcs-probes-primer
  - https://www.keysight.com/us/en/assets/7018-06765/application-notes/5992-2475.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Oscilloscope probe grounding technique

**Goal:** see the signal that is really there. Most "ringing" debugged by firmware engineers
is produced by the probe's ground lead.

## Ground lead inductance
A standard 15 cm ground clip is ~150 nH. With the probe tip capacitance (~10 pF) it forms a
resonant circuit around 100-150 MHz that rings on any edge faster than ~3 ns, i.e. every
modern MCU GPIO at high speed setting. Fixes:
- **Ground spring** (the little coil shipped with the probe) touching a ground pad within a
  few mm of the signal: resonance moves above the scope bandwidth.
- Solder a short ground wire or use a PCB probe adapter / test point with adjacent ground.
- Compare: if the "ringing" frequency changes when you move the ground lead, it's the probe.

## Probe setup
- **10x passive probes** for almost everything: ~10 Mohm // 10-15 pF loading, full scope
  bandwidth. **1x** has ~100 pF loading and ~6-20 MHz bandwidth; use only for small signals
  like ripple on low-impedance rails.
- **Compensate** each probe on the scope's calibration square wave whenever moved between
  channels/scopes: adjust until the top is flat (overshoot or rounded corners otherwise mean
  wrong amplitudes on edges).
- Set the scope channel to the probe attenuation (most auto-detect).
- Bandwidth: for edges, scope+probe bandwidth >= 0.35 / rise time x 3-5.

## Safety and grounding loops
- Scope ground clips connect to **mains earth**. Clipping ground onto a node that isn't at
  earth potential (a non-isolated SMPS primary, a high-side shunt, a mains-powered circuit)
  shorts it through the scope: blown traces, sometimes injuries. Use a **differential probe**
  or an isolated scope for floating measurements. Never float the scope by removing its earth.
- USB-powered boards connected to a PC and scope have a ground loop; mostly fine, but
  noise measurements may show mains hum through it.

## Loading effects on firmware-visible behaviour
- Probing a crystal oscillator pin adds capacitance and can stop or shift it: probe the
  MCO output instead.
- 10 pF on a weak I2C pull-up line slows edges slightly; usually fine. On high-impedance
  analog nodes (MOhm dividers) the 10 Mohm probe changes the reading.

## Verify
- [ ] Same edge measured with long ground lead vs spring: ringing gone with spring.
- [ ] Probe compensation checked on the cal output today.
- [ ] Ground connection point for floating circuits reviewed before clipping on.
