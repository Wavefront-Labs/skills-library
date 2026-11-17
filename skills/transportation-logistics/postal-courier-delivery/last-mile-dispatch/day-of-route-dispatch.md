---
id: transportation-logistics.postal-courier-delivery.last-mile-dispatch.day-of-route-dispatch
name: day-of-route-dispatch
category: transportation-logistics
field: postal-courier-delivery
product: last-mile-dispatch
tags: [last-mile-dispatch, dispatch, dispatcher, route-planning, route-optimisation, route-optimization, vrp, vehicle-routing-problem, driver-allocation, live-rerouting, delivery-windows, time-windows, eta, customer-promise, stops-per-hour, route-density, onfleet, routific, optimoroute, circuit, tms, failed-delivery-rate, otd, on-time-delivery, sla]
level: practitioner
status: draft
description: "Build and run a day's last-mile delivery plan: clean addresses, set realistic stop times, allocate drivers, monitor live ETAs, and re-route around breakdowns without breaking promises."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Day-of route dispatch (last mile)

**Goal:** turn today's orders into routes that drivers can actually complete inside
their hours and the customers' time windows, and keep promises intact when the day
goes wrong.

Tools differ (Onfleet, Routific, OptimoRoute, Circuit, carrier TMS modules); all
solve a vehicle-routing problem with time windows from the same inputs. *Draft:
numbers below are starting assumptions to calibrate against your own history.*

## 1. Clean the inputs (the optimiser is only as good as these)
1. **Geocode check:** sort orders by geocode confidence; fix any that landed on a
   postcode/zip centroid, a street midpoint or the wrong town. One bad pin can add
   30+ minutes to a route.
2. **Time windows:** confirm hard windows (booked slots, business opening hours)
   vs soft preferences. Too many hard windows make routes infeasible.
3. **Service time per stop:** don't use one global number. Typical splits:
   house/letterbox ~1–2 min, apartment block 4–6 min, business with goods-in 5–10 min,
   two-person/large item 10–20 min. Calibrate from POD timestamps.
4. **Vehicle constraints:** capacity (weight, volume/cages), van height for car parks,
   EV range, driver shift length and break rules.

## 2. Build routes
- Run the optimiser, then **inspect every route on the map**: crossing routes,
  zig-zags and one stop far outside the cluster mean bad data or a missing constraint.
- Leave **slack**: plan to ~85–90% of shift length so one delay doesn't cascade.
- Balance on time, not stop count — 120 rural stops ≠ 120 flats.
- **Lock** stops that must be early (medical, perishables) before re-optimising.

## 3. Allocate drivers
- Match routes to drivers' area knowledge where possible; new drivers get denser,
  simpler routes and a check-in at the midpoint.
- Confirm vehicles roadworthy and charged/fuelled before releasing routes.
- Publish routes early enough to support reverse-order loading (see
  transportation-logistics.postal-courier-delivery.parcel-courier-work.multi-drop-parcel-day).

## 4. Live control
Watch a short list, every 20–30 minutes:
| Signal | Response |
|---|---|
| Route running >30 min behind plan | Move a block of stops to a nearby driver ahead of plan |
| Stop with time window at risk | Call/message the customer before the window breaks |
| Driver stationary unexpectedly | Call — breakdown, accident or access problem |
| Failed-delivery spike in one area | Check address data/access codes for that block |

**Re-routing a breakdown:** split the stranded route by geography, hand blocks to the
nearest drivers with capacity, arrange a parcel transfer point (not a roadside swap
in a live lane), and push updated ETAs to customers.

## 5. Customer promises
- Send the ETA window from the live plan, not the static plan; narrow it as the
  driver approaches.
- If a window will be missed, say so before it's missed and offer a rebook.

## 6. Close the day
Review: on-time %, failed-delivery % by reason, planned vs actual stop times. Feed
actual service times back into tomorrow's parameters.

## Gotchas
- Optimisers love left-turn/U-turn-heavy paths if road restrictions aren't loaded.
- Driver breaks inserted at the wrong place push every afternoon window late.
- Re-optimising mid-day reshuffles stops drivers already loaded for — move blocks
  instead.

## Verify
- [ ] No low-confidence geocodes left in today's plan.
- [ ] Every route has visible slack and was visually inspected.
- [ ] At-risk windows were contacted before they broke.
- [ ] Actual stop times fed back into service-time parameters.
