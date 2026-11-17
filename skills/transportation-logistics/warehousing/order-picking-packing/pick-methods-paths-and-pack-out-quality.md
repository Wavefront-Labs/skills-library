---
id: transportation-logistics.warehousing.order-picking-packing.pick-methods-paths-and-pack-out-quality
name: pick-methods-paths-and-pack-out-quality
category: transportation-logistics
field: warehousing
product: order-picking-packing
tags: [order-picking, picking, packing, pick-and-pack, discrete-picking, batch-picking, zone-picking, cluster-picking, wave-picking, pick-to-light, voice-picking, rf-picking, pick-path, s-shape, serpentine, pick-accuracy, mispick, carton-selection, cartonization, dim-weight, void-fill, pack-station, ship-label, e-commerce-fulfilment]
level: practitioner
status: draft
description: "Choosing pick methods (discrete, batch, zone, cluster), designing pick paths, accuracy habits that prevent mispicks, and pack-out: carton selection, dim weight and quality checks."
sources: ["Tompkins et al., Facilities Planning (order picking chapters)", "de Koster, Le-Duc & Roodbergen (2007), Design and control of warehouse order picking: a literature review", "Carrier dimensional-weight rules (UPS/FedEx published divisors)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Pick methods, paths and pack-out quality

**Goal:** pick the right item fast and pack it so it arrives undamaged at the lowest
shipping cost. Travel is typically about half of a picker's time — reduce it first.

## 1. Choose the pick method by order profile
| Method | How | Best when |
|---|---|---|
| Discrete (order) | One picker, one order at a time | Large multi-line orders, low volume |
| Batch | Pick total quantity for many orders, sort later | Many orders sharing SKUs (single-line e-commerce) |
| Cluster | One trip, a cart with totes for 6–20 orders, put to the right tote | Small multi-line e-commerce orders |
| Zone | Pickers stay in zones; tote passes zone to zone (pick-and-pass) or merges later | Large facilities, many SKUs |
| Wave | Release by time window/cut-off; combinable with the above | Carrier cut-offs drive the day |
Technology: RF scanning (flexible), **voice** (hands-free, good for cases/cold stores),
**pick-to-light** (very fast for high-velocity small items), goods-to-person automation.

## 2. Pick paths
- **S-shape (serpentine):** walk every aisle with a pick fully — simple, good with
  dense picks.
- **Return / largest-gap:** enter aisles from the end and return — better when picks
  per aisle are few.
- Let the WMS sort pick lists by **location sequence** that matches the physical
  walking route; check the sequence after any re-slotting.
- Heavy, crush-resistant items first; fragile last; cold-chain last before pack.

## 3. Accuracy habits
- **Scan location then item** (or check digit by voice). Never pick by description.
- Count aloud or by unit-of-measure: eaches vs. inner packs vs. cases.
- Look-alike SKUs (sizes, colours) slotted apart, not side by side.
- Short pick → report it in the device; don't substitute without a rule.
- Measure accuracy: errors per 1,000 lines (good sites < 1–3; best ~0.1–0.5). Feed
  errors back to the picker and to slotting.

## 4. Pack-out
1. **Verify at pack:** scan each item into the carton (scan-to-pack) — catches
   mispicks before they ship.
2. **Carton selection:** smallest carton that protects the item. Use the WMS
   cartonization suggestion, but check fragility.
3. **Dimensional weight:** carriers bill the greater of actual and dim weight =
   L×W×H ÷ divisor (e.g. 139 in³/lb for many US domestic services, 5,000 cm³/kg common
   internationally — *divisors vary by carrier and contract*). A 16×12×10 in box =
   1,920 in³ ÷ 139 ≈ 13.8 → 14 lb billed even if contents weigh 3 lb.
4. **Protection:** 5 cm (2 in) of cushioning around fragile items, nothing loose (shake
   test), heavy items at the bottom, liquids bagged and upright.
5. **Seal** with H-taping for heavy cartons; label on the largest flat face, not over
   seams; remove old labels/barcodes.
6. Inserts: packing slip, returns label if policy, documents for export (see trade
   documentation).

## 5. Station set-up
Everything within reach: cartons by size, tape, fill, printer, scale. Standing height
work surface; reduce bending and twisting.

## Gotchas
- Batch picking without accurate sortation creates swapped orders.
- Oversized cartons cost money twice: dim weight and void fill.
- Pick-to-light without confirmation buttons pressed in order hides mispicks.

## Verify
- [ ] Pick method matches the order profile (lines/order, SKU overlap).
- [ ] Pick lists sorted in walking sequence.
- [ ] Location and item scanned every pick; accuracy tracked per 1,000 lines.
- [ ] Scan-to-pack verification and smallest-protective carton used.
- [ ] Dim weight checked for the carton choice on high-volume SKUs.
