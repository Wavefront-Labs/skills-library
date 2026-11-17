---
id: creative-arts.comics-and-sequential-art.comic-colouring.cut-and-grind-gradient-rendering
name: cut-and-grind-gradient-rendering
category: creative-arts
field: comics-and-sequential-art
product: comic-colouring
tags: [comic-colouring, colour-rendering, comic-rendering, cut-and-grind, gradient-rendering, lasso-gradient, feathered-selection, modern-comics-colour]
level: practitioner
status: draft
description: "Render with the cut-and-grind method: lasso a hard-edged shape, then grade it with a soft brush or gradient inside the selection, for the hybrid look common in modern mainstream comics."
sources:
  - https://openlibrary.org/search?q=DC+Comics+Guide+to+Coloring+and+Lettering+Comics
  - https://helpx.adobe.com/photoshop/using/making-quick-selections.html
  - https://en.wikipedia.org/wiki/Colorist
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cut-and-grind gradient rendering

**Goal:** hard-edged shadow shapes with soft gradients inside: crisp design plus
volume.

## The method
1. **Cut**: with the lasso (or polygon lasso), draw the shadow shape with a hard edge,
   staying inside the flat (intersect with a flat selection, or use a clipping mask).
2. **Grind**: inside the selection, paint with a large soft airbrush or apply a
   gradient so the shadow grades from dark (core) to lighter (reflected light).
3. Repeat for highlights: lasso the highlight shape, grade with a lighter colour.
4. Optional: a few soft, unselected passes for ambient glow.

## Tips
- Gradient direction follows the form and light: darkest near the terminator, lighter
  toward the edge where bounce light hits.
- Use a Multiply layer for shadow and Screen/Add for light so you can tweak colour
  globally.
- Save frequent shapes as selections if a panel repeats.

## Style control
- Pure cut (no grind) = cel style; pure grind (no cut) = soft airbrush.
- The balance defines the colourist's look; keep it consistent across the book.

## Gotchas
- Gradients without hard edges everywhere: rubbery "airbrushed 90s" look (unless
  intended).
- Lasso edges anti-aliased while flats are aliased: fine for render layers, but don't
  apply it to the flats layer.

## Verify
- [ ] Shapes hard-edged where designed, gradients follow light.
- [ ] Look consistent page to page.
