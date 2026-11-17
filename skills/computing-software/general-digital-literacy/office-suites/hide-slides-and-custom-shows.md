---
id: computing-software.general-digital-literacy.office-suites.hide-slides-and-custom-shows
name: hide-slides-and-custom-shows
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, slideshow, presenting, custom-slide-show, hide-slide, skip-slide]
level: practitioner
status: docs-checked
description: "Hide backup slides, build custom shows for different audiences from one PowerPoint deck, and skip slides in Google Slides, Keynote and Impress."
sources:
  - https://support.microsoft.com/en-us/powerpoint/hide-or-show-a-slide
  - https://support.microsoft.com/en-us/powerpoint/create-and-present-a-custom-show
  - https://support.microsoft.com/en-us/accessibility/powerpoint/use-keyboard-shortcuts-to-deliver-powerpoint-presentations
  - https://support.google.com/docs/answer/1694830
  - https://support.apple.com/guide/keynote/skip-or-unskip-a-slide-tan9cbb7c9fe/mac
  - https://github.com/LibreOffice/help/blob/master/source/text/simpress/guide/individual.xhp
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Hide slides and custom shows

## Hide a slide (still in the file, not shown in slideshow)
- PowerPoint: right-click the thumbnail › **Hide Slide** (slash through the slide number); **Unhide Slide** reverses it.
- Google Slides: right-click › **Skip Slide** (click again to show it). Keynote: select the slide › Slide ›
  **Skip Slide**, or Control-click › Skip Slide. Impress: View › Slide Sorter, select › Slide Show ›
  **Show/Hide Slide**.
- During a PowerPoint show you can still reach a hidden slide: right-click › *See All Slides* and pick it,
  or press **H** on the slide before it (Windows: not in Presenter View).

## Custom shows (PowerPoint)
1. **Slide Show › Custom Slide Show › Custom Shows › New**.
2. Tick slides under *Slides in presentation*, **Add**; reorder with the arrows; type a *Slide show name*, OK.
3. Run: Custom Slide Show › pick it, or **Set Up Slide Show › Show slides: Custom show**.
4. Link from a slide: select text or an object › Insert › **Action** › Mouse Click › *Hyperlink to* ›
   **Custom Show** › pick it and tick *Show and return* (drill down to detail, then come back).
- Impress: Slide Show › Custom Slide Shows › New.

## When to use what
- Backup slides for Q&A: hide them at the end.
- Same deck for 10- and 30-minute versions: custom shows, so edits to a slide update both.
- Very different audiences: separate files may be clearer.

## Gotchas
- Sharing the file shares hidden slides too; Google says people you share with can see skipped slides.

## Verify
- [ ] Run the show from the start: hidden slides are skipped and the custom show plays its order.

## Checked
2026-10-27, against Microsoft Support (PowerPoint for Microsoft 365 and 2016-2024: Hide or show a slide; Create and present a custom show; delivery keyboard shortcuts), Google Docs Editors Help (Add, delete and organize slides), the Keynote for Mac User Guide (skip a slide) and the LibreOffice help master branch (custom slide show guide). Confirmed: Hide/Unhide Slide, See All Slides and the H key, the Custom Shows dialog steps, Action › Hyperlink to › Custom Show with Show and return, Set Up Slide Show custom show option, Google Skip Slide and its sharing note, Keynote Skip Slide, and Impress Show/Hide Slide and Custom Slide Shows. Removed an unconfirmed "Print Hidden Slides" claim.
Method: documentation only; no commands were run.
