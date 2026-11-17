---
id: manufacturing-production.cnc-machining-production.multi-axis-machining-setup.five-axis-work-offsets-tcp-and-collision-proving
name: five-axis-work-offsets-tcp-and-collision-proving
category: manufacturing-production
field: cnc-machining-production
product: multi-axis-machining-setup
tags: [multi-axis-machining-setup, 5-axis, five-axis, 3-plus-2, positional-5-axis, simultaneous-5-axis, 4th-axis, trunnion, table-table, head-head, kinematics, pivot-point, centre-of-rotation, machine-calibration, kinematic-calibration, tcp, tcpm, rtcp, g43-4, traori, tilted-work-plane, g68-2, cycle800, plane-spatial, work-offsets, tool-reach, gauge-length, collision-avoidance, machine-simulation, vericut, mill-turn, cnc-machining-production]
level: advanced
status: draft
description: "Set up and prove 4/5-axis and mill-turn work: kinematic calibration, one work offset with TCP/tilted planes, tool reach and gauge length planning, and simulation on a true machine model."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Five-axis work offsets, TCP and collision proving

**Goal:** run 3+2 and simultaneous 5-axis jobs from a **single work offset**, with the
control handling the rotary geometry, and prove them in simulation so the first
real run is boring.

*Draft: code names vary — FANUC `G43.4`/`G68.2`, Heidenhain `M128`/`FUNCTION TCPM`/
`PLANE SPATIAL`, Siemens `TRAORI`/`CYCLE800`, Haas `G234`/`G254` (DWO). Availability
depends on purchased options and correct kinematics data from the builder.*

## 1. Kinematics and calibration
- Know your machine type: **table-table** (trunnion), **head-table**, or **head-head**.
  The control needs exact pivot/rotary-centre data to compute TCP and tilted planes.
- Run the **kinematic calibration** routine (e.g. Heidenhain KinematicsOpt, Renishaw
  AxiSet, Siemens CYCLE996, builder-specific cycles with a probe and a datum sphere)
  on a schedule and after any crash. Thermal growth and a minor crash both move
  pivot points; errors multiply with distance from the rotary centre.
- Check rotary axis backlash and clamping behaviour (clamped for 3+2, unclamped for
  simultaneous).

## 2. Work offsets: one datum, control does the maths
- Set **one work offset** on the part (usually with rotaries at zero) and let the
  control's tilted-plane function (`G68.2`, `PLANE SPATIAL`, `CYCLE800`) or dynamic work
  offset handle every other orientation.
- The alternative — a separate offset per face, each set by hand — multiplies setup time
  and error. Use it only on controls without the option.
- The CAM post must know which method is used; post output and machine setup must match.
- Probe the part datum with the rotaries at the orientation where you'll set it; the
  probe cycle must be compatible with the active plane.

## 3. TCP (tool centre point control)
- In simultaneous 5-axis, **TCP/TCPM/RTCP** (`G43.4`, `M128`, `TRAORI`) makes the control
  keep the tool tip on the programmed path as rotaries move; the program is in part
  coordinates and independent of tool length.
- Without TCP the post must output pivot-compensated coordinates for one specific tool
  length — change the tool or stick-out and the part is wrong. Avoid for production.
- Feed rate in simultaneous moves: inverse-time (`G93`) or the control's TCP feed mode
  — follow the post.

## 4. Tool reach planning
- Choose holders and stick-out for **clearance at the worst orientation**, not the
  average. Shrink-fit/slim holders and extensions are common.
- Record **gauge length** for every tool in the CAM tool library; simulation is only
  valid if gauge lengths match the tool presetter's values.
- Shortest tool that clears: every extra mm of stick-out reduces rigidity sharply
  (deflection scales with length cubed).

## 5. Simulation on a true machine model
- Use **machine simulation** on G-code (post output), not just the CAM toolpath:
  Vericut, CAM-integrated machine sim (Mastercam, NX, hyperMILL, Fusion extension) or
  the control's own 3D simulation.
- Model: machine kinematics and travel limits, table, fixture, clamps, stock, tool
  holders. Turn on near-miss checks (e.g. 2–5 mm clearance), not just contact.
- Watch for **axis limit flips** (rotary hits limit and unwinds mid-cut) and
  singularities near B/A = 0 on some kinematics, causing rapid C rotations.

## 6. First run
- Rotary-axis moves at very low rapid override; verify orientation by eye before each
  feature. Keep a hand on feed hold.
- Check one feature on each face before running the whole program.

## Gotchas
- Mill-turn: same principles plus turning/milling mode switching and B-axis head tool
  orientation; spindle-to-subspindle collision zones.
- Fixture tall enough for clearance but not so tall it limits travel.
- Re-posting after a post update without re-simulating.

## Verify
- [ ] Kinematic calibration current (date recorded).
- [ ] One part datum; tilted planes/TCP used; post matches.
- [ ] Gauge lengths in CAM match presetter values.
- [ ] G-code machine simulation clean with near-miss checking.
- [ ] First run at reduced rapid with each face checked.
