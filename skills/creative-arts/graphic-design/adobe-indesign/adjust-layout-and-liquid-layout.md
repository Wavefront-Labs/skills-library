---
id: creative-arts.graphic-design.adobe-indesign.adjust-layout-and-liquid-layout
name: adjust-layout-and-liquid-layout
category: creative-arts
field: graphic-design
product: adobe-indesign
tags: [graphic-design, adobe-indesign, indesign, indesign-document-setup, adjust-layout, liquid-layout, page-tool, resize-document, scale-rule, object-based-rule, guide-based-rule, format-change]
level: advanced
status: draft
description: "Resize InDesign layouts to new formats with Adjust Layout and Liquid Layout rules (scale, re-center, guide-based, object-based) instead of rebuilding by hand."
sources:
  - https://helpx.adobe.com/indesign/using/adjust-layout.html
  - https://helpx.adobe.com/indesign/using/alternate-layouts-liquid-layouts.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Adjust Layout and Liquid Layout

**Goal:** convert a layout from A4 to Letter, or a flyer to a different ad size, with most objects
moving and resizing correctly automatically.

## Adjust Layout (File > Adjust Layout, or Document Setup > Adjust Layout)
- Change page size, margins and bleed in one dialog; InDesign repositions and scales objects
  proportionally relative to the new margins.
- Options: **Auto-Adjust Margins to Page Size Changes**, **Adjust Font Size** (with min/max limits),
  **Adjust Locked Content**.
- Good for near-similar proportions (A4 <-> Letter). For very different proportions (portrait to landscape),
  expect manual cleanup.

## Liquid Layout rules (Page tool Shift+P, or Layout > Liquid Layout)
Set a rule per page (usually on the parent) that governs what happens when the page is resized with the
Page tool or in Alternate Layouts:
| Rule | Behaviour | Use |
|---|---|---|
| Scale | everything scales like an image | same proportions only |
| Re-center | content stays the same size, centred | fixed-size elements |
| **Guide-based** | liquid guides (dashed) - objects crossed by them stretch in that direction | headers/bands that should widen |
| **Object-based** | per object: pin edges (lock to page edges), fixed or flexible width/height | most control: logos pinned to corner, images flexible |
| Controlled by Master | inherit from the parent | |

Object-based: select an object with the Page tool; click the circles on its edges to pin, and the
spring icons inside to allow resizing in height/width.

## Frame fitting matters
Image frames need **Auto-Fit** with Fill Frame Proportionally (see frame fitting skill), otherwise images
crop oddly when frames resize. Text frames: auto-size or flexible columns.

## Workflow for ad resizes
1. Build the master layout with object-based rules and auto-fitting frames.
2. Create a new size via Alternate Layout or Page tool; review.
3. Fix the remaining 10-20% by hand. Still faster than rebuilding.

## Gotchas
- Rules are per page; forgetting to set them on parents means each page needs setup.
- Text does not reflow intelligently - headline sizes may need manual changes.
- Grouped objects behave as one; ungroup or use object-based rules on the group.

## Verify
- [ ] Resized page: logos pinned correctly, images not distorted, nothing outside the trim.
- [ ] Font sizes within the limits; manual fixes noted.
