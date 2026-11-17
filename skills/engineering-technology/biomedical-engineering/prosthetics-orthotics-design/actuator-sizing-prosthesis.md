---
id: engineering-technology.biomedical-engineering.prosthetics-orthotics-design.actuator-sizing-prosthesis
name: actuator-sizing-prosthesis
category: engineering-technology
field: biomedical-engineering
product: prosthetics-orthotics-design
tags: [actuator-sizing, powered-prosthesis, exoskeleton, torque-speed, gearbox-ratio, series-elastic-actuator, battery-sizing, joint-power]
level: advanced
status: gated
description: "Size motors, gearboxes and batteries for powered prosthetic joints from gait data: torque-speed envelopes, thermal limits, series elasticity and energy per stride."
sources: ["Winter, Biomechanics and Motor Control of Human Movement (joint moment and power data)", "Pratt and Williamson, Series elastic actuators (IEEE/RSJ IROS 1995)", "Motor manufacturer sizing guides (current datasheets)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Actuator and battery sizing for powered prosthetic joints

**Goal:** choose a motor, transmission and battery that deliver the required joint torque and power over a gait cycle within mass, size and thermal limits.

## Inputs
- Joint **torque and angle versus time** from gait analysis (able-bodied data scaled by body mass or measured from the user), for walking at several speeds and for stairs and ramps.
- Joint power P = torque x angular velocity; identify **peak torque**, **peak speed**, **peak power** and the **RMS torque** (thermal duty).
- Order of magnitude for level walking ankle push-off: the plantarflexion moment peaks at about 1.5-1.7 N m per kg (gated: unconfirmed, source is paywalled or blocked) and the positive power peak is a few W per kg (gated: unconfirmed, source is paywalled or blocked) at comfortable speed; scale to the user mass and check against measured data.

## Sizing steps
1. **Torque-speed cloud:** plot instantaneous torque versus speed for the gait cycle (and other tasks) on the joint side.
2. **Choose a reduction ratio N:** motor torque = joint torque / (N x efficiency), motor speed = N x joint speed. Choose N so the cloud fits inside the motor's peak torque-speed envelope and the RMS torque is below the motor continuous torque rating (thermal limit), with margin (for example 20-30%).
3. **Motor selection:** use motor constants (torque constant Kt, resistance R, thermal resistance); copper loss P = (tau / Kt)^2 x R; check the temperature rise for the duty cycle in the worst ambient condition.
4. **Transmission:** efficiency, backdrivability (impact and passive swing), backlash, noise and mass; harmonic drives, planetary gears and ball screws trade these differently.
5. **Series elastic element:** a spring in series with the actuator stores energy during stance and releases it at push-off, lowering peak motor power and providing impact tolerance; size the spring stiffness to the torque-angle behaviour of the joint (quasi-stiffness).
6. **Energy per stride:** E = integral of positive electrical power over the cycle = integral of (torque x speed)/(efficiency of motor, drive and gearbox) plus losses and controller power, taking negative work as dissipated unless regeneration is designed. Multiply by strides per day for battery capacity with a margin for stairs, cold and ageing.
7. **Battery:** choose cell chemistry, capacity and protection circuit (lithium-ion with certified safety design, see medical-battery-safety), check voltage sag at peak current.

## Verify
- [ ] Torque-speed cloud sits inside motor and gearbox limits with margin.
- [ ] Thermal test at worst-case duty shows temperatures below the limits for skin and components.
- [ ] Battery runtime measured against the design in realistic walking tests.
