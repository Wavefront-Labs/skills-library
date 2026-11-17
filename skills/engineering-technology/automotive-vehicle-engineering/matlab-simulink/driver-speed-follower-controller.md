---
id: engineering-technology.automotive-vehicle-engineering.matlab-simulink.driver-speed-follower-controller
name: driver-speed-follower-controller
category: engineering-technology
field: automotive-vehicle-engineering
product: matlab-simulink
tags: [driver-speed-follower, driver-model, pi-controller, anti-windup, feedforward, simulink]
level: practitioner
status: gated
description: "Build a driver block with feedforward plus PI and anti-windup that follows a cycle speed and splits output into accelerator and brake demands."
sources:
  - "Guzzella and Sciarretta, Vehicle Propulsion Systems"
  - "Simulink PID Controller block (https://www.mathworks.com/help/simulink/slref/pidcontroller.html)"
  - "Vehicle Dynamics Blockset: Longitudinal Driver (https://www.mathworks.com/help/vdynblks/ref/longitudinaldriver.html)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Driver speed-follower

1. Error `e = v_ref - v`. Feedforward from the cycle itself: `a_ref = dv_ref/dt` (precompute and look up) times mass gives a tractive force request, which removes most work from the PI.
2. PI with clamping anti-windup (PID block, Anti-windup = clamping). Start Kp so that a 1 m/s error asks for roughly 10-20% pedal (starting heuristic (gated: unconfirmed, source is paywalled or blocked)) and Ki to remove steady error in a few seconds; tune against cycle tracking.
3. Convert signed demand to pedals: positive -> accelerator 0..1, negative -> brake 0..1 with a small dead band to avoid fighting regen and friction.
4. Add a preview of 1-2 s of reference to start braking early at cycle decelerations.
5. Add rate limits on pedal so the plant sees human-like inputs.

**Gotchas:** integrator winding during standstill or traction limit; reset the integrator at cycle start and during gear changes if the driver is gear-aware.

## Verify
- [ ] RMS speed error and maximum error reported; trace tolerance respected.
- [ ] No simultaneous accelerator and brake above the dead band.
