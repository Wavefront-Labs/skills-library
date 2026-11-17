---
id: transportation-logistics.navigation-wayfinding.route-planning.constraint-based-route-selection
name: constraint-based-route-selection
category: transportation-logistics
field: navigation-wayfinding
product: route-planning
tags: [route-planning, route-selection, trip-planning, navigation-wayfinding, constraints, alternate-route, contingency-planning, checkpoints, escape-routes, timing, time-estimate, naismith, weather-window, daylight, fuel-planning, range, bailout, go-no-go, decision-points, gpx, caltopo, komoot, google-maps, multi-modal, risk-assessment]
level: intro
status: draft
description: "Plan a route for any mode: list hard constraints, compare candidate routes, estimate time with margins, add checkpoints and decision points, prepare alternates and escape routes, and share the plan."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Constraint-based route selection — choose the path before you move

**Goal:** pick a route that meets your hard limits (time, range, legality, capability,
weather, daylight), estimate it honestly, and build in decision points and alternates
so that a surprise becomes a plan change, not an emergency. Works for walking, driving,
riding, boating or flying; mode-specific detail lives in the sibling skills.

## 1. Define the trip and the hard constraints
Write down, before looking at maps:
- **Start, destination, must-visit points**, and deadline (arrival by / back by).
- **Capability:** slowest person, vehicle limits (range, height/weight, ground
  clearance), skills (scrambling, night driving, IFR).
- **Rules:** road restrictions, permits, closed areas, airspace, traffic separation
  schemes, private land.
- **Environment:** daylight hours, forecast, tides, seasonal hazards (snow, heat,
  flood), traffic peaks.
- **Resources:** fuel/charge/energy, water, food, communications coverage.
Anything that would make a route impossible is a constraint; everything else is a
preference.

## 2. Generate 2–3 candidate routes
- Use a planner suited to the mode (road: Google/Apple/HERE maps with avoid options;
  outdoors: CalTopo, Komoot, OS Maps, Gaia; sea/air: chart/flight planning tools).
- Don't accept the first suggestion: generate alternatives that trade distance against
  safety, scenery, ascent, traffic, exposure or facilities.
- Check each against every hard constraint. Discard failures.

## 3. Estimate time honestly
- Base speed per segment by terrain/road type, not one average. Walking:
  Naismith (5 km/h + 1 min per 10 m ascent); driving: planner time + 10–20% for
  stops and traffic; long trips: add breaks (e.g. 15 min every 2 h).
- Add a **margin** (often 20–30%) for the unknown; more in winter or with groups.
- Compare the result with daylight and deadlines. If the margin can't fit, change the
  plan now — shorten, start earlier, or choose the other route.

## 4. Checkpoints and decision points
- Split the route into legs ending at recognisable **checkpoints** with a planned time.
- Mark **decision points**: places where you can still choose an alternate cheaply
  (before a mountain pass, the last fuel station, the harbour before an open crossing).
- Set **turn-around/go-no-go criteria** in advance: "if we're not at the col by 13:00,
  we descend"; "if wind > 25 kn forecast, take the inner route". Decide them when calm.

## 5. Alternates and escape routes
- For each leg: where do you go if weather turns, someone is hurt, or a road is closed?
  Nearest exits, shelters, safe harbours, diversion airfields, hospitals.
- Keep fuel/energy reserves to reach the alternate, not just the destination
  (e.g. aviation-style fixed reserve; for EVs, charge to reach the next two chargers).

## 6. Package and share the plan
- Route file (GPX/KML) on devices, plus a paper summary: legs, distances, times,
  bearings/roads, checkpoints, decision rules, alternates, emergency numbers.
- Leave the plan with a responsible person with a **check-in time** and what to do if
  you miss it.
- Brief companions: they should know the decision points too.

## 7. Execute and adapt
At each checkpoint, compare actual vs planned time. Being significantly slower early
usually gets worse — act at the decision point, not after it.

## Gotchas
- Planner shortest-time routes over unsuitable roads (single-track, unpaved, seasonal).
- Ignoring the return leg's time when it's an out-and-back.
- Phone-only plans with no offline map or battery reserve.
- "Summit fever" — skipping your own turn-around time.

## Verify
- [ ] Hard constraints listed; chosen route passes all of them.
- [ ] Time estimate per leg with margin fits daylight/deadline.
- [ ] Checkpoints, decision points and turn-around criteria written.
- [ ] Alternate/escape for each leg; reserves sufficient to reach it.
- [ ] Plan and check-in time shared with someone not on the trip.

*Uncertainty:* margins and speed figures are rules of thumb; calibrate them against your own logged trips.
