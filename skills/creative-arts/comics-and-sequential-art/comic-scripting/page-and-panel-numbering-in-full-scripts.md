---
id: creative-arts.comics-and-sequential-art.comic-scripting.page-and-panel-numbering-in-full-scripts
name: page-and-panel-numbering-in-full-scripts
category: creative-arts
field: comics-and-sequential-art
product: comic-scripting
tags: [comic-scripting, full-script, comic-script-format, panel-numbering, script-page-breakdown, page-headers, left-right-page, script-formatting]
level: practitioner
status: draft
description: "Lay out a full comic script so every page and panel is unambiguous: page headers with left/right side, panel counts, numbered balloons, and renumbering after edits."
sources:
  - https://openlibrary.org/search?q=DC+Comics+Guide+to+Writing+Comics
  - https://en.wikipedia.org/wiki/Comic_book
  - https://scottmccloud.com/2-print/3-mc/index.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Page and panel numbering in full scripts

**Goal:** a script the penciller, letterer and editor can all navigate by number, with
no question about which drawing a line of dialogue belongs to.

There is no single industry-mandated format (publishers and writers differ), but every
working format shares the same skeleton.

## The skeleton
```
PAGE ONE (right-hand page)          <- side matters for page turns
Five panels.

PANEL 1
Wide establishing shot. A rain-slick harbour at night...

  1  CAPTION:      Port Calder. Three hours before the fire.

PANEL 2
Closer on MARA (30s, dock-worker jacket) ducking under a crane.

  2  MARA:         Late again.
  3  MARA (small): Always late.

PAGE TWO (left-hand page)
...
```

## Rules that stop production errors
1. **Page header on every page**, spelled out or numbered (`PAGE ONE` / `PAGE 1`), plus
   the panel count directly under it ("Five panels."). The artist budgets the page
   before reading details.
2. **Mark the side.** In a standard comic, page 1 is a right-hand page (odd = right,
   even = left) unless the book opens on a spread or has an inside-front-cover story.
   Note it so reveals are planned for page turns (odd to even).
3. **Panels restart at 1 on each page.** Never number panels continuously through the
   book; editors refer to "page 7 panel 3".
4. **Balloon numbers run continuously across the whole page** (some writers across the
   whole issue). The letterer's placement guide uses those numbers.
5. **One new page = one new page break** in the document (hard page break in Word/Docs)
   so the PDF page roughly mirrors the comic page when printed.
6. **Speaker names in caps**, then a colon, aligned in a column; modifiers in
   parentheses: `(OFF)`, `(WHISPER)`, `(BURST)`, `(RADIO)`, `(CONT'D)`.

## Renumbering after edits
- Cutting or inserting a panel: update the panel count line and every panel number on
  that page, then balloon numbers. Do it in one pass with search, not by eye.
- Cutting a page: renumber every later page and re-check left/right sides; a reveal
  that was on a page turn may now sit on a facing page.
- Keep a dated version in the file name (`issue03_script_v4_2026-10-16`) so the artist
  never draws from a stale draft.

## Gotchas
- "Page 12-13 (spread)" must be written as both numbers; letterers and printers
  count physical pages.
- Ad pages in floppies: the writer counts story pages only; the editor maps them to
  printed pages later. Ask whether page 1 is still a right-hand page after ads.
- Panel counts above about 7 on a standard page get cramped; flag it to yourself.

## Verify
- [ ] Every page has a header, side, and panel count that matches the panels below.
- [ ] Panel numbers restart per page; balloon numbers have no gaps or duplicates.
- [ ] After any edit, page sides re-checked against planned page-turn reveals.
