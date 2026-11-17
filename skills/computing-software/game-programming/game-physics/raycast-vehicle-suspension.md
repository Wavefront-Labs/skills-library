---
id: computing-software.game-programming.game-physics.raycast-vehicle-suspension
name: raycast-vehicle-suspension
category: computing-software
field: game-programming
product: game-physics
tags: [game-physics, vehicle-physics, raycast-vehicle, suspension, spring-damper, anti-roll-bar, wheel-raycast, arcade-car, game-programming, arcade-vehicle]
level: practitioner
status: verified
description: "Build a raycast-wheel vehicle: per-wheel suspension rays, spring-damper forces at contact points, anti-roll bars, drive/brake forces, and tuning for stable arcade or sim handling."
sources: ["https://docs.godotengine.org/en/stable/classes/class_vehiclebody3d.html", "https://github.com/bulletphysics/bullet3", "https://docs.unity3d.com/Manual/class-WheelCollider.html"]
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# Raycast vehicle suspension

**Goal:** a car built from one rigid body plus per-wheel raycasts, stable over bumps and fun to drive
(the model behind Bullet's btRaycastVehicle; Godot's `VehicleBody3D` docs say it is based on the raycast vehicle system, and warn it has known issues and is not meant for realistic vehicle physics).

## Per wheel, every physics step
```
origin = chassis.transform * wheel.mountPoint
hit = raycast(origin, -chassis.up, restLength + wheelRadius)
if hit:
    length = hit.distance - wheelRadius
    compression = restLength - length                     # > 0 when compressed
    springForce = stiffness * compression
    vel = dot(chassis.velocityAtPoint(hit.point), chassis.up)
    damperForce = -damping * vel
    F = clamp(springForce + damperForce, 0, maxForce)     # suspension only pushes
    chassis.addForceAtPosition(chassis.up * F, hit.point)  # (or along hit normal)
    wheel.grounded = true; wheel.load = F
```
Use a sphere/shape cast instead of a ray for smoother behaviour over edges and small obstacles.

## Tuning springs
Tune by natural frequency rather than raw stiffness (see game-physics soft-constraints-and-stable-springs):
`stiffness = m_corner * (2*pi*f)^2`, with corner mass = car mass / 4; damping from the ratio
(`c = 2 * zeta * sqrt(k * m_corner)`). Checked for a 300 kg corner with f = 1.5, 2.0 and 2.5 Hz and zeta = 0.3, 0.5 and 0.7: at 1 kHz the simulated damped
frequency and damping ratio match `f*sqrt(1-zeta^2)` and zeta to within 1%. Pick f and zeta from the ride you want.
Explicit (semi-implicit Euler) springs go unstable when `sqrt(k/m) * dt > 2`: at 50 Hz and 75 kg per wheel mass that is k above about 750,000 N/m;
below that, very stiff springs still ring, so raise the physics rate or soften.

## Driving forces (at the contact point, in the wheel's ground plane)
- Forward axis = wheel forward projected on ground plane; side axis = right projected.
- Drive: `engineForce * throttle` along forward on driven wheels; brake opposes forward velocity.
- Lateral grip: `-sideVelocity * gripFactor * load`, clamped by friction limit `mu * load`
  (simple arcade). For sim handling, use a slip-angle/slip-ratio tire model (see game-physics
  tire-friction-models).
- Steering rotates front wheel forward axes; reduce max steer angle with speed for stability.

## Stability helpers
- **Anti-roll bar**: per axle, `antiRoll = (compressionLeft - compressionRight) * antiRollStiffness`,
  apply it to the **body** pushing **up** at the more compressed wheel and **down** at the other: that reduces body roll and flips
  (static roll model, 30 kN/m springs, 1.6 m track, 2 kN m roll torque: 0.052 rad without a bar, 0.031 rad with a 10 kN/m bar applied this way,
  0.156 rad if the signs are reversed, i.e. the bar makes roll worse).
- Lower the centre of mass (set it explicitly on the rigid body, often below the chassis).
- Downforce proportional to speed squared for high-speed grip.
- Inertia tensor tweaks (larger yaw inertia) to calm twitchy steering.

## Verify
- [ ] Car settles at rest without bouncing or drifting on a slope (with brakes).
- [ ] Driving over bumps at speed does not launch or flip the car unexpectedly.
- [ ] Behaviour close at 50 and 100 Hz physics after frequency-based tuning: for f = 2 Hz, zeta = 0.5 the simulated damped frequency was 1.85 vs 1.79 Hz (3.7% apart) and zeta 0.54 vs 0.52, so allow a few percent.

## Checked (2026-10-22)
- Python quarter-car simulation (semi-implicit Euler, 4 s free oscillation from 5 cm): `k = m (2 pi f)^2`, `c = 2 zeta sqrt(k m)` reproduce the damped frequency and zeta at 1000 Hz (e.g. f = 2, zeta = 0.5: 1.736 Hz vs 1.732 expected, zeta 0.502); at 50/100 Hz the estimate drifts by up to about 7% for zeta = 0.7. Stability limit: with m = 75 kg, dt = 1/50, k = 1e5 and 3e5 stay bounded (omega*dt 0.73 and 1.26), k = 1e6 and 5e6 blow up (omega*dt 2.3 and 5.2).
- Anti-roll direction checked with the static roll-equilibrium formula in Python (numbers above); the original skill text pushed down on the compressed side, which is the wrong sign for forces applied to the body.
- Godot `VehicleBody3D.xml` class doc (fetched): based on the raycast vehicle system, known-issues note. Bullet `btRaycastVehicle.h` exists. Removed 'f ~1.5-2.5 Hz for road cars, higher for race cars' and the 0.3-0.7 damping range (no source) and the 'most arcade racers' claim.
- The pseudocode loop (ray, compression, spring + damper, clamp to push only) is the standard model; its spring and damper arithmetic is what the quarter-car test exercised, the raycast itself was not run.
