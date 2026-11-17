---
id: transportation-logistics.logistics-supply-chain.inventory-distribution-planning.dc-replenishment-and-allocation
name: dc-replenishment-and-allocation
category: transportation-logistics
field: logistics-supply-chain
product: inventory-distribution-planning
tags: [inventory-distribution-planning, logistics-supply-chain, drp, distribution-requirements-planning, replenishment, reorder-point, min-max, s-s-policy, order-up-to, eoq, safety-stock, fair-share-allocation, stock-deployment, multi-echelon, service-level, fill-rate, days-of-cover, inventory-turns, excess-and-obsolete, dc, distribution-centre]
level: practitioner
status: draft
description: "Set DC replenishment parameters (reorder point, order-up-to, EOQ), run DRP netting from forecast, allocate scarce stock fairly, and track fill rate vs days of cover."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# DC replenishment and allocation — the right stock in the right building

**Goal:** keep each distribution centre (DC) or store able to fill orders at the target
service level with as little stock as possible, and decide sensibly who gets stock
when there isn't enough.

## 1. Pick a replenishment policy per segment
| Policy | When | Rule |
|---|---|---|
| Reorder point (s, Q) | continuous review, steady items | when position ≤ s, order Q |
| Periodic order-up-to (R, S) | weekly ordering cycles, many SKUs per supplier | every R, order S − position |
| Min-max (s, S) | lumpy, store/branch stock | when ≤ min, order up to max |
**Inventory position** = on hand + on order − backorders − committed. Ordering off
on-hand alone double-orders.

Parameters:
- Reorder point `s = d × L + SS` (demand per period × lead time + safety stock).
- Order-up-to `S = d × (R + L) + SS_(R+L)` — safety stock covers review period plus lead time.
- **EOQ** `Q = √(2 D K / h)` (annual demand, cost per order, holding cost per unit-year).
  Round to pack/pallet multiples and check it against shelf life and space.
- Safety stock from the S&OP skill (`z × σ_error × √L`); see
  transportation-logistics.logistics-supply-chain.supply-chain-planning.forecast-to-sop-cycle.

## 2. DRP netting (multi-DC from one source)
For each SKU-DC, by week:
1. Gross requirement = forecast (or orders if larger in the frozen zone).
2. Projected on hand = previous + scheduled receipts − gross requirement.
3. If projected on hand < safety stock → planned receipt (lot-sized), offset by
   transit lead time into a planned shipment from the supplying DC/plant.
4. Sum planned shipments by source → becomes the source's dependent demand.
Run weekly, firm the next 1–2 weeks, and let the rest float.

## 3. Allocation when supply is short
- **Fair share:** give each location stock so all reach the same days of cover:
  target cover = (total available + Σ location on hand) / Σ daily demand; ship each
  location up to target cover × its demand, minus its own stock.
- Priority overrides: strategic customers, contractual service levels, or locations
  with no alternative source first — agree the rule in S&OP, not on the phone.
- Hold back a small central reserve for slow-moving items rather than pushing them
  into every node (pooling reduces total safety stock roughly with √(number of nodes)
  when demand is independent).

## 4. Deployment decisions
- Push (forecast-driven) for seasonal pre-builds and long lead times; pull
  (replenish on consumption) for stable fast movers.
- Fast movers decentralised near customers; slow movers centralised.
- Re-balance between DCs only when transfer cost < expected stock-out or markdown cost.

## 5. Measure
- **Fill rate** (units or lines shipped complete from stock / ordered) — the customer view.
- **Days of cover / weeks of supply** and **inventory turns** — the cash view.
- Plot them together per SKU segment: high cover + low fill = wrong stock in wrong place.
- Excess & obsolete: stock beyond N months cover or no movement in 6–12 months — review monthly.

## Gotchas
- Lead time means the *whole* lead time: order cycle, supplier, transit, receiving, put-away.
- MOQ and pallet rounding can add more stock than safety stock does; include it in reviews.
- Allocating by order date ("first come") rewards customers who over-order.
- Phantom inventory (system says yes, shelf says no) breaks every rule; cycle-count A items often.

## Verify
- [ ] Each SKU-location has a policy and parameters recalculated within the last quarter.
- [ ] Ordering uses inventory position, not on-hand.
- [ ] DRP planned shipments reconcile to source supply plan.
- [ ] Allocation rule written and applied in the last shortage.
- [ ] Fill rate and days of cover reported side by side per segment.

*Uncertainty:* √n pooling holds only for independent, similar demand; use simulation for real networks.
