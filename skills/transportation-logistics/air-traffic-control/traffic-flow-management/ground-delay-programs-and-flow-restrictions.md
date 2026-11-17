---
id: transportation-logistics.air-traffic-control.traffic-flow-management.ground-delay-programs-and-flow-restrictions
name: ground-delay-programs-and-flow-restrictions
category: transportation-logistics
field: air-traffic-control
product: traffic-flow-management
tags: [air-traffic-control, atc, traffic-flow-management, tfm, atfm, atfcm, ground-delay-program, gdp, ground-stop, edct, ctot, slot, calculated-takeoff-time, miles-in-trail, mit, minutes-in-trail, reroute, playbook, airport-acceptance-rate, aar, capacity, demand, network-manager, eurocontrol, ccfp, collaborative-decision-making, cdm, a-cdm]
level: advanced
status: docs-checked
description: "Balance demand and capacity: estimate acceptance rates, size a ground delay program or slot regulation, apply miles-in-trail and reroutes, and revise as conditions change."
sources: ["https://www.fly.faa.gov/", "https://www.eurocontrol.int/service/network-manager"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ground delay programs and flow restrictions

**Goal:** absorb unavoidable delay on the ground (cheap, safe) instead of in the air
(expensive, risky), with the smallest total delay that keeps sectors and airports
within capacity.

> Draft: illustrated with US (GDP/EDCT/MIT, FAA ATCSCC) and European (Network Manager
> regulations/CTOT) concepts. Tools, parameters and authority differ by country;
> the arithmetic below is a simplified planning aid, not the production algorithm.

## 1. Estimate capacity honestly
- **Airport acceptance rate (AAR)** — arrivals per hour the runways can take in the
  forecast conditions. Example: a single runway at 5 NM spacing and ~140 kt
  groundspeed gives about 140 / 5 ≈ 28 arrivals/hour in theory; mixed departures,
  wake gaps and IMC push it lower (calibrate from your own historical rates).
- **Sector capacity / monitor alert value** — max aircraft per hour (or occupancy)
  the controllers can handle.
- Take the forecast seriously: the main errors come from weather timing (fog lift,
  thunderstorm onset) — build the plan around the forecast window and its uncertainty.

## 2. Measure demand
Pull scheduled + filed arrivals per 15-minute bin. Compare with capacity per bin.
Where demand exceeds capacity for more than a bin or two, a program is likely needed.

## 3. Sizing a ground delay program (worked logic)
1. Program window: e.g. 1400–1900 local, AAR 30/h vs demand 42/h.
2. Excess = 12/h × 5 h = 60 flights to shift. Assign arrival slots at 2-minute
   intervals (60 / 30) in order of original scheduled arrival (ration-by-schedule).
3. Each flight's **delay = slot time − original ETA**; its departure time (EDCT/CTOT)
   = slot − estimated en-route time.
4. **Scope**: include flights from airports close enough to hold on the ground; very
   long-haul or already-airborne flights are exempt and take their delay in holding or
   speed control.
5. Watch the **average and max delay**; if the max is unacceptable, consider a
   reroute, a lower-AAR shorter program, or diversions planning with operators.

## 4. Other tools
- **Ground stop**: immediate halt of departures to a destination for short, severe
  events — high impact; set an end time and review it.
- **Miles-in-trail (MIT)/minutes-in-trail**: spacing on a stream crossing a boundary,
  e.g. "20 MIT over fix X". Simple to apply but can cascade upstream; specify exactly
  which flows and altitudes it covers.
- **Reroutes/playbooks**: move flows around convective weather or closed airspace;
  check the receiving sectors can take them.
- **Level capping**: keep short flights low to protect high sectors.

## 5. Running and revising
- Publish clearly: cause, window, rate, scope, expected average delay.
- Use **collaborative decision making**: operators substitute and cancel flights
  within their slots; freed slots compress the program.
- Re-forecast every ~30–60 min (an operating practice, not a rule). Extend, revise the rate, or cancel early — a program
  held after the weather cleared wastes delay.
- Monitor **compliance**: departures outside their EDCT/CTOT window break the plan.

## Gotchas
- Over-conservative AAR is invisible to controllers but costs thousands of delay
  minutes; under-conservative pushes airborne holding and diversions.
- Stacked restrictions (MIT on top of a GDP) double-penalise the same flights.
- Exempt traffic still lands — subtract it from capacity before allocating slots.

## Verify
- [ ] Capacity and demand were compared per 15-minute bin, not per hour only.
- [ ] Slot spacing equals 60 / AAR minutes and exempt flights were accounted for.
- [ ] Each restriction has a stated cause, scope, start, end and review time.
- [ ] The program was revised or cancelled when the forecast changed.
- [ ] Compliance with issued departure times was monitored.

## Checked

Jurisdiction: US FAA ATCSCC (GDP, EDCT, MIT) and EUROCONTROL Network Manager (CTOT) concepts. Checked 2026-10-25 by recomputation: 140 kt at 5 NM spacing is 28 arrivals per hour; 12 per hour excess over 5 hours is 60 flights; slot spacing 60/30 is 2 minutes. The skill states terms and illustrative rates only and gives no regulatory thresholds; the planning practices (15-minute bins, re-forecast interval) are operational advice and are described as such.

Method: documentation only; no commands were run.
