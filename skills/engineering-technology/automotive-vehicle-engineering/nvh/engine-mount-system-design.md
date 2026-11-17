---
id: engineering-technology.automotive-vehicle-engineering.nvh.engine-mount-system-design
name: engine-mount-system-design
category: engineering-technology
field: automotive-vehicle-engineering
product: nvh
tags: [engine-mounts, powertrain-mounts, torque-roll-axis, mount-decoupling, hydromount, rigid-body-modes, powertrain-noise]
level: practitioner
status: gated
description: "Design the powertrain mounting system: rigid-body mode placement, torque-roll-axis decoupling, mount rates, hydromounts and checks for static deflection and shake."
sources:
  - "Harrison, Vehicle Refinement"
  - "Genta, Motor Vehicle Dynamics"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Engine mount system design

1. Rigid-body modes: a powertrain on mounts has six modes (bounce, roll, pitch, yaw, lateral, fore-aft); target frequencies typically about 8-20 Hz (gated: unconfirmed, source is paywalled or blocked), below the idle firing frequency divided by root-two (isolation begins at frequency ratio sqrt(2)); for a 4-cylinder at 750 rpm idle the firing frequency is 25 Hz, so the mount modes should sit below about 17.7 Hz (computed).
2. Decoupling: align the mount stiffness so that torque reaction is primarily in roll about the **torque roll axis (TRA)**; aim for high energy decoupling (commonly 80-90% target (gated: unconfirmed, source is paywalled or blocked)) in the roll mode, with other modes separated by at least 1-2 Hz.
3. Mount rates: stiffness set from static load (deflection under weight with limits on droop), cranking torque and maximum torque loads (limit travel with stops), and the frequency targets.
4. Hydromounts: provide damping near the rigid-body resonance (10-15 Hz) for shake and bump control while remaining soft at higher frequencies; active mounts use actuators to cancel idle and cylinder deactivation vibration.
5. Constraints: crash behaviour, engine-to-body clearance, maximum motion at tip-in and tip-out (shuffle), thermal exposure, durability.
6. Evaluate in multibody simulation, optimise with decoupling objective, then check physical vehicle idle and acceleration shake.
7. Tune with alternatives: mount bracket stiffness (non-rigid brackets lower the effective rate).

**Gotchas:** bracket compliance reduces mount decoupling effects.

## Verify
- [ ] Measured rigid-body mode frequencies near the targets in a vehicle test.
- [ ] Idle seat-rail and steering-wheel vibration within the target.
