---
id: creative-arts.comics-and-sequential-art.webcomics.converting-page-comics-to-vertical-scroll
name: converting-page-comics-to-vertical-scroll
category: creative-arts
field: comics-and-sequential-art
product: webcomics
tags: [webcomics, vertical-scroll, webtoon-format, page-to-scroll-conversion, reformatting, panel-resequencing, balloon-relettering]
level: practitioner
status: draft
description: "Reformat page-layout comics for vertical scroll: re-sequencing panels into one column, recomposing wide panels, re-lettering for phone size, and what can't convert cleanly."
sources:
  - https://webtoons-static.pstatic.net/creator101/en/pdf/Creators-Resource-Handbook-Updated.pdf
  - https://en.wikipedia.org/wiki/Webtoon
  - https://help.clip-studio.com/en-us/First_Topic.htm
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Converting page comics to vertical scroll

**Goal:** a readable vertical version of a page-format comic without redrawing
everything.

## Process
1. **Get layered files** (art, letters separate). Flattened pages make this far harder.
2. **Sequence panels** into a single column in reading order.
3. **Resize** each panel to full column width (or deliberately narrower for small
   beats). Wide horizontal panels shrink a lot; tall panels grow.
4. **Recompose where needed**: extend backgrounds, crop, or split a wide panel into two
   stacked panels. Side-by-side simultaneous panels may need stacking with a visual cue.
5. **Re-letter**: page-size text becomes tiny after column scaling; reflow balloons
   at phone-legible sizes and place them between panels where helpful.
6. **Spacing**: add gutters as pacing (bigger at scene changes).
7. **Splashes and spreads**: become tall crops or panned sequences of crops; some
   simply don't convert well.

## Things that don't survive
- Page-turn reveals (replace with scroll gaps).
- Page-design tricks (art spanning panels, panel shapes that form an image).
- Dense 9-panel grids: often become very long scrolls; consider trimming.

## Verify
- [ ] Reading order correct in one column.
- [ ] Text legible on a phone at 800 px width.
- [ ] Reveals rebuilt as scroll gaps.
