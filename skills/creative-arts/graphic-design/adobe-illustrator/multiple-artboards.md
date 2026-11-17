---
id: creative-arts.graphic-design.adobe-illustrator.multiple-artboards
name: multiple-artboards
category: creative-arts
field: graphic-design
product: adobe-illustrator
tags: [graphic-design, adobe-illustrator, illustrator, illustrator-artboards, illustrator-document-setup, multiple-artboards, artboard-tool, artboards-panel, rearrange-artboards, export-artboards, stationery-set]
level: practitioner
status: draft
description: "Use multiple artboards in Illustrator for sets (stationery, icon sets, campaign sizes): create, name, order, rearrange, copy art across them and export or print per artboard."
sources:
  - https://helpx.adobe.com/illustrator/using/using-multiple-artboards.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Multiple artboards

**Goal:** one Illustrator file holding a whole set of related pieces, each exportable on its own.

## Create and size
- New document: set **Number of Artboards**, arrangement (grid by row/column), spacing.
- **Artboard tool (Shift+O):** drag to draw, Alt/Option+drag to duplicate an artboard with
  its artwork (tick "Move/Copy Artwork with Artboard" in the Options bar). Type exact
  W/H and X/Y in the Control or Properties panel; pick presets (A4, Letter, 1080x1080).
- **Object > Artboards > Fit to Artwork Bounds** for icon or logo artboards that hug art.

## Name and order (Window > Artboards)
- Double-click a name to rename: `01-business-card-front`, `02-business-card-back`.
  Names become export file names.
- The panel order is the **page order** for PDF export and printing; drag to reorder.
- **Rearrange All Artboards** (panel menu) lays them out in a clean grid by panel order,
  with set spacing - use after a messy session.

## Working across artboards
- **Edit > Paste on All Artboards** (Alt+Shift+Ctrl+V / Opt+Shift+Cmd+V): puts the same
  element (logo, crop marks, guides) in the same relative spot on every artboard.
- **Paste in Place** (Shift+Ctrl/Cmd+V) pastes at the same position on the active artboard.
- Rulers can be global or per artboard (View > Rulers > Change to Artboard Rulers).

## Output
- **File > Export > Export for Screens** - tick artboards, choose formats/scales.
- **Save As PDF** - choose All or a Range (e.g. `1-3, 5`).
- **Print** - artboard range, or "Ignore Artboards" to tile.
- **Save As AI with "Save each artboard to a separate file"** for handing off singles.

## Gotchas
- Max 1000 artboards; canvas is 227 x 227 inches (Large Canvas: 2270 inches at 1/10 scale).
- Art that crosses an artboard edge exports cropped (unless bleed is set for print).
- Artboard order and physical position are independent; exports follow panel order.

## Verify
- [ ] Every artboard named meaningfully and ordered as the deliverable order.
- [ ] Export for Screens / PDF produces one correctly named file or page per artboard.
