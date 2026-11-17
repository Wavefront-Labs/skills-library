---
id: engineering-technology.aerospace-engineering.flight-dynamics-control.climb-performance
name: climb-performance
category: engineering-technology
field: aerospace-engineering
product: flight-dynamics-control
tags: [flight-dynamics, aircraft-performance, flight-performance, climb-performance, rate-of-climb, climb-gradient, excess-power, best-climb-speed]
level: practitioner
status: verified
description: "Compute steady climb rate and gradient from thrust, drag and weight, find best-climb speeds and relate them to certification climb gradient requirements."
sources:
  - "Anderson, Aircraft Performance and Design"
  - "Raymer, Aircraft Design"
  - "14 CFR Part 25 section 25.121"
  - "https://www.law.cornell.edu/cfr/text/14/25.121"
  - "https://en.wikipedia.org/wiki/Service_ceiling"
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# Climb performance

**Goal:** rate and gradient of climb for sizing and performance charts.

## Relations (steady, small flight-path angle)
- Climb gradient `gamma = (T - D)/W` (radians; percent gradient `100 gamma`).
- Rate of climb `ROC = V sin(gamma) ~ (T - D) V / W = P_excess / W`.
- `D = (CD0 + K CL^2) 1/2 rho V^2 S`, with `CL = W cos(gamma)/(q S)`.
- Best gradient (steepest climb) occurs near `V` for maximum `T - D`; for a jet it is near the speed of minimum drag (`CL = sqrt(CD0/K)`); best rate occurs at a higher speed where `(T - D) V` peaks. For propeller aircraft constant power gives best rate at minimum power speed (`CL = sqrt(3 CD0/K)`).
- Altitude: thrust lapses and `ROC` falls; absolute ceiling at `ROC = 0`, service ceiling at a specified small `ROC` (a typical definition is 100 ft/min, with about 500 ft/min often used for jets; use the project definition).

## Certification gradients
Part 25 requires minimum climb gradients in takeoff, en-route, approach and landing configurations with one engine inoperative (25.121 to 25.123, 25.119); for example 25.121(b) requires one-engine-inoperative gradients of at least 2.4, 2.7 and 3.0 percent for two-, three- and four-engine airplanes at V2 with gear retracted, and 25.119 requires 3.2 percent in the all-engines landing climb; check the current text for the other segments.

## Procedure
1. Compute `T(V,h)` from the lapse model or engine deck, `D(V,h)` from the polar.
2. Plot `ROC` and gradient vs `V` and find the maxima.
3. Include acceleration factor for climbs at constant Mach or calibrated airspeed.
4. Check against the certification gradients with margin.

## Verify
- [ ] ROC at sea level maximum thrust matches manufacturer-type figures within the model's accuracy.
