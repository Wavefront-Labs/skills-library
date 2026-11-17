---
id: computing-software.robotics-software.robot-control-and-kinematics.pid-tuning-controllers
name: pid-tuning-controllers
category: computing-software
field: robotics-software
product: robot-control-and-kinematics
tags: [pid-tuning, pid-controller, anti-windup, ziegler-nichols, derivative-filter, control-loop-rate]
level: practitioner
status: draft
description: "Implement and tune PID loops: discrete form, anti-windup, derivative filtering, and step-response tuning."
sources:
  - https://control.ros.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# PID control
```python
class PID:
    def __init__(s, kp, ki, kd, umin, umax, tau_d=0.02):
        s.kp, s.ki, s.kd, s.umin, s.umax, s.tau = kp, ki, kd, umin, umax, tau_d; s.i = s.dprev = s.eprev = 0.0
    def step(s, e, dt):
        d_raw = (e - s.eprev) / dt; s.dprev += dt/(s.tau+dt) * (d_raw - s.dprev); s.eprev = e   # low-pass derivative
        u = s.kp*e + s.i + s.kd*s.dprev
        sat = min(max(u, s.umin), s.umax)
        if sat == u: s.i += s.ki * e * dt          # conditional integration = anti-windup
        return sat
```
- Tuning workflow: set `ki = kd = 0`, raise `kp` until oscillation (Ku, period Tu); Ziegler-Nichols PID start: `kp = 0.6 Ku`, `ti = Tu/2`, `td = Tu/8` (a starting point, usually too aggressive; back off). Then add `kd` for damping and a small `ki` for steady error.
- Run the loop at a fixed rate (ros2_control update_rate) and use measured `dt`.
- Position loops: velocity feed-forward and gravity feed-forward cut the work PID must do.

## Gotchas
- Derivative on noisy encoders without filtering amplifies noise.
- Integral windup after saturation causes overshoot; clamp or condition it.

## Self-check
Step response: overshoot under about 10 percent, settles, no limit cycle, and holds under load.
