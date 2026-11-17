---
id: transportation-logistics.logistics-supply-chain.network-design.facility-location-and-cost-to-serve
name: facility-location-and-cost-to-serve
category: transportation-logistics
field: logistics-supply-chain
product: network-design
tags: [network-design, logistics-network-design, logistics-supply-chain, facility-location, warehouse-location, center-of-gravity, centre-of-gravity, milp, mixed-integer-programming, p-median, flow-path, cost-to-serve, mode-mix, supply-chain-design, coupa-supply-chain-guru, anylogistix, optilogic, pulp, python, scenario-analysis, baseline-model, service-radius]
level: advanced
status: draft
description: "Model a logistics network: build and validate a baseline, centre-of-gravity screen, MILP facility location with service constraints, flow-path and cost-to-serve analysis, scenario comparison."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Facility location and cost-to-serve — redesign the network on evidence

**Goal:** decide how many facilities, where, serving which customers by which mode,
by building a model that first reproduces today's cost and then compares scenarios.

## 1. Build the baseline (don't skip)
Collect 12 months of:
- Demand by customer/ship-to (aggregate to postcode/zip3 or 3-digit areas — a few
  hundred to a few thousand demand points is plenty), by product family, with weight/cube.
- Supply points (plants, suppliers, ports) and their capacity.
- Facilities: fixed cost (rent, staff base), variable handling cost per unit, capacity.
- Transport rates by mode as functions of distance and weight (fit from actual invoices:
  e.g. FTL cost = fixed + rate × km; LTL/parcel by weight band and zone).
Model today's flows and compare to actual P&L: total within ~5% and each major cost
bucket roughly right. If not, the model's scenarios aren't trustworthy.

## 2. Quick screen: centre of gravity
Weighted mean location: `x* = Σ wᵢxᵢ / Σ wᵢ` (same for y; use projected coordinates
or great-circle iteration — lat/long averaging distorts at large scales). Weight by
outbound tonnage × rate. Useful to see roughly where 1–3 sites "want" to be; it ignores
roads, labour and existing sites, so treat as a starting candidate list, not an answer.

## 3. MILP facility location
Decision variables: `open_j ∈ {0,1}`, `flow_ij ≥ 0` (facility j to customer i).
Minimise `Σ fixed_j·open_j + Σ (handling_j + transport_ij)·flow_ij + inbound costs`
subject to: demand met for every i; `flow_ij ≤ demand_i·open_j`; capacity per j;
service constraint (e.g. ≥95% of demand within 1-day transit or N km);
optional single sourcing (each customer from one DC).
Python sketch with PuLP (Tested with PuLP 3.3.2 (`pip install "pulp<4"`): PuLP 4.0 is a rewrite in which variables are created from the problem (`m.add_variable`) and `pulp.LpStatus` no longer exists, so these snippets fail there.):
```python
m = pulp.LpProblem("net", pulp.LpMinimize)
y = pulp.LpVariable.dicts("open", J, cat="Binary")
x = pulp.LpVariable.dicts("flow", [(i,j) for i in I for j in J], lowBound=0)
m += pulp.lpSum(F[j]*y[j] for j in J) + pulp.lpSum(c[i,j]*x[i,j] for i in I for j in J)
for i in I: m += pulp.lpSum(x[i,j] for j in J) == D[i]
for i in I:
    for j in J: m += x[i,j] <= D[i]*y[j]
for j in J: m += pulp.lpSum(x[i,j] for i in I) <= Cap[j]*y[j]
m.solve()
```
Commercial tools (Supply Chain Guru, anyLogistix, Optilogic) wrap the same idea with
richer cost and multi-echelon structure.

## 4. Scenarios to run
- Number of DCs: solve for 1..N forced open; plot total cost vs count — the curve is
  usually flat near the optimum, so pick for service and risk within the flat zone.
- Mode mix: more FTL to regional pools vs direct LTL/parcel.
- Demand growth +/−20%, fuel +30%, labour cost by region, lease-break timing.
- Cost-to-serve: allocate all costs back to customers/channels; often reveals a tail
  of small-drop customers that cost more to serve than they earn.

## 5. Decide
Present total landed cost, service coverage, one-off transition costs (moving stock,
severance, IT), payback and risk (single points of failure). Validate shortlisted sites
on the ground: labour market, access, zoning, flood risk.

## Gotchas
- Inventory cost rises with more DCs (safety stock per node) — include it.
- Linear transport costs understate small shipments; use stepwise or fitted curves.
- Optimising average week hides peak capacity needs.
- Aggregated demand points far from real addresses distort last-mile cost.

## Verify
- [ ] Baseline reconciles to actual costs within ~5% overall.
- [ ] Each scenario differs from baseline by stated, documented changes only.
- [ ] Service constraint checked post-solve on real transit times.
- [ ] Sensitivity shows the recommendation survives demand and fuel swings.

*Uncertainty:* the 5% reconciliation target is practitioner convention; PuLP sketch omits inbound and multi-product detail.
