---
id: creative-arts.comics-and-sequential-art.comic-colouring.automated-flatting-tools
name: automated-flatting-tools
category: creative-arts
field: comics-and-sequential-art
product: comic-colouring
tags: [comic-colouring, flatting, flats, auto-flatting, colorize-flatting, clip-studio-paint, csp-colouring, csp-refer-other-layers, csp-close-gap, fill-close-gap, bucket-fill-reference]
level: practitioner
status: draft
description: "Speed up flatting with automated tools: CSP fill with Refer other layers and Close gap, Colorize hint layers, Photoshop actions/plug-ins, and the manual clean-up they still need."
sources:
  - https://help.clip-studio.com/en-us/First_Topic.htm
  - https://openlibrary.org/search?q=DC+Comics+Guide+to+Coloring+and+Lettering+Comics
  - https://www.clipstudio.net/en/functions/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Automated flatting tools

**Goal:** get 80-90% of flats done automatically, then fix the rest by hand.

## Options
| Tool | How it works | Notes |
|---|---|---|
| CSP Fill tool, "Refer other layers" | bucket fills on a flats layer using the line layer as reference | set Close gap, Area scaling (expand ~1-3 px) so fills go under lines; anti-aliasing off |
| CSP "Enclose and fill" / "Paint unfilled area" | lasso around an area to fill all enclosed regions, or catch leftover gaps | fast for hair and small shapes |
| CSP Colorize (AI, Ver. 1.10+ in some editions) | paints rough colour from hint strokes | output needs heavy clean-up; better for rough colour than exact flats |
| Photoshop flatting actions/plug-ins (third party, e.g. MultiFill-style tools) | fill every enclosed region with a random colour | then merge regions manually |
| Gap-closing line layer | draw temporary closing lines on a separate layer used as reference | delete after |

## Workflow (CSP example)
1. Line art on its own layer; set it as **Reference layer** (layer properties).
2. Flats layer below; Fill tool sub tool "Refer other layers": Multiple referring =
   reference layer, Close gap level medium, Area scaling +1-2 px, anti-aliasing off.
3. Click regions with distinct colours.
4. Use "Paint unfilled area" or a fill sub tool for leftover gaps and tiny holes.
5. Zoom check for leaks (fill escaping through a broken line) and white specks.

## Manual clean-up still needed
- Gaps in line art (open contours): close with a temporary line or paint by hand.
- Thin areas (fingers, hair strands) where close gap fills over the line.
- Separate regions with no line between them (e.g. a colour change on clothing).

## Verify
- [ ] No leaks across regions; no white specks.
- [ ] Fills extend under lines; aliased.
