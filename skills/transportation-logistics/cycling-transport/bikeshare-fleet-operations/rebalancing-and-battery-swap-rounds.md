---
id: transportation-logistics.cycling-transport.bikeshare-fleet-operations.rebalancing-and-battery-swap-rounds
name: rebalancing-and-battery-swap-rounds
category: transportation-logistics
field: cycling-transport
product: bikeshare-fleet-operations
tags: [cycling-transport, bikeshare-fleet-operations, bike-share, bikeshare, docked-bikeshare, dockless, e-scooter, micromobility, shared-mobility, rebalancing, redistribution, dock-fill-level, station-occupancy, battery-swap, swap-round, fleet-sweep, low-battery, ops-dashboard, gbfs, service-van, cargo-trailer, damaged-bike, triage, parking-compliance, geofence, demand-patterns, peak-commute, fleet-utilisation]
level: practitioner
status: draft
description: "Keep a shared bike/scooter fleet usable: plan rebalancing routes from station fill levels, run battery-swap rounds, triage damaged vehicles and clear parking problems."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Rebalancing and battery-swap rounds (bikeshare fleet operations)

**Goal:** riders find a bike (or an empty dock) where and when they want it, vehicles
are charged and safe, and the street isn't cluttered with broken or badly parked ones.

> Draft: general practice for docked and dockless systems (bikes and e-scooters).
> Ops dashboards and thresholds are operator-specific; numbers are illustrative.
> GBFS is the public open data feed many systems publish (station status, vehicle status).

## 1. Read the network
- **Station/zone fill level**: bikes available vs docks/capacity. Flag stations
  **< ~20%** (going empty) and **> ~80–90%** (going full).
- **Demand patterns**: morning commute empties residential areas and fills business
  districts; evening reverses it. Hills drain downhill; uphill stations empty.
- Events, weather and holidays shift demand — check the calendar each shift.
- Use the forecast in the ops tool if you have one; otherwise historical patterns per
  hour of day and day of week.

## 2. Plan a rebalancing route
1. List **sources** (overfull) and **sinks** (empty/going empty), prioritising high-demand
   stations that will hit 0 or full **before the next peak**.
2. Van/trailer capacity (e.g. a van carrying ~15–25 bikes; e-cargo trailer ~6–10).
3. Build a loop: source → nearest sink(s) → next source, minimising empty driving.
4. **Pre-peak timing**: rebalance residential stations before ~07:00; business district
   docks emptied before ~08:30 so riders can return. Adjust to your city.
5. Don't fully fill a sink — leave docks for returns (e.g. target ~50–60% fill).

## 3. Battery-swap rounds (e-bikes and scooters)
- Pull a list of vehicles below a threshold (e.g. **< 25–30%**), ordered by location and
  expected demand.
- Carry charged batteries in a protected, ventilated rack in the vehicle; secure them —
  no loose batteries rolling around.
- At each vehicle: unlock via the ops app, swap, check the new battery registers, quick
  safety check (brakes, lights, tyre), relock, mark complete.
- Depleted batteries go back to the **charging room**, which needs fire detection,
  spacing, and no damaged packs on chargers.

## 4. Fleet sweep and triage
- **Sweep**: walk/ride a zone collecting vehicles that are damaged, mis-parked, or
  out of geofence.
- **Triage** every flagged vehicle:
  - *Ride-safe* (cosmetic) → leave in service.
  - *Minor fix* (flat, loose bell, light) → fix on the street if quick.
  - *Unsafe* (brakes, frame, battery damage, steering) → mark out of service in the app
    immediately and remove to the depot.
- User damage reports are leads, not truth — verify on site.

## 5. Parking compliance and the street
- Re-park blocking vehicles (footways, ramps, building entrances, tactile paving).
- Respect city permit rules: maximum response times for complaints, fleet caps,
  no-parking zones.
- Photograph before/after for complaints and city reporting.

## 6. Shift handover
- Report: stations still critical, vehicles removed, batteries charged/in charge,
  incidents, vandalism hotspots.
- Update the dashboard statuses before you leave — the next shift plans from it.

## Gotchas
- Rebalancing that chases the last hour's map arrives too late; plan for the next peak.
- Swapping without checking registration leaves "charged" vehicles reporting empty.
- Damaged lithium batteries can ignite days later: isolate them, don't charge them.
- Over-filling docks blocks returns and riders end trips far away, making it worse.

## Verify
- [ ] Each shift began with a fill-level list of critical stations/zones.
- [ ] Rebalancing targets the next peak, leaving room for returns.
- [ ] Every swapped battery registered and the vehicle passed a quick safety check.
- [ ] Unsafe vehicles were marked out of service before being moved.
- [ ] Handover notes and dashboard statuses are current.
