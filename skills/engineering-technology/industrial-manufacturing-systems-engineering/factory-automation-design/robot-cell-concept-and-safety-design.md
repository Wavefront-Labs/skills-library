---
id: engineering-technology.industrial-manufacturing-systems-engineering.factory-automation-design.robot-cell-concept-and-safety-design
name: robot-cell-concept-and-safety-design
category: engineering-technology
field: industrial-manufacturing-systems-engineering
product: factory-automation-design
tags: [robot-cell, robotic-cell, automation-concept, cell-layout, cycle-time, cycle-time-budget, robot-selection, payload, reach, end-of-arm-tooling, eoat, gripper, machine-tending, machine-safety, risk-assessment, iso-12100, iso-13849, performance-level, plr, iso-13855, safety-distance, light-curtain, iso-10218, iso-ts-15066, cobot, collaborative-robot, iso-13857, iso-14119, guarding, interlock, functional-safety, robodk, process-simulate]
level: advanced
status: draft
description: "Concept a robot cell: cycle-time budget, robot and gripper sizing, cell layout, and safety design via ISO 12100 risk assessment, ISO 13849 PL and ISO 13855 safety distances."
sources:
  - "ISO 12100, Safety of machinery: general principles for design, risk assessment and risk reduction"
  - "ISO 13849-1, Safety-related parts of control systems"
  - "ISO 13855, Positioning of safeguards with respect to approach speeds of the human body"
  - "ISO 10218-1 and ISO 10218-2, Robotics: safety requirements"
  - "ISO 13857, Safety distances to prevent hazard zones being reached"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Robot-cell concept and safety design

**Goal:** a cell concept that provably meets cycle time, with a robot sized with
margin and a safety design derived from a risk assessment, before anyone buys hardware
or writes a line of robot code.

## 1. Write the requirement
Parts and variants, rate (takt), part presentation in and out, quality checks, changeover
needs, available floor space, operator interactions (load, inspect, clear jams) and
uptime target. Every operator interaction is a safety requirement later.

## 2. Build a cycle-time budget
Sequence every motion and wait, then sum the critical path:
- Robot moves: use the vendor's simulation (RobotStudio, ROBOGUIDE, RoboDK, Process
  Simulate) with the real payload; hand estimates from max speed are optimistic,
  because short moves never reach it.
- Gripper actuation and confirm: ~0.2-0.5 s per open/close with sensor feedback.
- Machine time, vision triggers, conveyor index, handshakes.
Example (machine tending, takt 60 s): machine cycle 42 s; robot unload/load swap with a
double gripper 9 s; part to outfeed and return 7 s (done during machining, off the
critical path) → critical path 42 + 9 = 51 s = **85% of takt**. Aim for ≤ ~85% at
concept stage to leave margin for the real world.

## 3. Size robot and tooling
- Payload = part + gripper + adapters + cable dress; check **load inertia and offset**
  against the robot's wrist load diagram, not just the kg figure. Concept margin of
  ~20-30% below rated payload is a sensible starting rule.
- Reach: check every target pose with tool orientation, not just distance from the
  base; avoid working near reach limits and wrist singularities.
- Repeatability (±0.02-0.1 mm typical industrial) vs what the process needs; fixtures
  and vision often matter more than the robot.

## 4. Lay out the cell
Robot base at the centroid of its targets; infeed/outfeed reachable without awkward
wrist flips; operator load stations outside the safeguarded space (turntable or
two-station fixture so loading overlaps robot work); maintenance access to every
component; space for the safeguarding distances computed below.

## 5. Risk assessment (ISO 12100 process)
List tasks in all life phases (normal running, setup, jam clearing, cleaning,
maintenance). Identify hazards (crushing, impact, ejected parts, energy release).
Estimate risk, then reduce in strict order: **inherently safe design → safeguarding →
information for use**. A warning sign never replaces a guard.

## 6. Determine required performance level
For each safety function (door interlock, light curtain, safe speed, e-stop), use the
ISO 13849-1 risk graph: severity S1/S2, exposure frequency F1/F2, possibility of
avoidance P1/P2 → **PLr** a to e. Robot-cell perimeter functions commonly come out at
PLr d (the robot standards also set minimum requirements; check the current ISO 10218
edition, which was revised recently and now incorporates collaborative guidance that
previously sat in ISO/TS 15066). Then design architecture (category, MTTFd, DCavg, CCF)
to achieve PL ≥ PLr and verify it with a tool such as SISTEMA.

## 7. Compute safeguard distances (ISO 13855)
S = K × T + C, with T = sensor response + machine stopping time (measured, worst case).
- K = 2,000 mm/s if S ≤ 500 mm (minimum 100 mm); if the result exceeds 500 mm,
  recompute with K = 1,600 mm/s (minimum 500 mm).
- For a vertical light curtain with resolution d ≤ 40 mm, C = 8 × (d - 14) mm.
Example: 14 mm curtain (C = 0), response 20 ms, robot stop 350 ms → T = 0.37 s;
2,000 × 0.37 = 740 > 500 → 1,600 × 0.37 = **592 mm**. Fixed fences must meet reach
distances (ISO 13857) for their height and opening size. Check these values against the
current edition of ISO 13855; the standard has been revised and details differ by edition.

## Gotchas
- Stopping time grows with speed and payload; measure it at the worst case and
  re-measure after any program or tooling change.
- "Collaborative robot" describes an application, not a robot; a cobot holding a sharp
  part still needs a risk assessment and often guarding.
- Muting and bypass modes are where most accidents happen; design them explicitly.
- Regulatory frameworks (EU Machinery Regulation, OSHA/ANSI RIA in the US) decide
  which standards apply and who signs off; check your jurisdiction.

## Verify
- [ ] Cycle-time critical path from simulation is ≤ ~85% of takt at concept.
- [ ] Payload and inertia checked against the wrist load diagram with margin.
- [ ] Every life-phase task appears in the risk assessment.
- [ ] Each safety function has a PLr and a calculated achieved PL ≥ PLr.
- [ ] Safeguard distances computed from measured stopping times and drawn on the layout.
