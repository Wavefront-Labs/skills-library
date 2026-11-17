---
id: engineering-technology.automotive-vehicle-engineering.matlab-simulink.road-grade-and-wind-inputs
name: road-grade-and-wind-inputs
category: engineering-technology
field: automotive-vehicle-engineering
product: matlab-simulink
tags: [road-grade-input, road-grade, wind-input, grade-resistance, lookup-table, simulink]
level: practitioner
status: verified
description: "Feed grade and headwind into a Simulink vehicle model from distance-based profiles, with correct force terms and a distance integrator."
sources:
  - "Gillespie, Fundamentals of Vehicle Dynamics"
  - "Guzzella and Sciarretta, Vehicle Propulsion Systems"
  - "https://www.mathworks.com/help/simulink/slref/1dlookuptable.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Road grade and wind inputs

- Grade force `Fg = m*g*sin(theta)`; keep sin(), not tan(), unless slopes are tiny. Percent grade p -> `theta = atan(p/100)`.
- Aero force uses relative speed: `Fa = 0.5*rho*CdA*(v + v_headwind)*abs(v + v_headwind)`. Using `abs` keeps the sign right for tailwinds above vehicle speed.
- Grade should be a function of **distance**, not time: integrate speed to `s` and use a 1-D Lookup Table (Linear interpolation; Clip extrapolation, optionally with the block's "Use last table value for inputs at or above last breakpoint" check box, which needs Linear interpolation and Clip) of `theta(s)`. A time-based profile lets a slower vehicle drive up the wrong hill.
- Smooth profile data (GPS altitude is noisy): resample on a uniform distance grid and low-pass before differentiating.
- Air density from temperature and altitude: `rho = p/(R*T)` with R = 287.05 J/(kg K) (R_universal / M_air = 8.314462618 / 0.0289652, computed).

**Gotchas:** wind sign conventions; define positive headwind explicitly in the interface spec.

## Verify
- [ ] Constant-speed steady state on 5% grade needs power ~ m*g*sin(theta)*v + road load*v.
- [ ] Round trip over the same route returns about the same altitude.
