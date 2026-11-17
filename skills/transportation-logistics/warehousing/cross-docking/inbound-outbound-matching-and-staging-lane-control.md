---
id: transportation-logistics.warehousing.cross-docking.inbound-outbound-matching-and-staging-lane-control
name: inbound-outbound-matching-and-staging-lane-control
category: transportation-logistics
field: warehousing
product: cross-docking
tags: [cross-docking, cross-dock, flow-through, pre-distributed, post-distributed, pick-by-line, dock-door-assignment, staging-lanes, inbound-outbound-matching, asn, sscc, dwell-time, consolidation, deconsolidation, hub, ltl-terminal, retail-distribution, appointment-scheduling, yard-management, sorting]
level: practitioner
status: draft
description: "Moving goods dock to dock with no storage: pre- vs post-distributed cross-docking, matching inbound to outbound, door assignment, staging-lane control and keeping dwell time under target."
sources: ["Bartholdi & Gue (2004), The best shape for a crossdock, Transportation Science", "Frazelle, World-Class Warehousing and Material Handling", "GS1 SSCC and Despatch Advice standards"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Inbound-outbound matching and staging-lane control

**Goal:** goods arrive and leave on different trucks within hours, never touching a
storage location — which only works if information arrives before the freight.

## 1. Pick the cross-dock type
- **Pre-distributed:** the supplier labels each pallet/carton for its final destination
  (store) before shipping; you just sort and load. Fastest; needs supplier compliance
  and accurate ASNs.
- **Post-distributed (pick-by-line):** you receive bulk and split it into destination
  quantities on the dock using allocations. More flexible, more labour.
- **Consolidation/deconsolidation:** many small inbound → full outbound (or the
  reverse), typical of LTL terminals and hubs.

## 2. Information first
- Require **ASNs** with SSCC labels **before arrival** (e.g. at dispatch from the
  supplier). No ASN → the freight goes to an exception area and may break the flow.
- Match inbound lines to outbound orders/routes in advance: the WMS/TMS builds a
  **flow plan**: for each inbound pallet/carton, its outbound door and trailer.
- Schedule appointments so inbound arrives just before matching outbound departure
  (often 2–24 h window).

## 3. Door assignment
- Put inbound doors **opposite or close to** the outbound doors they feed most
  (by volume), minimising travel. Re-optimise as the outbound mix changes.
- Put high-volume outbound destinations in the middle of the dock for shortest average
  travel; low-volume ones at the ends.
- I-shaped docks suit smaller operations; larger ones use L/T/X shapes to keep travel
  short with many doors.

## 4. Staging-lane control
- One lane per outbound door/route, clearly marked; capacity = one trailer.
- Scan every pallet/carton into its lane — the system shows completeness per
  outbound load.
- **Never block lanes** with freight waiting for an exception decision; use a
  dedicated exception area.
- Clear lanes in step with departures; a lane that's still full after its truck
  left is a missed shipment.

## 5. Exceptions
- **Unlabelled/unknown freight:** to exception area, identify via supplier/ASN, relabel.
- **Short/over shipments vs. ASN:** note on receipt, re-allocate outbound quantities
  (may short some stores).
- **Missed outbound:** decide quickly: next departure, alternative carrier, or
  temporary storage (and record it as storage — it's no longer a cross-dock flow).
- **Damage:** hold, document, notify; replace from stock if possible.

## 6. Measure
- **Dwell time** (dock-in to dock-out scan) per unit; targets often < 24 h, many
  operations < 4–8 h. Percentage of freight that needed storage. Outbound on-time
  departure rate. Mis-sorts per 1,000 units.

## Gotchas
- Inbound arriving late cascades into many outbound misses — prioritise late inbound
  unloading by the outbound departures it feeds.
- Insufficient dock floor space turns a cross-dock into an accidental warehouse.
- Supplier label compliance needs enforcement (chargebacks, scorecards).
- *Dwell targets vary by industry; set from your service commitments.*

## Verify
- [ ] ASNs received before arrival for ≥ target % of inbound.
- [ ] Every inbound unit has an outbound door assigned before unloading.
- [ ] Lanes scanned and complete before each departure; no exception freight in lanes.
- [ ] Dwell time measured and within target.
