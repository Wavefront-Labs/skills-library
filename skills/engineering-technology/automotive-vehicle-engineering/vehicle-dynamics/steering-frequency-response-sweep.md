---
id: engineering-technology.automotive-vehicle-engineering.vehicle-dynamics.steering-frequency-response-sweep
name: steering-frequency-response-sweep
category: engineering-technology
field: automotive-vehicle-engineering
product: vehicle-dynamics
tags: [steering-frequency-response, frequency-response, sine-sweep, yaw-bandwidth, phase-lag, handling-bandwidth]
level: practitioner
status: draft
description: "Run a steering frequency-response sweep, compute yaw-rate and lateral-acceleration gain and phase against frequency, and judge handling bandwidth."
sources:
  - "Gillespie, Fundamentals of Vehicle Dynamics"
  - "ISO 7401 (frequency-response method), confirm edition"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Steering frequency-response sweep

1. Drive at constant speed with sinusoidal or swept-sine steering of small amplitude (0.1-0.4 g in linear range) from about 0.1 Hz to 3-4 Hz. Hold a few cycles per frequency for steady results, or use chirp with careful windowing.
2. Compute transfer function from steering angle to yaw rate and lateral acceleration: `H(f) = Pxy(f)/Pxx(f)` (cross-spectrum over input auto-spectrum), with coherence above ~0.9 as quality gate.
3. Read DC gain, resonance peak, **-3 dB bandwidth** and phase lag at 1 Hz. Phase lag at 1 Hz relates to perceived lag between input and car response; lower is usually better.
4. Compare with the bicycle-model transfer function and tune parameters: rear stiffness, inertia, tyre relaxation length.
5. Repeat at several speeds.

**Gotchas:** limit amplitude to the linear range; nonlinear distortion shows as low coherence.

## Verify
- [ ] Coherence above the quality gate in the band of interest.
- [ ] Measured and modelled magnitude/phase overlay within an agreed tolerance.
