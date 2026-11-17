---
id: computing-software.game-programming.game-physics.joint-motors-and-limits
name: joint-motors-and-limits
category: computing-software
field: game-programming
product: game-physics
tags: [game-physics, joint-motor, joint-limits, constraints, game-programming]
level: practitioner
status: verified
description: "Implement joint limits and motors: inequality rows with clamped accumulated impulses, motor max force, spring limits, and engine API settings."
sources: ["https://box2d.org/documentation/", "https://nvidia-omniverse.github.io/PhysX/physx/5.4.1/docs/Joints.html", "https://github.com/jrouwe/JoltPhysics"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Joint motors and limits

**Goal:** hinges that stop at angles, wheels driven by motors, doors that spring shut.

## Limits as inequality constraints
For a revolute joint angle `theta` with `[lower, upper]`:
- If `theta <= lower`: row `C = theta - lower >= 0`, accumulated impulse clamped `>= 0`.
- If `theta >= upper`: row `C = upper - theta >= 0`, clamped likewise.
- Equal limits: treat as an equality (lock).
Use speculative handling: activate the row slightly before the limit using
`bias = C / dt` when `C > 0` so the joint does not overshoot at speed.

## Motors
A velocity constraint `J*V = targetSpeed` with impulse clamped to `[-maxForce*dt, maxForce*dt]`:
```cpp
float Cdot = w2 - w1 - motorSpeed;
float impulse = -motorMass * Cdot;
float old = motorImpulse;
motorImpulse = clamp(old + impulse, -maxMotorTorque * dt, maxMotorTorque * dt);
impulse = motorImpulse - old;  // apply to both bodies' angular velocity
```
- Low max torque + target speed 0 = joint friction (doors that don't swing freely).
- Solve the motor before the limit so the limit wins (1-DOF test, motor at 5 rad/s into an upper limit of 0.5 rad: motor first ends at 0.500, limit first ends at 0.514).

## Engine APIs
- Box2D v3: `b2RevoluteJointDef.enableLimit/lowerAngle/upperAngle` (limits are restricted to +/-0.99*pi), `enableMotor/motorSpeed/
  maxMotorTorque`, `enableSpring/hertz/dampingRatio`.
- PhysX: `PxRevoluteJoint::setLimit(PxJointAngularLimitPair)` (hard, or soft with stiffness and damping), `setDriveVelocity`,
  `setDriveForceLimit`, `PxRevoluteJointFlag::eDRIVE_ENABLED`; D6 joints use `setDrive`.
- Jolt: `HingeConstraintSettings` limits (`mLimitsMin` in [-pi, 0], `mLimitsMax` in [0, pi]), `mMaxFrictionTorque`, and `MotorSettings` with velocity, position, or position-and-velocity motor states.

## Pitfalls
- Angle wrap: compute relative angle in `(-pi, pi]`; engines restrict the limit range (Box2D +/-0.99*pi, Jolt hinge [-pi, pi] with min <= 0 <= max), so a hinge that must turn further needs a different joint or motor logic.
- Position-driven motors with very high stiffness jitter; use soft spring parameters.

## Verify
- Drive a hinge at full torque into its limit: no penetration past limit, no jitter at rest.

## Checked (2026-10-22)
- Box2D main `types.h` (`b2RevoluteJointDef` fields and the +/-0.99*pi comment); PhysX `PxRevoluteJoint.h` (`setLimit`, `setDriveVelocity`, `setDriveForceLimit`, `eDRIVE_ENABLED`), PxD6Joint.h `setDrive`, 5.4.1 Joints page (soft limits with stiffness/damping); Jolt `HingeConstraint.h` (`mLimitsMin/Max` ranges, `mMaxFrictionTorque`, `mMotorSettings`) and `MotorSettings.h` (`EMotorState`).
- Python 1-DOF hinge (inertia 1, 60 Hz, speculative limit `w <= C/dt`): motor then limit ends at theta 0.500 with zero penetration; limit then motor ends at 0.514. A motor with target speed 0 and max torque 0.5 against a 2 N m external torque lets the hinge accelerate (w = 3.0 rad/s after 2 s) while max torque 3 holds it at 0, matching the 'joint friction' bullet.
- The C++ motor snippet is the standard sequential-impulse form; its clamp logic was exercised in the Python port, not compiled.
