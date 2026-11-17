---
id: transportation-logistics.warehousing.warehouse-management-systems.wave-release-rf-tasks-and-exception-queues
name: wave-release-rf-tasks-and-exception-queues
category: transportation-logistics
field: warehousing
product: warehouse-management-systems
tags: [wms, warehouse-management-system, sap-ewm, manhattan-active-wm, blue-yonder, oracle-wms, korber, infor-wms, netsuite-wms, wave-planning, wave-release, waveless, order-streaming, replenishment, rf-gun, rf-scanner, task-interleaving, short-pick, exception-queue, inventory-transactions, allocation, cut-off, shift-supervisor]
level: practitioner
status: draft
description: "Running a WMS shift: building and releasing waves against carrier cut-offs, triggering replenishment first, supervising RF task queues, and clearing short-pick and allocation exceptions."
sources: ["Vendor documentation concepts: SAP EWM (waves, warehouse tasks), Manhattan Active WM (order streaming)", "Frazelle, World-Class Warehousing and Material Handling", "Practitioner experience patterns (generic)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Wave release, RF tasks and exception queues

**Goal:** turn the day's orders into work that finishes before each carrier cut-off,
keep pickers productive, and stop exceptions from silently piling up. Terms are
generic; SAP EWM, Manhattan, Blue Yonder, Oracle and Körber WMS all have equivalents
(wave/warehouse task/order streaming/exception workbench).

## 1. Before the first wave
- Check the **order pool**: count orders and lines by carrier/service and cut-off time,
  priority (expedites), and holds (credit, address, inventory).
- Check **inventory health**: open cycle-count discrepancies, locked locations,
  quarantined stock — they cause short picks.
- Check **labour**: who's in, on which equipment, which zones.

## 2. Build and release waves (or streams)
1. Group orders by **cut-off first** (latest truck/parcel pickup), then by pick zone or
   carrier. Earliest cut-off goes first.
2. Size each wave to finish in a set time (e.g. 60–90 minutes) at the zone's
   measured rate: lines ÷ (pickers × lines/hour).
3. **Run replenishment before (or with) the wave** — allocation against pick faces
   that are almost empty creates short picks. Most WMSs can calculate wave-demand
   replenishment; release those tasks first and give them priority.
4. Release; check allocation results: **unallocated lines** need a decision (backorder,
   allocate from reserve, substitute, split shipment) before pickers reach them.
5. Waveless/streaming systems release continuously; the same logic applies via
   priority rules and cut-off-based sequencing.

## 3. Supervise RF task queues
- Watch the task monitor: tasks open by type (replen, pick, putaway, move), age, and
  assigned user. Old tasks = stuck work.
- **Task interleaving** (putaway on the way to a pick) improves travel, but disable it
  near cut-off if it delays picks.
- Productivity outliers: low → equipment, training, bad path; very high → check
  accuracy (skipped scans).
- Enforce **scan discipline**: location, item, quantity, and LPN/carton scans; no
  manual keying except with a supervisor override that is logged.

## 4. Exception queues (clear them every hour)
- **Short picks**: picker found less than expected. Steps: verify location
  (neighbouring slots, overflow), trigger an immediate cycle count, re-allocate from
  reserve, and adjust inventory only after the count. Never let pickers "zero out"
  without count.
- **Damaged/unpickable stock**: move to a hold location, record reason.
- **Unassigned or failed tasks**: reassign or cancel with reason.
- **Orders stuck in status** (picked not packed, packed not shipped): walk the flow.
- **Interface errors** (orders not received from ERP, ship confirmations not sent
  to carrier/ERP): escalate to IT before cut-off.

## 5. End of shift
- All waves closed or carried over deliberately; ship confirmations sent; open
  exceptions handed over with owner.

## Gotchas
- Releasing all orders at once floods pick faces and congests aisles.
- Inventory adjustments posted to "fix" a short without investigation hide theft and
  process errors (see inventory control).
- System clock/time zone settings affect cut-off logic in multi-site WMS.

## Verify
- [ ] Waves sequenced by carrier cut-off and sized to the zone's capacity.
- [ ] Replenishment tasks completed before pickers reach those faces.
- [ ] Unallocated lines decided before release ends.
- [ ] Exception queues reviewed hourly; no task older than your threshold.
- [ ] All shipments confirmed to carriers and ERP before shift end.
