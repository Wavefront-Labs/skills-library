---
id: energy-mining-utilities.energy-storage-operations.storage-dispatch.scheduling-battery-charge-discharge-and-services
name: scheduling-battery-charge-discharge-and-services
category: energy-mining-utilities
field: energy-storage-operations
product: storage-dispatch
tags: [storage-dispatch, dispatch, scheduling, day-ahead, intraday, energy-arbitrage, price-spread, charge-discharge-window, ancillary-services, frequency-response, fcas, ffr, regulation, reserve, capacity-market, revenue-stacking, soc-headroom, cycle-budget, throughput, warranty, degradation, availability-declaration, bid, offer, optimiser, round-trip-efficiency, bess, battery-trading]
level: practitioner
status: draft
description: "Schedule a storage asset: build a day-ahead charge/discharge plan, stack ancillary services without overcommitting SOC, budget cycles against warranty, and declare availability honestly."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Scheduling battery charge, discharge and services

**Goal:** turn market prices and grid-service contracts into a schedule the storage
asset can actually deliver, without breaching warranty limits or SOC constraints.

> Status: draft. Market products, gate closure times and penalty regimes differ by
> market (e.g. UK, Australian NEM, ERCOT, CAISO); this is the cross-market logic, not
> any market's rules. Many sites use an optimisation platform or a third-party trader.

## 1. Know the asset's constraints
- **Power (MW)** and **usable energy (MWh)** at the point of connection — after
  auxiliary load, transformer losses and any offline equipment.
- **Round-trip efficiency** (often around 85% AC-to-AC for lithium-ion at the meter;
  confirm yours): you must buy more MWh than you sell.
- **Warranty limits:** cycles per day/year, energy throughput, SOC range, average SOC,
  temperature. Breaching them can void warranty or capacity guarantees.
- **Grid connection limits:** import and export caps, ramp rates.

## 2. Build the day-ahead plan
1. Look at forecast prices; find the cheapest charging window and the most valuable
   discharge window(s). The spread must beat losses and degradation cost:
   discharge price × RTE − charge price > degradation cost per MWh.
2. Fit charge and discharge blocks to the energy available, including ramp times.
3. Check SOC trajectory hour by hour stays inside the usable window.
4. Leave **headroom** for services you've committed to (next section).

## 3. Stacking services
- Frequency response or reserve needs reserved MW **and** enough energy in the
  right direction for the required duration. A 10 MW/1 h service for 15 minutes
  needs 2.5 MWh above the minimum SOC (for discharge-direction service) plus margin.
- **Never sell the same MW twice** unless the market explicitly allows co-optimised
  stacking; double commitment is the commonest scheduling error and leads to penalties.
- Build the energy trade around the service: the service usually constrains SOC; trades
  fill what's left.

## 4. Cycle budgeting
- Translate the warranty into a **cycle or throughput budget** per month and track it.
  A day with small spreads may be worth sitting out to save cycles for volatile days.
- Track **degradation** (capacity tests, SOH from the BMS) against the warranty curve.

## 5. Intraday and real time
- Re-optimise when prices, forecasts or availability change. Watch actual SOC against
  plan; frequency service activity moves SOC unpredictably, so recover it in the next
  available window.
- If the plant derates (thermal, faults), **re-declare availability promptly** to the
  system operator. Declaring capability you don't have is a compliance breach.

## 6. Record and review
After each day: planned vs actual MWh, revenue by product, penalties, cycles used,
availability. Use them to tune bid strategy and SOC margins.

## Gotchas
- Forgetting auxiliary consumption makes the SOC plan optimistic.
- Clock/settlement period mismatches (5 vs 30 min) create imbalance charges.
- Price forecasts are wrong on the days that matter most; keep flexibility.

## Verify
- [ ] Constraints (MW, MWh, RTE, warranty, grid) entered correctly.
- [ ] SOC trajectory feasible with headroom for each service.
- [ ] No MW committed twice.
- [ ] Cycle budget tracked month to date.
- [ ] Availability re-declared on any derate.
