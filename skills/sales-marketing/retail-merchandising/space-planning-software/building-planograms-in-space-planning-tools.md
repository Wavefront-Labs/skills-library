---
id: sales-marketing.retail-merchandising.space-planning-software.building-planograms-in-space-planning-tools
name: building-planograms-in-space-planning-tools
category: sales-marketing
field: retail-merchandising
product: space-planning-software
tags: [space-planning-software, space-planning, planogram-software, blue-yonder, jda-space-planning, jda, relex, relex-space, nexgen, nexgen-pog, smartdraw, planogram, pog, fixture-library, product-library, store-clusters, planogram-versions, compliance-export, retail-merchandising, category-management, product-dimensions, product-images]
level: practitioner
status: draft
description: "Build and maintain planograms in space-planning software (Blue Yonder/JDA, Relex, Nexgen): clean product and fixture libraries, build POGs, version by store cluster, export for stores."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Building planograms in space-planning tools

**Goal:** turn the planogram logic (see sales-marketing.retail-merchandising.planogramming.planogram-design-and-compliance)
into accurate, buildable files for every store cluster, without re-drawing the same shelf
twenty times.

The tools differ in menus but share one workflow. **Note:** the specific menu names below
are generic; Blue Yonder (formerly JDA) Space Planning, Relex Space and Nexgen POG each name
things differently and version-to-version changes are common — follow your vendor's
training material for exact clicks.

## 1. Product library — garbage in, garbage out
Every product record needs:
- **ID** (GTIN/UPC/EAN and internal SKU), description, brand, category, subcategory.
- **Dimensions** W×H×D for the unit and for the case/tray if displayed in shelf-ready
  packaging. Units must be consistent (all cm or all inches).
- **Orientation**: which face is the front; whether it can be laid down or stacked.
- **Images** (front face at least) so the rendered planogram is recognisable in store.
- **Performance data**: units and sales/margin per week, imported from your sales system.

Before any build, run the tool's data-quality or "missing dimensions" report and fix
products with zero or default dimensions (often 1×1×1). Measure new lines with a ruler;
supplier data is frequently wrong.

## 2. Fixture library
Create each fixture once: gondola bay widths and heights, shelf depths and thickness,
notch pitch, peg-board hole spacing, dividers, freezer and chiller cabinets. Name them
consistently (`GOND-100W-180H-5SH`). Store layouts reference fixtures, so a wrong
fixture propagates everywhere.

## 3. Build the master planogram
1. Create a new planogram on the right fixture (e.g. 4 bays × 5 shelves).
2. Place products shelf by shelf following the category decision tree; use the tool's
   **auto-fill or auto-facing** to allocate facings by sales or days of supply, then
   adjust by hand.
3. Check the **performance panel/report**: days of supply per item, % space vs % sales,
   capacity vs case pack. Fix items under minimum DOS.
4. Set shelf heights so the tallest item on each shelf plus a finger gap (~2–3 cm) fits.
5. Run the **validation/collision check** for overlaps, overhangs and items exceeding shelf depth.

## 4. Store-cluster versions
- Cluster stores by fixture length (e.g. 4, 6, 8 bays) and demographic/sales profile.
- Build the largest version first, then derive smaller ones by removing the lowest-ranked
  items and reducing facings — most tools support copying a planogram and re-flowing.
- Keep a naming convention: `CAT_SUBCAT_CLUSTER_WIDTH_YYYYMMDD` (e.g.
  `COFFEE_GROUND_C2_4B_20261101`). Dates in names make old versions easy to purge.
- Maintain a store-to-planogram assignment table (often in the tool's floor-planning
  module or a spreadsheet the tool imports).

## 5. Export for stores and compliance
- Export a **PDF** per planogram: rendered image, shelf-by-shelf product list with
  position numbers and facings, shelf heights. Many teams also export a CSV for
  shelf-edge label printing in planogram order.
- Publish via your store communication portal with the reset date.
- Feed compliance audit photos back to the space team; recurring "doesn't fit" flags
  usually mean bad dimensions in the library.

## Gotchas
- **Units mismatch** (inches vs cm) between import and library silently scales items.
- **Auto-fill** respects only the rules you set; it will happily put a heavy item on the top shelf.
- Large libraries slow the tool; archive discontinued products and old planograms.
- Licensing is per seat and expensive; small retailers may use lighter tools (e.g.
  general diagramming software with planogram templates) at the cost of no
  performance data — a reasonable start under ~20 stores (judgement, not a vendor claim).

## Verify
- [ ] No products in the planogram with default/zero dimensions or missing images.
- [ ] Validation report shows no overlaps, overhangs or depth violations.
- [ ] Every item meets minimum days of supply and case-pack capacity.
- [ ] Each store is assigned exactly one current version per category.
- [ ] Exported PDF/CSV matches the build (spot-check 3 shelves).
- [ ] A store built a test bay from the PDF without questions.
