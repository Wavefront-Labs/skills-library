---
id: creative-arts.comics-and-sequential-art.comic-colouring.fixing-aliased-fills-and-gaps-under-line-art
name: fixing-aliased-fills-and-gaps-under-line-art
category: creative-arts
field: comics-and-sequential-art
product: comic-colouring
tags: [comic-colouring, flatting, flats, aliased-fill, fill-gaps, white-specks, flat-cleanup, trapping-under-lines]
level: practitioner
status: draft
description: "Find and fix flatting defects: white specks between flats and lines, leaks, anti-aliased fringes, and flats that fall short of the line, with a fast QC pass method."
sources:
  - https://openlibrary.org/search?q=DC+Comics+Guide+to+Coloring+and+Lettering+Comics
  - https://help.clip-studio.com/en-us/First_Topic.htm
  - https://en.wikipedia.org/wiki/Trap_(printing)
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Fixing aliased fills and gaps under line art

**Goal:** flats that fully meet or run under every line, with no specks or fringes
that show in print.

## Common defects
| Defect | Cause | Fix |
|---|---|---|
| White specks between fill and line | bucket stopped at anti-aliased line edge | expand fill under lines (area scaling +1-2 px) or paint with aliased pencil |
| Leaks (colour floods neighbour) | gap in line art | undo; close gap temporarily; refill |
| Fringes/halos | anti-aliased fill or selection | refill with anti-alias off |
| Fill short of line in tight corners | bucket can't enter thin areas | pencil in by hand |
| Wrong region merged | two regions same flat colour touching | separate with distinct colour |

## QC pass (fast)
1. **Hide LINES** and look at FLATS alone: white specks and gaps jump out.
2. Or add a temporary solid bright layer **under** FLATS (e.g. magenta): any hole in
   FLATS shows magenta.
3. Magic wand the white (tolerance 0, contiguous off) on FLATS to find stray white
   pixels.
4. Fix at 200-300% zoom; tackle panel by panel.

## Why it matters in print
Lines are black on top, but slight misregistration on press can reveal tiny white
gaps between colour and line; colour running under lines (like trapping) hides it.

## Verify
- [ ] Magenta-underlay test shows no holes.
- [ ] No anti-aliased pixels in FLATS.
- [ ] No leaks across regions.
