---
id: creative-arts.graphic-design.brand-identity.packaging-graphics
name: packaging-graphics
category: creative-arts
field: graphic-design
product: brand-identity
tags: [graphic-design, brand-identity, brand-touchpoints, packaging-design, packaging-graphics, dieline, shelf-impact, front-of-pack, mandatory-information, barcode, flexography, range-architecture]
level: practitioner
status: draft
description: "Design packaging graphics: front-of-pack hierarchy, range and variant systems, mandatory information and barcodes, working to dielines, and print process limits like flexo."
sources:
  - https://www.gs1.org/standards/barcodes/ean-upc
  - https://www.food.gov.uk/business-guidance/packaging-and-labelling
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Packaging graphics

**Goal:** a pack that wins the 3-second shelf moment, tells the shopper what it is and which variant, and
passes regulation and print.

## Front-of-pack hierarchy (decide the order)
1. **Brand block** (logo, often in a consistent position across the range).
2. **Product descriptor** (what it is).
3. **Variant** (flavour, scent, strength), signalled by colour coding plus words.
4. **Key claim or benefit** (one, not five).
5. Required front-of-pack information (net quantity, warnings, nutrition labels where required).

## Range architecture
- Fixed elements (brand block, layout grid, typography) and variable elements (variant colour, imagery).
- Test the range together on a mock shelf: variants must be distinct, brand block must block together.

## Mandatory information
- Varies by country and category (food, cosmetics, pharma): ingredients and allergens emphasised, net quantity
  with minimum height, nutrition, best-before, producer address, recycling marks, batch codes area. Get the
  legal text from the client's regulatory team; do not write it.
- Minimum font sizes are often legal requirements (e.g. EU food information Regulation 1169/2011: x-height
  at least 1.2 mm, 0.9 mm for small packs).
- **Barcode** (EAN-13/UPC-A): GS1 numbers from the client; nominal size and quiet zones; dark bars on a
  light background; not over folds or curves.

## Working to the dieline
- Use the converter's dieline on its own layer (spot colour named `Dieline`, overprint, non-printing in
  final output). Respect folds, glue flaps, bleed (often 3 mm), safe zones and panel orientation.
- Mock up physically (print, cut, fold) before final; check how panels read on the shelf.

## Print process limits
- **Flexography** (cartons, films, labels): minimum dot, line and reverse text sizes are larger than offset;
  fewer fine gradients; trapping. Get the printer's design guide.
- Many packs print with spot colours plus white ink on films or metallic substrates; build separate
  white and varnish layers.

## Gotchas
- Variants coded only by colour fail for colour-blind shoppers; add words.
- Mandatory text placed last never fits; reserve the area from the start.

## Verify
- [ ] Physical mockup checked; barcode verified with a scanner.
- [ ] Regulatory text approved by the client's compliance team; printer's guide limits met.
