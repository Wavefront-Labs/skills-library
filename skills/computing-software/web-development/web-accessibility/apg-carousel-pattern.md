---
id: computing-software.web-development.web-accessibility.apg-carousel-pattern
name: apg-carousel-pattern
category: computing-software
field: web-development
product: web-accessibility
tags: [aria-patterns, carousel-pattern, slideshow, wcag-2-2-2, wai-aria-apg]
level: practitioner
status: docs-checked
description: "Building accessible carousels per the APG: pause/rotation control, previous/next and slide picker buttons, slide labelling, live region rules, and stopping auto-rotation on focus."
sources:
  - https://www.w3.org/WAI/ARIA/apg/patterns/carousel/
  - https://www.w3.org/WAI/tutorials/carousels/
  - https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Carousel pattern

First question: do you need a carousel? A static grid or a single hero avoids the rotation, focus and live-region problems below.

## 1. Structure
```html
<section class="carousel" aria-roledescription="carousel" aria-label="Featured products">
  <button type="button" class="rotation" aria-label="Stop slide rotation">⏸</button>
  <button type="button" aria-controls="slides" aria-label="Previous slide">‹</button>
  <button type="button" aria-controls="slides" aria-label="Next slide">›</button>
  <div id="slides" aria-live="off">
    <div role="group" aria-roledescription="slide" aria-label="1 of 4">…</div>
    <div role="group" aria-roledescription="slide" aria-label="2 of 4" hidden>…</div>
  </div>
</section>
```
Slide picker ("dots") variant: a tablist where each tab selects a slide (`role="tab"`, slides `role="tabpanel"`), or a group of buttons with `aria-disabled`/`aria-current` on the active one.

## 2. Rules
- **Auto-rotation**: needs a visible pause/stop control (WCAG 2.2.2) as the first element in the carousel's focus order; stop rotation when keyboard focus enters the carousel or the mouse hovers over it, and do not restart unless the user explicitly asks. The rotation button's label changes to the action it will perform ("Stop slide rotation" / "Start slide rotation").
- **Live region**: `aria-live="off"` while auto-rotating (no constant announcements); `"polite"` when rotation is stopped so manual next/previous changes are announced.
- Hidden slides are removed from tab order and AT (`hidden` or `inert`), so links in off-screen slides aren't focusable.
- Prev/next buttons and pickers are real buttons with names; WCAG 2.5.8 (Target Size Minimum, AA) asks for 24 by 24 CSS px targets unless an exception applies.
- Swipe (path-based) gestures need single-pointer alternatives such as the buttons (2.5.1, Level A).
- Slide text over images meets contrast; enough time to read (2.2.1).

## 3. Libraries
Verify any carousel library against the checks below; do not assume its defaults meet them.

## Verify
Keyboard: first Tab reaches pause; focusing anything stops rotation; off-screen slide links unreachable. Screen reader: the carousel is announced with its label and role description, and the slide label (for example "2 of 4") is announced on manual navigation.

## Checked

2026-10-26, against WCAG 2.2 / APG as of 2026-10-26 (w3c repos). Confirmed against the APG carousel pattern: rotation control first in the Tab sequence inside the carousel, rotation stops on keyboard focus and on mouse hover and does not restart unless the user asks, aria-roledescription carousel/slide, slide role group (tabpanel in the tabbed variant), live region off while rotating and polite otherwise, and the changing rotation-button label. WCAG 2.2.2 and 2.5.1 are Level A and 2.5.8 is Level AA. Removed the click-through claim, library recommendations and the reduced-motion claim.

Method: documentation only; no commands were run.
