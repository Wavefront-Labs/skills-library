---
id: creative-arts.graphic-design.adobe-illustrator.stroke-panel-caps-joins-and-dashes
name: stroke-panel-caps-joins-and-dashes
category: creative-arts
field: graphic-design
product: adobe-illustrator
tags: [graphic-design, adobe-illustrator, illustrator, pen-tool, stroke-panel, dashed-lines, caps-and-joins, miter-limit, align-stroke, arrowheads, dotted-line, scale-strokes]
level: practitioner
status: draft
description: "Control strokes in Illustrator's Stroke panel: caps, joins, miter limit, align stroke inside/outside, even dashes that fit corners, round-dot lines, arrowheads and scaling strokes."
sources:
  - https://helpx.adobe.com/illustrator/using/strokes.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Stroke panel: caps, joins, dashes and arrowheads

**Goal:** strokes that look intentional at corners and ends, with dashes and arrows that behave.

## Caps and joins (Window > Stroke, Ctrl/Cmd+F10; Show Options)
- **Caps:** Butt (ends at the anchor), **Round** (semicircle beyond the anchor), Projecting (square beyond).
- **Joins:** **Miter** (sharp), Round, Bevel. Sharp angles with miter joins can spike; the
  **Limit** (default 10x) switches to bevel beyond that ratio.
- Icons and UI usually use round caps + round joins, or butt + miter for crisp geometric styles - pick one per system.

## Align stroke (closed paths)
Center (default), **Inside**, or **Outside**. Inside keeps the shape's outer size exact (UI, cards);
outside keeps the fill area exact (outlines around text-shaped art). Not available for open paths or text.

## Dashes
- Tick **Dashed Line**; enter dash/gap pairs (e.g. 6 pt dash, 4 pt gap).
- **Align dashes to corners and path ends** (right-hand icon): adjusts lengths so corners get full
  dashes - looks deliberate on rectangles. The other option keeps exact lengths.
- **Dotted line:** Round cap + dash **0** + gap e.g. 6 pt with stroke weight 3 pt = round dots.
- Cut-lines/perforation marks on dielines often use dashed strokes on a separate layer (see dieline skill).

## Arrowheads
Start and end arrowheads from the menu, **Scale** % for each, swap button, and **Align**: tip at end of
path or arrow placed beyond the path end. Arrowheads scale with stroke weight - check after changing weight.

## Profiles and weight
- Variable width profiles: see the width tool skill.
- Weight under 0.25 pt (0.1 mm) may not print reliably (hairlines); printers commonly ask >= 0.25 pt.
- **Scale Strokes & Effects** (Preferences > General, or Transform panel options): on to keep proportions
  when scaling illustrations; off when strokes must keep exact weights (icons, technical drawings).

## Gotchas
- Strokes on text sit centred and eat into letters; use Appearance with stroke below fill (see appearance skill).
- Dashed lines and arrowheads become separate shapes when outlined (Outline Stroke) - check results before sending to cutters.

## Verify
- [ ] Corners show full dashes; caps/joins consistent across the artwork.
- [ ] No hairlines below the printer's minimum.
- [ ] Stroke scaling setting appropriate for the job.
