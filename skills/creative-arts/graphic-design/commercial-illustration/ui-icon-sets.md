---
id: creative-arts.graphic-design.commercial-illustration.ui-icon-sets
name: ui-icon-sets
category: creative-arts
field: graphic-design
product: commercial-illustration
tags: [graphic-design, commercial-illustration, ui-icon-set, icon-set, svg-icons, icon-design, icon-library, optical-alignment, icon-export]
level: practitioner
status: draft
description: "Design a consistent UI icon set: grid and stroke rules, optical alignment, naming, states, SVG export and clean-up, and accessibility notes for implementation."
sources:
  - https://helpx.adobe.com/illustrator/user-guide.html
  - https://help.figma.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Product and UI icon sets

**Goal:** a set that stays visually uniform as it grows and ships as clean, usable SVG.

## 1. Rules (build on `creative-arts.graphic-design.information-design.icon-grid-and-keylines`)
- **Base grid:** for example 24x24 with a 2 px padding (live area 20x20), and a consistent stroke (commonly 1.5 or 2 px at 24 px). Pick one and keep it.
- **Style:** outline or filled or two-tone; corner radius; stroke caps and joins; whether strokes are expanded.
- **Metaphors:** a vocabulary list with decisions (what is "settings", "share", "delete"), reusing established patterns for recognition.
- **Optical alignment:** circles slightly larger than squares, thin elements aligned by weight, not mathematically centred.

## 2. Production
- Figma: use frames at the base size, **components** for each icon and **variants** for states or sizes; keep strokes outlined or live consistently. Illustrator: artboard per icon, shared grid, **Object > Path > Outline Stroke** when strokes must be expanded.
- Name consistently (kebab-case: `arrow-left`, `user-add`), sorted by semantic group, not by appearance.
- Provide sizes only where optical changes are needed (a 16 px version may be redrawn with fewer details).

## 3. Export
- SVG: viewBox equal to the base size, no hard-coded width and height if the platform scales it, `fill="currentColor"` or `stroke="currentColor"` so the icon inherits text colour, no extra metadata.
- Clean with an SVG optimiser such as SVGO (check it does not remove the viewBox or merge shapes unexpectedly).
- Offer an icon font or sprite only if the implementation requires it; inline SVG is flexible and accessible.

## 4. Accessibility
- Decorative icons: hide from assistive tech; icons that convey meaning or act as buttons need an accessible name (text label, `aria-label`, or visually hidden text).
- Do not rely on icon shape alone for critical actions; add text where possible.

## 5. Review
Display the full set at small and large sizes, at 100 percent and at 200 percent zoom, in light and dark themes; check consistent weight and visual density.

## Failure modes
- Mixed stroke weights from scaling.
- Icons that are exported with white fills that fail on dark backgrounds.
- Different optical sizes of similar glyphs.
