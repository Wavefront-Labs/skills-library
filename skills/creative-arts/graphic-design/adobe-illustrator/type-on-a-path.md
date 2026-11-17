---
id: creative-arts.graphic-design.adobe-illustrator.type-on-a-path
name: type-on-a-path
category: creative-arts
field: graphic-design
product: adobe-illustrator
tags: [graphic-design, adobe-illustrator, illustrator, illustrator-type, type-on-a-path, circular-text, badge-lettering, type-on-path-options, baseline-shift, flip-text, seal-logo]
level: practitioner
status: draft
description: "Set type on a path in Illustrator, including circular badge text with top and bottom arcs reading the right way up, path type options, bracket handles, spacing fixes and alignment."
sources:
  - https://helpx.adobe.com/illustrator/using/creating-type-path.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Type on a path and circular text

**Goal:** text that follows a curve cleanly - the classic badge/seal with readable top and bottom arcs.

## Basics
- **Type on a Path tool** (under the Type tool), or simply click on an open or closed path with the
  Type tool while hovering (cursor changes). The path loses its fill and stroke.
- Three **brackets**: start bracket, centre bracket and end bracket. Drag the centre bracket to slide
  text along the path; drag it **across** the path to flip text to the other side.
- Type > Type on a Path > **Type on a Path Options**: Effect (Rainbow default, Skew, 3D Ribbon, Stair Step,
  Gravity), **Align to Path** (Baseline, Ascender, Descender, Center), Spacing (tightens text on curves), Flip.

## Circular badge (top and bottom text both upright)
1. Draw a circle (Shift+drag) with the Ellipse tool.
2. Duplicate it in place (Ctrl/Cmd+C, Ctrl/Cmd+F) - one circle for the top text, one for the bottom.
3. **Top:** click on the first circle with Type on a Path, type, set paragraph alignment **Center**,
   drag the centre bracket to 12 o'clock.
4. **Bottom:** on the second circle, type, Center, drag the centre bracket **across** the path to flip it
   inside, position at 6 o'clock. Now it reads left-to-right upright but sits inside the circle.
5. Fix the bottom text's position with Options > **Align to Path: Ascender** (or baseline shift a negative value)
   so both texts sit on the same visual ring. Alternatively use a slightly smaller circle for the bottom text.
6. Add separators (stars, dots) at 3 and 9 o'clock.

## Spacing on curves
- Text on convex curves spreads at the top; on concave curves letters crowd. Adjust **tracking** and
  the Spacing option; kern individual pairs (Alt/Option+arrows).
- Use a typeface with even widths; very condensed or script faces distort.

## Gotchas
- Text overflows silently (red + on the end bracket) when the path is too short.
- Bottom text placed "under" the circle without flipping reads upside down.
- For logos, convert to outlines on a copy after final approval (see create outlines skill).

## Verify
- [ ] Top and bottom arcs both read upright, centred at 12 and 6 o'clock.
- [ ] No overflow; letter spacing visually even around the curve.
