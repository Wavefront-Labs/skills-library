---
id: computing-software.general-digital-literacy.office-suites.morph-transition-and-zoom
name: morph-transition-and-zoom
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, slideshow, presenting, morph-transition, summary-zoom, slide-zoom]
level: practitioner
status: docs-checked
description: "Animate objects smoothly between slides with PowerPoint Morph (Keynote Magic Move) and build interactive navigation with Summary Zoom and Slide Zoom."
sources:
  - https://support.microsoft.com/en-us/powerpoint/training/use-the-morph-transition-in-powerpoint
  - https://support.microsoft.com/en-us/office/morph-transition-tips-and-tricks-bc7f48ff-f152-4ee8-9081-d3121788024f
  - https://support.microsoft.com/en-us/powerpoint/use-zoom-for-powerpoint-to-bring-your-presentation-to-life
  - https://support.apple.com/guide/keynote/add-transitions-tanff5ae749e/mac
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Morph and Zoom

## Morph (PowerPoint for Microsoft 365, 2019 and later; also the web and mobile apps)
1. Build slide 1. **Duplicate** it.
2. On slide 2 move, resize, recolour or rotate objects (same objects, changed).
3. Select slide 2 › **Transitions › Morph**. For text, set Effect Options to *Words* or
   *Characters* (words and letters rearranging).
4. Objects match by being the same object; force a match between two objects of the same type by giving
   both the same name starting with `!!` in the Selection Pane (Windows: Home › Editing › Select ›
   Selection Pane; Mac: Home › Arrange › Selection Pane).
- Morph can also zoom, scroll and crop across a large picture for a "camera" effect.
- Charts don't morph.
- Keynote: **Magic Move** transition, same duplicate-and-change approach; Match *By Object*, *By Word*
  or *By Character*, and *Fade Unmatched Objects*.

## Zoom
**Insert › Zoom**:
- **Summary Zoom**: one slide with thumbnails of chosen sections; click any to jump there.
- **Section Zoom** / **Slide Zoom**: link to a section or to chosen slides.
- Zoom tab: **Return to Zoom** brings you back after the target (on by default for summary and section
  zooms, off for slide zooms); *Zoom Background*, *Change Image*, *Zoom Transition* and duration.
- Summary zooms update through Zoom tab › **Edit Summary** › Update.
Use for non-linear talks (pick topics based on audience questions).

## Gotchas
- PowerPoint 2016 can only play Morph, and only with the required updates; without them it plays a Fade.
- Too many morphs feel gimmicky; keep it to moments that show change (before/after, process).

## Verify
- [ ] Play from slide 1 in Slide Show: objects glide, no unmatched object pops in.

## Checked
2026-10-27, against Microsoft Support (Use the Morph transition; Morph transition tips and tricks; Use Zoom for PowerPoint; PowerPoint for Microsoft 365 and 2019-2024) and the Keynote for Mac User Guide (Add transitions). Confirmed: Morph version table and the PowerPoint 2016 Fade fallback, Transitions › Morph and the Words/Characters effect options, the `!!` naming rule (same object type) and the Selection Pane path per OS, the camera-style image effect, no chart morphing, Magic Move match options, Zoom types, Return to Zoom defaults, Zoom tab options and Edit Summary. Corrected the Selection Pane path and removed an unconfirmed duration tip.
Method: documentation only; no commands were run.
