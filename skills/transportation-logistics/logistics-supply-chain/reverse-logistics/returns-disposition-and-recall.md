---
id: transportation-logistics.logistics-supply-chain.reverse-logistics.returns-disposition-and-recall
name: returns-disposition-and-recall
category: transportation-logistics
field: logistics-supply-chain
product: reverse-logistics
tags: [reverse-logistics, returns-management, logistics-supply-chain, rma, return-merchandise-authorisation, returns-processing, disposition, grading, refurbishment, restock, liquidation, recycling, weee, product-recall, recall-logistics, traceability, lot-tracking, chain-of-custody, return-to-vendor, rtv, returns-portal, ecommerce-returns, cost-per-return]
level: practitioner
status: draft
description: "Run the return flow: RMA rules, receiving and grading, disposition decision tree (restock, refurb, RTV, liquidate, recycle), credit timing, and executing a traceable product recall."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Returns disposition and recall — recover value fast, prove control

**Goal:** process returns quickly enough to recover value (a returned item loses value
every week it sits), decide each item's best next destination with a rule rather than
opinion, and run a recall where every affected unit is accounted for.

## 1. Front door: authorise and route
- **RMA / return authorisation** captures order, item, reason code, condition claim,
  and pre-assigns a destination (central returns centre vs vendor vs local store).
- Reason codes must be few and mutually exclusive (e.g. damaged in transit, defective,
  wrong item shipped, no longer wanted, size/fit). They drive root-cause fixes upstream.
- For low-value items, test "**returnless refund**" (refund, customer keeps/donates) —
  if return shipping + handling > recoverable value, don't move the item at all.

## 2. Receive and grade
1. Scan the RMA/label → match to order; log arrival date (it starts the credit clock).
2. Inspect against a written **grading standard**, with photos:
   - A: unopened/as new → restock as new
   - B: opened, complete, works → open-box / refurbished-light
   - C: cosmetic damage or missing parts → refurb or parts
   - D: defective/unsafe → RTV, repair or recycle
3. Data wipe for devices with user data (and record it — chain of custody).
4. Flag fraud patterns: wrong item returned, empty boxes, serial mismatches.

## 3. Disposition decision tree
Pick the destination with the highest **net recovery** = expected resale value −
processing − transport − holding time cost:
1. Restock to sellable inventory (A grade, current season).
2. Return to vendor (RTV) for credit when the vendor agreement allows; batch shipments
   to cut freight, but watch claim deadlines.
3. Refurbish/repair → resell as refurbished.
4. Secondary channels: outlet, marketplace, liquidator (by pallet/lot).
5. Donate.
6. Recycle/dispose under regulation (e.g. WEEE for electronics in the EU, battery rules);
   keep certificates of destruction for branded or regulated goods.
Encode the tree in the WMS/returns system by item category so receivers aren't guessing.

## 4. Credit and data
- Customer refund timing is a promise and sometimes a legal requirement (e.g. EU
  distance-selling refunds within 14 days of return/proof of dispatch — check current
  local law).
- Report weekly: return rate by SKU and reason, dock-to-disposition time, recovery %
  of original value, cost per return.
- Feed defects and "not as described" reasons back to product and content teams —
  prevention is the cheapest reverse logistics.

## 5. Product recall
1. **Scope:** identify affected lots/serials/date codes from production and
   traceability records; map where they went (DCs, stores, customers) — one step
   forward, one step back at minimum.
2. **Stop:** system block (quality hold) on affected stock everywhere in one action.
3. **Notify:** customers, channel partners and regulators per the applicable rules
   (food, consumer products, medical devices each have their own regulator and timelines).
4. **Retrieve:** dedicated return channel, labelled packaging, quarantine area;
   reconcile units back vs units shipped by lot.
5. **Dispose/repair** with documented evidence; report effectiveness (% recovered).
Run a mock recall annually: can you trace a lot to every customer within a few hours?

## Gotchas
- Restocking without regrading puts damaged items back into outbound picks.
- Returns centres fill up after peak season — plan labour for January.
- Liquidating branded goods into the wrong channel can undercut your own prices.
- Recall success is limited by traceability data quality captured at shipping.

## Verify
- [ ] Every return has a reason code and grade with photo evidence.
- [ ] Disposition rules exist per category and are applied by the system.
- [ ] Dock-to-disposition time tracked (target days, not weeks).
- [ ] Mock recall traced a lot end to end within the target time.

*Uncertainty:* refund deadlines and disposal regulations vary by country and product category.
