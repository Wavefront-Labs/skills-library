---
id: transportation-logistics.rail-operations.train-handling.slack-control-and-gradient-braking
name: slack-control-and-gradient-braking
category: transportation-logistics
field: rail-operations
product: train-handling
tags: [train-handling, slack-action, slack-control, run-in, run-out, in-train-forces, buff-forces, draft-forces, stretch-braking, power-braking, gradient-braking, undulating-territory, crest, sag, brake-point, minimum-reduction, eco-driving, energy-efficient-driving, coasting, das, driver-advisory-system, trip-optimizer, leader, train-driver, locomotive-engineer]
level: advanced
status: draft
description: "Manage a long train's mass: keep slack stretched or bunched deliberately over crests and sags, pick brake points, brake on grades without exhausting air, and drive for energy efficiency."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Slack control and gradient braking

**Goal:** move a long, heavy train over varied terrain with low in-train forces (no
broken knuckles, no derailments from buff), accurate stops and minimum energy.

*Draft: this is the shared craft; detailed limits (minimum reductions, stretch-braking
practice, dynamic axle limits) are railroad-specific. Simulator time with a qualified
instructor is how this is actually learned.*

## 1. Think of the train as a spring
- Each coupler has free slack (a few cm); across 100+ cars that's several metres. The
  train is either **stretched** (couplers in draft) or **bunched** (in buff).
- Transitions between stretched and bunched produce run-in/run-out shocks. The craft
  is: **choose the state, change it gently, keep it through the terrain.**
- Heavy cars behind light cars, and empties at the head of loads, make forces worse.

## 2. Read the profile, not just the section you're on
A long train spans several gradients at once. Before every crest or sag, ask: where is
the *mass* of the train, and which way will slack want to go?
- **Over a crest:** the head end starts descending while the rear still climbs. Reduce
  power progressively before the crest so the head end doesn't run away from the rear;
  begin light dynamic as the head end goes over, so slack bunches gently.
- **Through a sag:** head end climbing, rear descending → the rear runs in. Keep a
  little power on (stretched) through the dip, or keep a light dynamic and let it
  bunch deliberately — just don't switch states in the bottom.

## 3. Braking on grades
- **Dynamic first** for speed control (see
  transportation-logistics.rail-operations.mainline-locomotives.locomotive-traction-and-dynamic-braking).
- **Stretch braking** (light air application with power on to keep slack out) is used
  on some railroads in specific conditions; others restrict it — follow your rules.
- Make the **minimum reduction early**, add in small steps; avoid release-and-reapply
  cycles on long descents (each cycle costs recharge you may not get back).
- Watch speed trend, not speed: if speed is still rising after an application, add more
  now.

## 4. Choosing brake points
- Learn fixed markers for each regular stop and restriction (bridge, mile post).
- Adjust for weight, length, gradient, adhesion and dynamic availability.
- A good stop: one application, small adjustments, released or held per rules, no
  surge at the end.

## 5. Energy-efficient running
- **Coast early** to restrictions and stations instead of powering then braking.
- Use **driver advisory systems** (DAS, Trip Optimizer, LEADER-style) as advice: they
  calculate when to coast and power to meet the timetable with least energy. You still
  own the safety decisions.
- Arrive on time, not early — early arrival is wasted energy.

## Gotchas
- Applying the train brake while in heavy power with a bunched train can cause severe
  run-out.
- Undesired emergency applications (UDEs) often follow rough handling — slow down your
  control changes first before blaming equipment.
- Simulators teach patterns, but each train is different: feel the first few control
  changes before committing.

## Verify
- [ ] For each crest and sag on your route you can say where the slack will go and
      what you'll do about it.
- [ ] Descents completed without brake release/re-apply cycling.
- [ ] Stops made with one primary application.
- [ ] Event recorder/DAS data show no harsh slack events and reasonable energy use.
