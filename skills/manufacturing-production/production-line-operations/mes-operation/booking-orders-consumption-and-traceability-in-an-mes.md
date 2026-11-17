---
id: manufacturing-production.production-line-operations.mes-operation.booking-orders-consumption-and-traceability-in-an-mes
name: booking-orders-consumption-and-traceability-in-an-mes
category: manufacturing-production
field: production-line-operations
product: mes-operation
tags: [mes-operation, production-line-operations, mes, manufacturing-execution-system, shop-floor-system, production-order, work-order, order-start, order-confirmation, goods-issue, goods-receipt, consumption-booking, backflush, lot-traceability, batch-traceability, genealogy, barcode-scanning, label-printing, e-work-instructions, electronic-batch-record, erp, sap, isa-95, opcenter, plex, scrap-booking]
level: intro
status: draft
description: "Work an MES from the shop floor: start and confirm orders, scan and book material consumption, record scrap, follow e-work instructions, and keep lot genealogy intact for recalls."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Booking orders, consumption and traceability in an MES

**Goal:** make the system's record match what physically happened on the line — which
order ran, which material lots went into it, how many good and scrap came out — so
stock is right, costs are right and a recall can be traced in minutes. Screens differ
by product (Siemens Opcenter, Rockwell, Plex, SAP ME/DM, in-house systems); the logic
below is common to them. Your site's job aids give the exact clicks.

## 1. How the pieces fit
- The **ERP** (e.g. SAP) owns orders, bills of materials and stock. The **MES** runs
  execution on the floor and reports back. (ISA-95 is the standard model for this
  split.)
- A **production order** says: make *N* of product X, using BOM version Y, routing Z.
- Your bookings in the MES become stock movements in the ERP: **goods issue**
  (material consumed) and **goods receipt** (finished product made).

## 2. Starting an order
1. Select the order **on the line's own terminal** and check product, quantity and
   version against the physical materials and tooling.
2. Log in as **yourself**. Never run on someone else's login: it breaks the audit trail
   and in regulated plants (food, pharma, medical) is a data-integrity violation.
3. **Start** the order before producing. Production run without an active order lands
   on the wrong order or nowhere.
4. Complete any setup checks/sign-offs the MES requires (line clearance, first-off).

## 3. Booking material consumption
- **Scan** each material lot as it is loaded: the pallet/container label barcode,
  not a typed number. Most errors come from keyed lot numbers.
- If the MES rejects a scan ("wrong material", "lot on hold", "expired"), **stop and
  find out** — that check is the point of the system. Don't use an override unless you
  are authorised and record why.
- **Backflush** sites book consumption automatically from the BOM when output is
  confirmed. Then the lot scan is what assigns genealogy; and real usage beyond BOM
  (spills, setup waste) must be booked as scrap or the stock drifts.
- Partly used lots returned to store: book the return with the remaining quantity and
  re-label.

## 4. Confirming output and scrap
- Confirm good quantity at the frequency set (per pallet, per hour, at order end).
  Print the output label from the MES so the lot/serial on the pack matches the
  record.
- Book **scrap with a reason code** at the time it happens, at the operation where it
  happened. End-of-shift guesses ruin both stock and the quality data.
- At order end, **complete/close** the order only when the last good unit is booked;
  some systems block further bookings after close.

## 5. Electronic work instructions and records
- e-WI steps often require a confirm, a measured value or a scan before the next step
  unlocks. Enter real values: the record is legally a production record in regulated
  industries.
- Correct mistakes through the system's correction function (which keeps the original
  and logs who changed it and why), never by re-entering over it.

## 6. Traceability check
Genealogy = for each finished lot, the list of input lots (and vice versa). You should
be able to answer "which customers got product containing raw-material lot R?" in
minutes. Mock recalls test this; bad scans fail them.

## Gotchas
- Two orders open on one line: bookings go to the wrong one. Close or pause the
  previous order at changeover.
- System down: follow the **downtime/paper procedure** and back-enter afterward with
  the paper as evidence — don't rely on memory.
- Label reprints: void the old one, so duplicate labels don't appear in stock.

## Verify
- [ ] Order started on the right line before production; logged in as yourself.
- [ ] Every lot loaded was scanned; no unexplained overrides.
- [ ] Good and scrap counts booked with reasons, matching physical counts.
- [ ] Order closed after the last booking; genealogy shows all input lots.

*Uncertain: menu names and whether consumption is scanned or backflushed depend on
the specific MES and site configuration.*
