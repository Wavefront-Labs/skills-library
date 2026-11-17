---
id: transportation-logistics.postal-courier-delivery.delivery-hub-operations.hub-sort-cycle-and-peak-planning
name: hub-sort-cycle-and-peak-planning
category: transportation-logistics
field: postal-courier-delivery
product: delivery-hub-operations
tags: [delivery-hub-operations, parcel-hub, depot, delivery-station, sort-centre, sort-center, linehaul, trailer-schedule, unload-sort-load, cross-dock, trailer-utilisation, trailer-fill, cut-off, critical-path, peak-season, peak-planning, surge, throughput, pph, headcount-planning, yard-management, dock-doors, black-friday, christmas-peak]
level: practitioner
status: draft
description: "Plan and run a parcel hub's nightly unload-sort-load cycle against linehaul cut-offs, track trailer fill, and size labour and space for peak-season surges."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Hub sort cycle and peak planning

**Goal:** every inbound trailer unloaded, sorted and loaded onto the right outbound
before its departure time, at the planned cost, including during peak weeks when
volume can double.

*Draft: rates and ratios here are illustrative starting points — derive yours from
your site's measured parcels-per-hour (PPH).*

## 1. Map the cycle backwards from departures
1. List outbound departures (linehaul trailers, delivery-van loading waves) with their
   **hard cut-off** times.
2. Work back: departure − load time − sort time = latest time each inbound must be
   unloaded. That gives your **critical inbound arrivals**.
3. Compare against the linehaul schedule. Any inbound arriving after its latest
   unload time is a structural miss — fix the schedule, not the shift.

## 2. Capacity arithmetic
For each stage, capacity = staffed heads × PPH (or machine rate × availability):
```
volume tonight      = 40,000 parcels
sorter rate         = 6,000/hr nominal × 0.85 availability ≈ 5,100/hr
sort window needed  ≈ 40,000 / 5,100 ≈ 7.8 hr
unload heads needed = 40,000 / (window_hr × unload PPH per head)
```
The slowest stage sets the hub's throughput — usually unload (boxes floor-loaded in
trailers) or induction, not the sorter itself.

## 3. Running the night
- **Door plan:** fixed doors for big outbound lanes; inbound doors assigned by arrival
  order. Post it on a board the yard shunter can read.
- **Unload priority:** trailers carrying the most volume for the *earliest* departures
  first, not first-come-first-served.
- **Floor-loaded vs caged/palletised:** floor-loaded trailers take several times longer
  per parcel; put your fastest unloaders and an extendable conveyor there.
- **Outbound loading:** build walls tight floor-to-roof, heavy at the bottom; measure
  **trailer fill %** by eye or sensor at close. Partial trailers are cost; overflows are
  service failures — have a sweep/overflow plan.
- **Hourly check:** volume processed vs plan curve. If behind by >1 hour of work at the
  midpoint, add heads to the bottleneck stage now; at the end it's too late.

## 4. Peak planning (start ~10–12 weeks ahead)
- **Forecast by day**, not by week — Mondays after promotions and the last shipping
  days before holidays dominate.
- **Labour:** agency/temporary staff need induction, safety training and PPE; their PPH
  starts lower, so plan extra heads for the first 1–2 weeks.
- **Space:** overflow trailers in the yard, temporary sort lines, extra cages. Do a
  walk-through with the fire-safety plan: blocked exits are a common peak failure.
- **Linehaul:** extra trailers and sweep runs booked in advance; peak transport is
  scarce and expensive at short notice.
- **Kill-switches:** agree what you drop first if overwhelmed (e.g. defer non-time-
  definite services) before the night it's needed.

## Gotchas
- "The sorter is the bottleneck" is rarely true — measure each stage.
- One late inbound linehaul can miss several downstream departures; know which trailers
  are critical and chase them by phone.
- Yard congestion: count trailer positions you need at the peak hour, not the average.

## Verify
- [ ] Each outbound departure has a worked-back latest-unload time.
- [ ] Tonight's plan names the bottleneck stage and its staffing.
- [ ] Hourly processed-vs-plan is recorded and acted on at the midpoint.
- [ ] Peak plan covers forecast by day, labour ramp, space, linehaul and a drop list.
