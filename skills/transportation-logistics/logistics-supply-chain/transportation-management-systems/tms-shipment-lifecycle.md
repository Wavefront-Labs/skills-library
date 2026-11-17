---
id: transportation-logistics.logistics-supply-chain.transportation-management-systems.tms-shipment-lifecycle
name: tms-shipment-lifecycle
category: transportation-logistics
field: logistics-supply-chain
product: transportation-management-systems
tags: [transportation-management-systems, tms, logistics-supply-chain, shipment-planning, load-tendering, carrier-tender, routing-guide, rate-management, track-and-trace, freight-audit, freight-payment, edi-204, edi-990, edi-214, edi-210, api-tracking, oracle-otm, sap-tm, blue-yonder, manhattan-tms, mercurygate, e2open, ltl, ftl, accessorials, appointment-scheduling]
level: practitioner
status: draft
description: "Run a shipment through a TMS end to end: order to load, routing-guide tender, EDI 204/990/214/210 flow, track-and-trace exceptions and freight audit against the rate."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# TMS shipment lifecycle — order to paid invoice without surprises

**Goal:** move a shipment through a transportation management system (Oracle OTM,
SAP TM, Blue Yonder, Manhattan, MercuryGate, e2open and similar) so the right carrier
gets it at the contracted rate, you see problems before the customer does, and the
invoice matches what was agreed. Screen names differ by vendor; the lifecycle does not.

## 1. Get the master data right first
Most "TMS bugs" are master-data bugs. Before go-live or a new lane, check:
- **Locations:** ship-from/ship-to with correct address, geocode, dock hours,
  appointment requirement, equipment restrictions (no 53' trailers, liftgate needed).
- **Items/order lines:** weight, cube, freight class (US LTL, NMFC), handling units.
  A missing weight makes every rate and load plan wrong.
- **Carriers:** SCAC, modes, equipment, insurance expiry, EDI/API connection status.
- **Rates:** per lane (origin–destination zone), mode, equipment, effective dates,
  fuel surcharge table, accessorials (detention, liftgate, residential, inside delivery).
- **Routing guide:** ranked primary/backup carriers per lane with tender rules.

## 2. Plan: orders → shipments → loads
1. Orders flow in from ERP/OMS (often IDoc, EDI 940/850 or API).
2. Planning consolidates orders into shipments/loads by date window, lane and
   equipment capacity — run the optimiser, then *read its output*: check weight and
   cube utilisation, stop count and whether any order was left unplanned and why.
3. Mode decision: parcel vs LTL vs FTL vs intermodal is usually rule-driven by weight
   and cube breakpoints. Rough US rule of thumb (unconfirmed for your network): above
   ~10–12 pallets or ~10,000 lb, compare a volume-LTL or FTL quote against LTL.

## 3. Tender
- Tender to the routing-guide primary (EDI 204 / API load tender). Set an
  **acceptance window** (commonly 2–4 h for next-day loads).
- Carrier responds accept/decline (EDI 990). On decline or timeout the TMS
  cascades to the next carrier; after the guide is exhausted it goes to spot/broker.
- Watch **tender acceptance rate** per carrier and lane: a primary that rejects
  >10–20% is not really your primary (threshold is a convention, tune it).

## 4. Execute and track
- Appointment scheduling at pickup and delivery docks; store confirmation numbers.
- Status events arrive as EDI 214 or API/ELD/visibility-platform pings (picked up,
  in transit, out for delivery, delivered, exception codes).
- Configure **exception alerts**, not dashboards people forget to look at: missed
  pickup, no ping for N hours, ETA beyond delivery window, temperature alarm.
- Record proof of delivery and any accessorial events (detention start/stop times
  matter for the later invoice dispute).

## 5. Freight audit and settlement
- Carrier invoice arrives (EDI 210 or portal). The TMS rates the shipment
  independently and compares: base, fuel, accessorials.
- Set a tolerance (e.g. auto-approve within $X or Y%); everything else goes to an
  exception queue with reason codes.
- Common discrepancies: reweigh/reclass on LTL, unapproved accessorials, wrong
  fuel index week, duplicate invoices. Fix root causes in master data, not just
  the invoice.
- Accrue freight cost at shipment so finance isn't surprised by late invoices.

## Gotchas
- Effective-dated rates: a new contract loaded with the wrong start date silently
  rates a week of freight at old prices.
- Time zones on appointments and ETAs — check what zone the carrier sends.
- Freight class drives LTL cost; a dimension error can double the price.
- EDI partners need testing per transaction set; a "connected" carrier may only
  send 214s and ignore 204s.
- Don't let users bypass the TMS with phone bookings — it breaks audit and data.

## Verify
- [ ] Sample loads rate correctly against the contract by hand calculation.
- [ ] Tender cascades to backup on decline/timeout in a test.
- [ ] A late or silent shipment raises an alert to a named owner.
- [ ] Invoice audit catches a deliberately wrong accessorial.
- [ ] Tender acceptance, on-time and cost-per-unit KPIs report per lane and carrier.

*Uncertainty:* breakpoints and tolerances above are typical starting points, not
standards; EDI set numbers are ANSI X12 (EDIFACT users map to IFTMIN/IFTSTA equivalents).
