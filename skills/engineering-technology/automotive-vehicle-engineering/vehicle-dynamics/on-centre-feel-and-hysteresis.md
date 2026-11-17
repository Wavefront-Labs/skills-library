---
id: engineering-technology.automotive-vehicle-engineering.vehicle-dynamics.on-centre-feel-and-hysteresis
name: on-centre-feel-and-hysteresis
category: engineering-technology
field: automotive-vehicle-engineering
product: vehicle-dynamics
tags: [on-centre-feel, on-centre, steering-hysteresis, weave-test, iso-13674, dead-band, steering-friction]
level: practitioner
status: gated
description: "Quantify on-centre steering feel with weave tests: torque-angle hysteresis, steering sensitivity and lateral response, and trace friction sources."
sources:
  - "ISO 13674-1 (weave test), confirm current edition"
  - "Pfeffer and Harrer, Steering Handbook"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# On-centre feel and hysteresis

1. Test: weave test with sinusoidal steering around centre; ISO 13674-1 (weave test) is the procedure. Speed, frequency and peak lateral acceleration commonly quoted (100 km/h, about 0.2 Hz, about 0.2 g) (gated: unconfirmed, source is paywalled or blocked); confirm in the current edition.
2. Plot steering torque vs steering angle: hysteresis loop width is friction plus compliance; slope is stiffness; plot lateral acceleration vs steering angle for response gain and torque vs lateral acceleration for the gradient.
3. Metrics: torque deadband, hysteresis at zero lateral acceleration, steering sensitivity (ay per degree), phase lag between torque and acceleration.
4. Sources of friction: rack and pinion mesh, column universal joints, tie-rod joints, bushings and the tyre itself; separate by testing the steering on a bench and in the vehicle.
5. Improve: reduce joint friction, improve supports, balance EPS friction compensation.

**Gotchas:** assist software can mask or amplify hysteresis; test with and without friction compensation if possible.

## Verify
- [ ] Repeat tests show consistent hysteresis metrics.
- [ ] Subjective rating correlates with measured sensitivity and deadband.
