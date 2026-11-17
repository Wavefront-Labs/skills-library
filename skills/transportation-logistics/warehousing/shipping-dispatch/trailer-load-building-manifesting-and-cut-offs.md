---
id: transportation-logistics.warehousing.shipping-dispatch.trailer-load-building-manifesting-and-cut-offs
name: trailer-load-building-manifesting-and-cut-offs
category: transportation-logistics
field: warehousing
product: shipping-dispatch
tags: [shipping, dispatch, outbound, staging, load-building, trailer-loading, load-plan, weight-distribution, axle-weights, load-securing, load-bars, airbags, stop-sequence, lifo, manifest, end-of-day-manifest, parcel-carrier, ltl, ftl, bill-of-lading, seal, cut-off, carrier-pickup, ship-confirm, asn-outbound, proof-of-loading]
level: practitioner
status: gated
description: "Getting orders out the door: staging by route and cut-off, building trailer loads (weight distribution, stop sequence, securing), manifesting, sealing and ship-confirming before the carrier leaves."
sources: ["https://www.ecfr.gov/current/title-49/section-393.102", "https://www.fmcsa.dot.gov/regulations/cargo-securement"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Trailer load building, manifesting and cut-offs

**Goal:** every packed order gets on the right truck before it leaves, loaded so it
arrives intact and legally, with the carrier and customer knowing exactly what's on it.

## 1. Plan backwards from cut-offs
- List carrier departures/pickups with **cut-off times** (last pallet on the trailer,
  last parcel scanned, manifest closed). Work back: loading time, packing time, picking
  time → wave release times (see WMS skill).
- Display a countdown per door/carrier on the dock; escalate at T-60 and T-30 if volume
  is behind.

## 2. Staging
- Dedicated staging lanes per door/route/carrier, marked on the floor, sized for a
  full trailer's worth.
- Stage in **reverse stop order** for multi-drop routes (last drop staged to load
  first — LIFO).
- Scan pallets/cartons into the staging lane; the WMS shows what's missing for each
  load.

## 3. Building the load
- **Weight distribution:** heavy pallets low and spread along the trailer, not all at
  the nose or tail; keep axle weights within legal limits (many trailers: keep the CG
  near the middle). Use the load plan from the TMS/WMS for full trailers.
- **Stackability:** only stack pallets marked stackable; heavier under lighter.
- **Stop sequence:** first drop at the doors. Don't bury a first-drop pallet.
- **Fill gaps** and **secure:** load bars/straps, airbags/dunnage in voids, especially at
  the rear and around partial loads. Loads must withstand braking (0.8 g forward) and
  cornering (0.5 g sideways) — breaking-strength basis in 49 CFR 393.102 (EN 12195-1 (gated: unconfirmed, source is paywalled or blocked)); US rules also set lower working-load-limit forces (0.435 g forward, 0.25 g lateral)
  performance criteria.
- Temperature loads: pre-cool trailer, check setpoint, leave airflow gaps at walls/ceiling.
- Photograph the load before closing (proof of loading condition).

## 4. Manifesting and documents
- **Parcel:** every package scanned to the carrier's manifest; close the manifest
  (end-of-day) and transmit **before** the driver leaves; print the summary/pickup
  scan sheet for the driver to sign.
- **LTL/FTL:** bill of lading with piece count, weight, freight class (US LTL),
  hazmat information if any; driver signs for piece count ("shipper load and count"
  where applicable).
- Export loads: commercial invoice, packing list, export declaration references.

## 5. Seal and confirm
1. Close doors, apply a numbered **seal**, record it on the BOL and in the system.
2. **Ship-confirm** in the WMS: triggers outbound ASN to the customer, invoicing and
   inventory relief.
3. Release the trailer: dock lock off, signals to the driver.

## Gotchas
- Late parcels added after manifest close won't be scanned in → "lost" shipments.
- Pallets wrapped poorly shed cartons in transit — wrap with tension, include the
  pallet in the bottom wraps.
- Overweight axles can be fined or turned back at weigh stations.
- *Freight class, axle limits and securing rules vary by country/state; check local rules.*

## Verify
- [ ] Every order for the departure staged and scanned to its load.
- [ ] Weight distributed and the load secured against forward and side movement.
- [ ] Manifest closed and transmitted; BOL signed with piece count.
- [ ] Seal number recorded; ship-confirm posted before the truck left.
- [ ] Load photographed before the doors closed.

## Checked

Jurisdiction: United States (FMCSA 49 CFR 393) with EU reference. Checked 2026-10-25 on eCFR 393.102: breaking strength 0.8 g forward, 0.5 g rearward and lateral; working load limit 0.435 g forward, 0.5 g rearward, 0.25 g lateral. EN 12195-1 and the European best practice guidelines were not read. Carrier cut-off and manifest practices are operational and carry no checkable figures.

Method: documentation only; no commands were run.
