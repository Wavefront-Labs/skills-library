---
id: engineering-technology.aerospace-engineering.propulsion-engineering.engine-sizing-thrust-requirements
name: engine-sizing-thrust-requirements
category: engineering-technology
field: aerospace-engineering
product: propulsion-engineering
tags: [propulsion, engine-installation, engine-certification, engine-sizing, thrust-to-weight, constraint-diagram, oei-climb, second-segment]
level: practitioner
status: gated
description: "Size engine thrust from takeoff field length, one-engine-inoperative climb gradients, climb and cruise requirements on a thrust-to-weight versus wing-loading chart."
sources:
  - "Raymer, Aircraft Design: A Conceptual Approach"
  - "Mattingly, Heiser and Pratt, Aircraft Engine Design"
  - "14 CFR Part 25 section 25.121"
  - "https://www.law.cornell.edu/cfr/text/14/25.121"
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# Engine sizing

**Goal:** the sea-level static thrust needed at the aircraft level.

## Constraint-diagram method
For each requirement compute the thrust-to-weight `T/W` as a function of wing loading `W/S`:
- **Takeoff field length:** from a correlation or a numerical integration of ground roll, rotation, and the climb to 35 ft; thrust lapse at takeoff.
- **One-engine-inoperative climb (second segment):** minimum climb gradient with one engine inoperative under 25.121(b): 2.4% for two-engine, 2.7% for three-engine and 3.0% for four-engine airplanes, at V2, landing gear retracted, critical engine inoperative (14 CFR 25.121(b)(1), eCFR checked October 2026). `T/W = (N/(N-1)) (gradient + 1/(L/D))` per engine count `N`, with takeoff thrust and lapse.
- **Top-of-climb:** residual rate of climb at initial cruise altitude, with thrust lapse.
- **Cruise:** `T/W = 1/(L/D)` times lapse correction at cruise.
- **Landing/approach climb (go-around)** and balked landing gradients.

## Procedure
1. Compute constraint lines on a chart of `T/W_SLS` vs `W/S`.
2. The feasible region lies above all lines and left of the stall/landing wing loading limit.
3. Choose `W/S` for the design (balance cruise efficiency and field performance), read the required `T/W`.
4. Multiply by takeoff weight for the total thrust; select engine rating (flat rating, derate possibility) and count.

## Gotchas
- Thrust lapse models (see lapse skill) drive the answer; use engine data when available.
- Takeoff temperature (hot and high) typically sizes the engine.

## Verify
- [ ] A twin-jet transport result falls around 0.25-0.35 T/W (check against similar aircraft) (gated: unconfirmed, source is paywalled or blocked).
