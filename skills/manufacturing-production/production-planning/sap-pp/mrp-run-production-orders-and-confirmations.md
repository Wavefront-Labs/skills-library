---
id: manufacturing-production.production-planning.sap-pp.mrp-run-production-orders-and-confirmations
name: mrp-run-production-orders-and-confirmations
category: manufacturing-production
field: production-planning
product: sap-pp
tags: [sap-pp, sap, s4hana, sap-ecc, production-planning, mrp, mrp-live, md01n, md04, stock-requirements-list, md06, mrp-list, exception-messages, planned-order, co40, co41, production-order, co01, co02, co03, release-order, goods-issue, mb1a, migo, confirmation, co11n, co15, goods-receipt, backflush, material-master, mm02, mrp-type, lot-size, bom, cs03, routing, ca03, work-center, cm01, capacity-levelling, cm21]
level: practitioner
status: draft
description: "Plan production in SAP PP: check master data, run MRP (MD01N/MD04), convert planned orders to production orders, release, issue, confirm (CO11N) and read capacity load."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SAP PP: MRP run, production orders and confirmations

**Goal:** take demand through SAP PP to a confirmed production order, reading the
system's signals correctly and keeping master data from silently ruining the plan.

*Draft note:* transaction codes are the classic SAP GUI ones (ECC and S/4HANA); many
S/4HANA sites use Fiori apps instead (e.g. *Monitor Material Coverage*, *Manage
Production Orders*). Customising, authorisations and order types are site-specific.

## 1. Master data that drives everything
Before trusting any MRP result, check for the material:
- **Material master (MM03/MM02), MRP views:** MRP type (e.g. PD = MRP, VB =
  reorder point, ND = no planning), **MRP controller**, **lot-sizing procedure**
  (EX lot-for-lot, FX fixed, WB weekly, HB replenish to max), min/max/rounding lot,
  **procurement type** (E in-house, F external), **in-house production time** or
  routing-based scheduling, **safety stock**, planned delivery time.
- **BOM (CS03)** — valid for the date and quantity, right usage (production), scrap
  percentages.
- **Routing (CA03)** — operations, work centres, standard values (setup, machine,
  labour).
- **Production version** (in S/4HANA mandatory for MRP sourcing) linking BOM and routing.
- **Work centre (CR03)** — capacity and formulas used by scheduling and capacity load.
Most "SAP planned it wrong" complaints trace back to one of these fields.

## 2. Run MRP and read the result
- **MD01N** (MRP Live, S/4HANA) or MD01/MD02/MD03 (classic) — total plant, single
  material, or single-level. Typical setting: net change planning, create planned
  orders, schedule lead times.
- **MD04 Stock/Requirements List** — the planner's main screen: one line per receipt
  or requirement with dates, quantities and running available quantity. Refresh it;
  it is a snapshot.
- **MD06/MD05 MRP list** and exception groups: work the **exception messages** — e.g.
  *reschedule in/out*, *cancel process*, *start date in the past*, *safety stock
  violated*. Triage by impact (customer order first), not by count.
- Fix master data errors you find; don't keep overriding planned orders by hand to
  compensate.

## 3. Planned order → production order
- Convert from MD04 or individually (**CO40**) or collectively (**CO41**). Check dates,
  quantity and production version.
- **CO02** to change; **CO03** display. Check component availability (**availability
  check** in the order) — a missing part now saves a stopped line later.
- **Release** the order (CO02 release, or mass release via **COHV**). Released status
  (REL) allows goods issue and confirmation; print shop papers if used.
- **Goods issue** components (MIGO with movement type 261, or **backflush** at
  confirmation if the components are flagged for it).

## 4. Confirmations
- **CO11N** — time ticket confirmation per operation: yield, scrap, rework, activity
  times, partial/final. **CO15** confirms the whole order (simpler, less detailed).
- Final confirmation of the last operation can trigger the **goods receipt**
  automatically (if the control key and settings say so) and backflushed components.
- Check for **confirmation errors** (COGI — failed goods movements, e.g. no stock to
  backflush). Unprocessed COGI items mean stock and costs are wrong.
- Technically complete (TECO) orders that will not run further so they stop
  appearing as open supply in MRP.

## 5. Capacity
- **CM01** work-centre load by period; **CM21/CM25** capacity levelling (planning
  table) where used. Infinite MRP scheduling ignores capacity; overloads show here
  and must be resolved by moving orders, overtime or alternative work centres.

## Gotchas
- Old open orders and stale planned orders distort MRP: TECO/clean them.
- A safety stock set in two places (master + planning) double-counts.
- Backflush without accurate BOM scrap → negative or drifting stock.
- Firm planned orders (firming indicator/time fence) are not changed by MRP — know
  which orders are firmed.

## Verify
- [ ] MRP-relevant master data checked for the material and its components.
- [ ] MD04 reviewed after the run; exception messages triaged.
- [ ] Production orders created with correct version, components available, released.
- [ ] CO11N confirmations entered; COGI empty.
- [ ] Capacity load (CM01) shows no unresolved overloads in the frozen horizon.
