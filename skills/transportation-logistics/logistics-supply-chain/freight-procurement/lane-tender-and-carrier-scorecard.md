---
id: transportation-logistics.logistics-supply-chain.freight-procurement.lane-tender-and-carrier-scorecard
name: lane-tender-and-carrier-scorecard
category: transportation-logistics
field: logistics-supply-chain
product: freight-procurement
tags: [freight-procurement, carrier-management, logistics-supply-chain, freight-tender, rfp, rfq, lane-tender, bid-package, rate-negotiation, carrier-selection, 3pl-selection, carrier-scorecard, otp, on-time-performance, tender-acceptance, routing-guide, linehaul, fuel-surcharge, accessorials, award-optimisation, spot-market, contract-rates, kpi, sla]
level: practitioner
status: draft
description: "Run an annual lane tender: clean lane data, build the bid package, analyse bids by total cost, award with capacity and incumbency rules, then manage carriers on a scorecard."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Lane tender and carrier scorecard — buy capacity that actually shows up

**Goal:** get contract rates that carriers will honour, from carriers that perform,
and keep them honest through the year with a small set of measured KPIs.

## 1. Prepare the data (most of the work)
Build a lane file from 12 months of shipment history:
- Lane = origin and destination (zip3/postcode area or city), mode, equipment.
- Annual and weekly volume (loads or kg), with seasonality notes.
- Current incumbent, rate, fuel basis, accessorial spend.
- Facility details: hours, appointment rules, average dwell, live vs drop trailer.
Clean it: merge duplicate locations, drop one-off lanes (<~12 loads/year usually go
to spot/broker), and be honest about volume — overstating it and then under-tendering
destroys carrier trust and next year's acceptance.

## 2. Bid package
- Instructions, timeline (typically 2–3 rounds over 4–8 weeks), award date.
- Rate format fixed: all-in linehaul per load or per mile/km **excluding** fuel, with
  your fuel surcharge table (e.g. indexed to a published diesel price) stated.
- Accessorial schedule you want quoted (detention after N free hours, stop-off, layover,
  liftgate). Unquoted accessorials come back on invoices later.
- Payment terms, insurance minimums, KPI/SLA expectations, contract term.
- Ask for committed weekly capacity per lane, not just price.

## 3. Analyse bids
- Normalise to a common basis: total landed cost per lane = linehaul + expected fuel +
  expected accessorials.
- Compare against benchmark (market index or your spot history).
- Watch outliers: very cheap bids on head-haul lanes often mean poor acceptance later.
- Round 2: share anonymised position ("you're 8% above best") rather than full
  competitor rates.

## 4. Award
Use rules, not just lowest price:
- Primary + 1–2 backups per lane; cap any single carrier's share of a lane at e.g.
  70–80% to keep fallback capacity.
- Weight incumbency and scorecard history — switching has a cost (onboarding, EDI,
  facility familiarity).
- Award optimisation (solver or spreadsheet with constraints) helps once you have
  hundreds of lanes: minimise cost subject to capacity per carrier and min/max carriers.
- Load awards into the TMS routing guide with effective dates the same day.

## 5. Scorecard and governance
Measure monthly, review quarterly (QBR) with top carriers:
| KPI | Typical definition |
|---|---|
| Tender acceptance | accepted / tendered at contract rate |
| On-time pickup / delivery | within appointment window |
| Tracking compliance | loads with timely status updates |
| Invoice accuracy | invoices passing audit first time |
| Claims ratio | claims value / freight spend |
Share the data both ways — carriers will point to your dwell times; measure those too.
Act on it: shift volume toward good performers rather than just scolding.

## Gotchas
- Contract rate below market in a tight market → rejections → spot freight at a premium.
  Track "routing-guide depth" (how far down you go before acceptance).
- Mixing fuel inside linehaul makes later comparison impossible.
- Shipper behaviour (long dwell, late loads) is priced in next round — fix your docks.
- Mini-bids mid-year for lanes that fail are normal; don't wait for the annual tender.

## Verify
- [ ] Lane file reconciles to 12-month spend within a few percent.
- [ ] Every awarded lane has primary + backup loaded in the TMS.
- [ ] Bid comparison uses total cost incl. fuel and accessorials.
- [ ] Scorecard KPIs defined in writing and shared with carriers.
- [ ] Acceptance and spot-spend trend reviewed monthly.

*Uncertainty:* thresholds (low-volume cut-off, share caps) are common practice, not rules — adapt to network size.
