---
id: creative-arts.graphic-design.adobe-indesign.parent-pages-based-on-parents
name: parent-pages-based-on-parents
category: creative-arts
field: graphic-design
product: adobe-indesign
tags: [graphic-design, adobe-indesign, indesign, parent-pages, master-pages, nested-parent-pages, based-on-parent, parent-hierarchy, apply-parent, load-parent-pages]
level: practitioner
status: draft
description: "Structure InDesign parent pages as a hierarchy: a base parent for shared folios and grids, section variants based on it, applying and loading parents."
sources:
  - https://helpx.adobe.com/indesign/using/masters.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Parent pages based on parents

**Goal:** a small family of parent pages where shared elements live in one place and variants differ only where needed.

## Build a hierarchy
1. `A-Base`: margins, columns, baseline grid, folios, running heads - everything common.
2. New Parent (Pages panel menu > New Parent) `B-Feature`: **Based on Parent: A-Base**. It inherits A's
   items and adds e.g. a section colour bar and 3 columns.
3. `C-News`: based on A, 5 columns, different header.
4. `D-Opener`: based on A but with folios removed (override and delete inherited items, or use [None] base).
Changing a folio style on A updates B, C and D. Pages panel shows the inheritance letter on the parent icon.

## Applying parents
- Drag a parent onto a page or spread in the Pages panel (onto the corner for a single page, the spread edge for a spread).
- Pages panel menu > **Apply Parent to Pages**: type a range (`5-12, 20`).
- Alt/Option+click a parent to apply it to selected pages.
- `[None]` for pages that should have no parent elements (covers, ads).

## Sharing across documents
- **Load Parent Pages** (Pages panel menu > Parent Pages > Load Parent Pages) from another INDD;
  choose Replace or Rename on name conflicts.
- Or drag a parent spread into another open document's Pages panel.
- For series (monthly magazine), keep parents in a template (.indt) and start each issue from it.

## Columns and margins per parent
Each parent has its own Layout > Margins and Columns; document pages inherit them when the parent is
applied (unless the page was changed locally - see overrides skill).

## Gotchas
- Applying a different parent to a page with overridden items keeps the overrides (orphaned) - check.
- Deep chains (E based on D based on C...) become confusing; two levels is usually enough.
- Parent page objects are behind document objects unless placed on a higher layer.

## Verify
- [ ] Shared elements exist only on the base parent; variants inherit.
- [ ] Every document page uses the intended parent (Pages panel letters).
