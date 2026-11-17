---
id: creative-arts.graphic-design.adobe-indesign.alternate-layouts
name: alternate-layouts
category: creative-arts
field: graphic-design
product: adobe-indesign
tags: [graphic-design, adobe-indesign, indesign, indesign-document-setup, alternate-layouts, multiple-page-sizes, linked-stories, link-styles, content-placer, page-tool, multi-format-publishing]
level: advanced
status: draft
description: "Hold several page sizes or orientations in one InDesign file with Alternate Layouts: linked stories, copied style groups, liquid rules and per-layout export."
sources:
  - https://helpx.adobe.com/indesign/using/alternate-layouts-liquid-layouts.html
  - https://helpx.adobe.com/indesign/using/linked-content.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Alternate layouts and multiple page sizes

**Goal:** one InDesign document holding every size of a piece (ad sizes, A4 and Letter editions,
portrait and landscape) with text linked so copy edits propagate.

## Create an alternate layout
Pages panel menu > **Create Alternate Layout** (or Layout > Create Alternate Layout):
- Name, page size/orientation.
- **Liquid Page Rule:** Preserve Existing, or a rule (see adjust/liquid layout skill).
- **Link Stories:** text in the new layout is linked to the original story; edit the parent story and
  linked ones show an update icon - update in the Links panel. Prefer this for copy that must match.
- **Copy Text Styles to New Style Group:** the layout gets its own style group so you can change type
  sizes for the smaller format without affecting the original.
- **Smart Text Reflow** option.
The Pages panel shows layouts side by side in columns.

## Multiple page sizes in one document
Without alternate layouts, the **Page tool (Shift+P)** sets individual page sizes - useful for a
stationery set (card, letterhead, compliment slip) or cover + spine + flaps in one file.

## Linking content manually
- **Content Collector/Placer** (see that skill) places linked copies of objects or text anywhere,
  with Link options (update styles or keep local formatting via Link Options).
- Links panel shows linked stories; modified ones get a warning - update deliberately.

## Output
- Export each layout separately: PDF export page range by layout, or **File > Export** and choose the pages.
- Print or export alternate layouts as separate files for media owners with naming per size.

## Gotchas
- Linked stories overwrite local edits in the child when updated, unless you set Link Options to preserve
  local edits (paragraph/character style changes can be preserved; text edits cannot).
- Very different aspect ratios still require layout redesign; alternate layouts handle content consistency, not composition.
- Large multi-layout files become slow; split by campaign wave if needed.

## Verify
- [ ] Every required size exists as a layout; copy updates propagate via linked stories.
- [ ] Each layout preflights clean and exports to correctly named files.
