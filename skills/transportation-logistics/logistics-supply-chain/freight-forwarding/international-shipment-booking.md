---
id: transportation-logistics.logistics-supply-chain.freight-forwarding.international-shipment-booking
name: international-shipment-booking
category: transportation-logistics
field: logistics-supply-chain
product: freight-forwarding
tags: [freight-forwarding, freight-forwarder, logistics-supply-chain, incoterms, incoterms-2020, fob, exw, dap, ddp, fca, ocean-freight, air-freight, fcl, lcl, bill-of-lading, house-bill, master-bill, air-waybill, hawb, mawb, commercial-invoice, packing-list, certificate-of-origin, chargeable-weight, volumetric-weight, cut-off, vgm, demurrage, detention, nvocc]
level: practitioner
status: draft
description: "Book an international shipment end to end: confirm Incoterm, pick air/FCL/LCL by chargeable weight and transit, book, hit cut-offs, issue documents, and handle exceptions."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# International shipment booking — from enquiry to delivered

**Goal:** get goods from shipper to consignee across borders by the right mode, with
documents that clear customs first time, and catch problems while they're still cheap.

## 1. Intake: the questions before quoting
- **Incoterm (2020 rules)** and named place — decides who pays and owns risk where.
  EXW/FCA: buyer's forwarder collects. FOB/CFR/CIF are for sea/inland waterway only;
  for containers prefer FCA/CPT/CIP. DAP: seller delivers to destination, buyer clears
  import. DDP: seller also pays import duty/VAT — make sure they can legally act as
  importer of record.
- Commodity description and HS code (for regulatory checks and duty estimate).
- Pieces, gross weight, dimensions per piece, stackable or not.
- Dangerous goods? Temperature control? Value (insurance)? Ready date and required delivery date.

## 2. Pick the mode
**Air chargeable weight** = max(actual kg, volume m³ × 167) (IATA 1:6000 cm³/kg).
Courier/express often uses 1:5000 (×200).
**Sea LCL** charged per revenue tonne = max(m³, tonnes).
Rough decision guide:
- < ~100 kg chargeable, urgent → express courier.
- Urgent or high value per kg → air.
- ~2–15 m³ → LCL; above ~13–15 m³ compare a 20' FCL (≈33 m³ nominal, ~25–28 usable).
- 40' ≈ 67 m³ nominal; 40'HC ≈ 76 m³. Check weight limits as well as cube — heavy
  cargo fills a 20' by weight long before cube; road limits at origin/destination may
  bind before the container's payload.
Price breaks change weekly; always compare door-to-door total, not freight alone.

## 3. Book and control the cut-offs
1. Book with carrier/airline (or co-load/consolidator for LCL); get booking number,
   vessel/voyage or flight, ETD/ETA.
2. Diarise every cut-off: **documentation (SI) cut-off**, **VGM cut-off** (SOLAS
   verified gross mass — no VGM, no loading), **CY/port cut-off** for gate-in,
   air cargo acceptance time.
3. Arrange pickup/drayage to arrive before the gate cut-off, with buffer.
4. Export customs filing before cut-off (EU: export declaration/ECS; US: EEI in AES
   when required).

## 4. Documents
- **Commercial invoice** (seller, buyer, Incoterm, HS codes, values, currency, origin).
- **Packing list** matching invoice piece count and weights.
- **Bill of lading** (sea): check shipper/consignee/notify, description, marks, piece
  count before issuing. Original vs telex release vs sea waybill — agree with the
  shipper how cargo will be released, especially under letter of credit.
- **Air waybill** (MAWB from airline, HAWB from forwarder).
- Certificates as needed: origin (for preferential duty), phyto, DG declaration.

## 5. Track and handle exceptions
- Watch rollovers (container not loaded), transhipment delays, blank sailings.
- On arrival: notify consignee, arrange import clearance and delivery before free
  time ends — **demurrage** (container in terminal) and **detention** (container out
  with you) can exceed the freight cost.
- Damage: note it on the delivery receipt, photograph, notify carrier in writing
  within the time limit (often 3 days sea, 14 days air — check the convention/contract).

## Gotchas
- Description "parts" or "samples" gets held; be specific.
- Invoice and packing list numbers that don't match the B/L delay clearance.
- LCL minimums (often 1 m³) and destination LCL fees can make small sea shipments
  dearer than air.
- Insurance is not automatic; carrier liability limits are low per kg.

## Verify
- [ ] Incoterm and named place written on the quote, invoice and booking.
- [ ] Chargeable weight/cube calculated and container fit checked by weight and volume.
- [ ] All cut-offs in the diary with owners; VGM submitted.
- [ ] Draft B/L or AWB checked against invoice and packing list before issue.
- [ ] Free time at destination known and delivery booked inside it.

*Uncertainty:* claim time limits and LCL minimums vary by carrier contract and route; confirm per booking.
