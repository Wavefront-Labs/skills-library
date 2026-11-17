---
id: transportation-logistics.warehousing.receiving-putaway.dock-receipt-verification-and-putaway-logic
name: dock-receipt-verification-and-putaway-logic
category: transportation-logistics
field: warehousing
product: receiving-putaway
tags: [receiving, inbound, goods-in, putaway, dock-scheduling, asn, advance-ship-notice, purchase-order, receipt-verification, blind-receiving, over-short-damage, osd, discrepancy, lpn, license-plate, lot-control, expiry, fefo, quality-hold, directed-putaway, fixed-location, random-location, unloading, trailer-seal, carrier-signature]
level: practitioner
status: draft
description: "Taking goods in correctly: dock appointments, seal and condition checks, verifying against ASN/PO (or blind), recording over/short/damage, labelling LPNs, and directed putaway rules."
sources: ["Frazelle, World-Class Warehousing and Material Handling", "GS1 standards for SSCC labels and Despatch Advice (ASN)", "Practitioner receiving SOP patterns (generic)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Dock receipt verification and putaway logic

**Goal:** every unit that enters the building is the right item, in the right quantity,
in sellable condition, recorded in the system, and stored where it can be found —
because every error at receiving multiplies downstream.

## 1. Before the truck arrives
- **Dock appointments** with time slots per door; check the ASN (advance ship notice)
  or PO lines for the load: items, quantities, lots/expiry, SSCC pallet labels.
- Prepare: door, labour, MHE, and staging space sized to the load.
- Flag special handling: temperature, hazmat, high-value, quality inspection required.

## 2. At the door
1. Check paperwork (bill of lading/CMR) matches the appointment and PO/ASN.
2. **Seal check:** record the seal number and confirm it matches the paperwork and is
   intact *before* breaking it. Broken/mismatched seal → photograph, note on the
   carrier's document, escalate.
3. Inspect the trailer: temperature (reefer readout and probe a product), damage,
   wet floors, load shift, pests.
4. Secure the trailer (dock lock/chocks) before unloading — see forklift skill.

## 3. Unload and verify
- **ASN receiving:** scan SSCC pallet labels; for trusted suppliers with good history,
  receive at pallet level and sample-check cartons. Untrusted → open and count.
- **Blind receiving:** counters record what they find without seeing the expected
  quantity — slower but catches more errors; use for new suppliers or problem lines.
- Verify per line: item (scan barcode, don't read the description), quantity, unit of
  measure (case vs. each — a classic 12× error), lot and expiry, condition.
- Record **OS&D** (over, short, damaged) on the carrier's delivery document **before
  the driver leaves**, with photos; notations like "subject to count" protect claims
  only where agreed.
- Damaged or suspect goods → quality hold location, not stock.

## 4. Label and record
- Every pallet/case gets an **LPN** (licence plate) linking it to the receipt in the WMS.
- Confirm receipt in the WMS promptly so the stock is available and the ERP sees it
  (dock-to-stock time is a key KPI; targets often < 24 h, best sites hours).

## 5. Putaway logic
- **Directed putaway:** WMS suggests a location by rules — item velocity zone, product
  class (hazmat segregation, temperature), weight (heavy low), lot rules (FEFO/FIFO),
  location capacity (cube and weight), and consolidation with existing stock where
  allowed.
- Options: **fixed** (each item has a home — easy for people, wastes space),
  **random/dynamic** (any suitable empty location — best space use, depends on
  scanning), or hybrid (fixed pick faces + random reserve).
- **Cross-dock** inbound that's already allocated to outbound orders (see cross-docking).
- Operator scans the location barcode to confirm; system won't accept a different
  location without an override reason.

## Gotchas
- Accepting "said to contain" pallets without counting high-value items.
- Supplier relabelled cartons with wrong barcodes — scan and compare to PO item.
- Receipts backlogged at the dock make stock invisible, causing false backorders.
- *Thresholds and trusted-supplier rules are site policy; set them from your error data.*

## Verify
- [ ] Seal number recorded and checked before opening.
- [ ] Item, quantity, UOM, lot/expiry verified per line (or per sampled carton for trusted ASN).
- [ ] OS&D noted on carrier paperwork with photos before the driver left.
- [ ] Every pallet labelled with an LPN and received in the WMS.
- [ ] Putaway confirmed by location scan; dock-to-stock time measured.
