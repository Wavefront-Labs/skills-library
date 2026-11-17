---
id: engineering-technology.automotive-vehicle-engineering.powertrain-design.shift-schedule-design
name: shift-schedule-design
category: engineering-technology
field: automotive-vehicle-engineering
product: powertrain-design
tags: [shift-schedule, shift-map, upshift, downshift, kickdown, hysteresis, shift-hunting]
level: practitioner
status: gated
description: "Design upshift and downshift curves versus accelerator position and speed with hysteresis, economy/sport maps and adaptive overrides to avoid hunting."
sources:
  - "Naunheimer et al., Automotive Transmissions"
  - "Guzzella and Sciarretta, Vehicle Propulsion Systems"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Shift schedule design

1. Base axes: vehicle speed (or output speed) vs accelerator pedal position (or torque demand).
2. Economy map: upshift as early as possible while keeping the engine near the best BSFC island and with margin for the requested torque (check torque reserve at the target gear).
3. Power map: shift near peak power speed for performance/sport.
4. Hysteresis: downshift line well below the upshift line (typically 5-15 km/h gap, depends on gears (gated: unconfirmed, source is paywalled or blocked)) to avoid shift cycling.
5. Kickdown: pedal beyond a threshold (or rapid pedal rate) forces downshift to the gear with the highest available wheel force.
6. Adaptations: grade and load (hold gear uphill), driving style, cold/hot temperature, brake (downshift for engine braking), cornering.
7. Constraints: shift time, minimum time in gear, clutch/converter lock-up.
8. Validate with drive cycles and real-road drives; log shift counts and pedal behaviour.

**Gotchas:** shift busyness on motorways, torque reserve ignored.

## Verify
- [ ] Shift count per hundred km on a mixed route is within target.
- [ ] No upshift followed by a downshift within a set time at constant pedal.
