---
id: creative-arts.graphic-design.adobe-indesign.content-collector-and-placer
name: content-collector-and-placer
category: creative-arts
field: graphic-design
product: adobe-indesign
tags: [graphic-design, adobe-indesign, indesign, content-collector, content-placer, conveyor, linked-content, link-options, repurposing-layouts, indesign-graphics]
level: practitioner
status: draft
description: "Reuse InDesign page items with the Content Collector, Conveyor and Content Placer: collect objects, place them as linked copies, map styles, and update when the parent changes."
sources:
  - https://helpx.adobe.com/indesign/using/linked-content.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Content Collector and Content Placer

**Goal:** move text and graphics between documents or layouts (print to tablet, A4 to letter, catalogue
to flyer) as **linked** copies that update when the original changes.

## Tools
- **Content Collector tool (B)** opens the **Conveyor**, a holding area. Click objects to collect them;
  drag a marquee to collect several. Panel menu: **Collect All Threaded Frames**, or Load Conveyor
  (selection, pages, or all page items).
- **Content Placer tool (B toggles)** places items from the Conveyor. Options on the Conveyor:
  - **Create Link**: the placed item is a child of the original; Links panel tracks it.
  - **Map Styles**: map paragraph, character, table, cell styles from source to target names
    (Edit > Custom Style Mapping).
  - Place mode: place and remove from Conveyor, place multiple times, or place and load next.

## Linked content behaviour
- When the parent changes, the child shows the modified link icon in the Links panel; update to sync.
- Link options (Links panel menu > Link Options): choose which attributes are preserved on update
  (local edits like size, interactivity, style overrides) so layout tweaks on the child survive.
- Edit > **Place and Link** does the same for selected items without the Conveyor.

## Uses
- Alternate layouts for different page sizes (Layout > Create Alternate Layout uses this linking).
- Recurring legal text or price boxes shared across a set of documents.
- Moving items between documents without copying and pasting styles by accident.

## Gotchas
- Updating the child overwrites local text edits unless Link Options preserve them; tell editors to edit
  the parent only.
- Linked text frames show as linked stories; breaking threads changes what is linked.
- Styles with the same names but different definitions are overwritten on update when mapping is not set.

## Verify
- [ ] Links panel lists children with parent paths; changes to the parent appear after updating.
- [ ] Style mapping produced the target document's styles, with no imported duplicates.
