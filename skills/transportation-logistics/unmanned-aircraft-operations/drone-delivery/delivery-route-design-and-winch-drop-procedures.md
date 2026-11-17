---
id: transportation-logistics.unmanned-aircraft-operations.drone-delivery.delivery-route-design-and-winch-drop-procedures
name: delivery-route-design-and-winch-drop-procedures
category: transportation-logistics
field: unmanned-aircraft-operations
product: drone-delivery
tags: [drone-delivery, uav-delivery, last-mile, medical-delivery, route-design, ground-risk, overflight-of-people, population-density, winch-delivery, tether-lowering, parachute-drop, delivery-zone, drop-zone, payload-mass, center-of-gravity, network-scheduling, battery-swap, turnaround, hub-and-spoke, customer-communication, bvlos]
level: practitioner
status: draft
description: "Running drone delivery: routing around ground risk, sizing delivery zones, executing winch and drop deliveries safely, and scheduling a hub network for battery and turnaround limits."
sources: ["JARUS SORA v2.5 ground-risk methodology", "Public operator material on winch/tether delivery (e.g. Wing, Zipline, Manna) and medical-delivery programmes", "FAA Part 135 drone air-carrier certification public descriptions"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Delivery route design and winch/drop procedures

**Goal:** get a package to a doorstep or clinic by drone with predictable risk to the
people below and a delivery that lands where the customer expects it. Builds on
`transportation-logistics.unmanned-aircraft-operations.bvlos-operations.c2-link-detect-and-avoid-and-contingency-planning`.

## 1. Route design
- Start from **ground risk**: overlay population density (census + daytime activity
  data), roads, schools, hospitals, gatherings. Prefer routes over fields, rivers,
  rail corridors and industrial land; cross busy roads perpendicularly.
- Respect airspace: controlled zones, helipads (hospitals!), restricted areas.
- Set cruise altitude high enough for obstacles and noise reduction but within
  approval limits; consistent altitudes by direction reduce conflicts between your own
  aircraft.
- Build **corridors**, not single lines — with contingency volume and emergency
  landing spots every few hundred metres to a few km.
- Validate with test flights: logged C2 quality, GNSS quality, wind behaviour around
  terrain.

## 2. Delivery zone selection
- Minimum clear area: depends on method — a winch delivery may need a ~2–4 m clear
  circle under a hovering aircraft with clearance above (no trees/wires), a parachute
  drop a much larger zone for drift (tens of metres).
- Customer-designated zones checked by imagery and, for new addresses, by a first
  approach that aborts if obstructions are detected.
- No deliveries onto roofs, balconies, roads or into pools.

## 3. Winch/tether delivery procedure
1. Arrive at delivery altitude (e.g. ~20–50 m above the zone), hold position, check
   the zone is clear (downward camera; people > safe distance).
2. Lower the package on the tether at a controlled speed; slow down near the ground.
3. Detect touchdown (tension drop), release the hook, retract.
4. **Abort conditions:** person/animal approaching, tether snag (tension spike or
   no payout), excessive swing in wind, GNSS degradation — cut the hold and climb;
   tether has a weak link / cut device for snags.
5. Confirm delivery to the customer (photo, app notification).

## 4. Parachute drop
- Compute release point from wind at drop altitude and parachute descent rate (e.g.
  ~5 m/s); release upwind by drift distance.
- Package designed to survive the landing; contents rated for shock.

## 5. Payload and aircraft
- Weigh every parcel; enforce max mass and dimensions; centre of gravity inside limits
  (an off-centre load changes hover power and yaw authority).
- Battery: plan each sortie with outbound + hover + return + reserve; hot weather and
  headwinds cut range.

## 6. Network scheduling
- Hub-and-spoke: aircraft, batteries and loaders at the hub. Throughput limited by
  **turnaround time** (battery swap, load, preflight) and charging capacity.
- Stagger departures to avoid queues in airspace and over the hub.
- Time-window promises to customers should include weather holds; communicate
  delays proactively.

## Gotchas
- Wind gusts near buildings swing tethered packages — set a lower wind limit for winch
  deliveries than for cruise.
- Dogs and children run toward drones — instruct customers and abort decisively.
- Noise complaints come from repeated routes; vary or raise routes where allowed.
- *Distances above are illustrative; operators set them from their own tests and approvals.*

## Verify
- [ ] Route corridors avoid high-density areas or carry a documented mitigation.
- [ ] Each delivery zone verified clear for the method used.
- [ ] Winch abort conditions briefed and implemented in software.
- [ ] Parcel mass and CG checked for each flight.
- [ ] Turnaround and charging capacity support the scheduled sortie rate.
