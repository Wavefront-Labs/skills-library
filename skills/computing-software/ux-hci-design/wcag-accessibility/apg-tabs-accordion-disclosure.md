---
id: computing-software.ux-hci-design.wcag-accessibility.apg-tabs-accordion-disclosure
name: apg-tabs-accordion-disclosure
category: computing-software
field: ux-hci-design
product: wcag-accessibility
tags: [apg-tabs, apg-accordion]
level: practitioner
status: docs-checked
description: "Build tabs with arrow-key navigation and accordions with aria-expanded header buttons, following the APG patterns."
sources:
  - https://www.w3.org/WAI/ARIA/apg/patterns/tabs/
  - https://www.w3.org/WAI/ARIA/apg/patterns/accordion/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tabs
Roles: `tablist` contains `tab` elements; each content area is a `tabpanel`. The tablist has `aria-labelledby` (visible label) or `aria-label`. Each tab has `aria-controls` pointing to its panel; the active tab has `aria-selected="true"` and the others `false`. Each panel has `aria-labelledby` pointing to its tab. Add `aria-orientation="vertical"` for a vertical tablist (default is horizontal) and `aria-haspopup` on a tab that has a popup menu.

Keys: Tab moves focus into the tablist on the active tab, and the next Tab goes to the tabpanel (unless its first meaningful content is focusable). Left/Right arrows move to the previous/next tab and wrap at the ends (Down/Up do this in a vertical list). Space or Enter activates a tab if it was not activated on focus. Home and End (optional) go to the first and last tab. Delete (optional) closes a tab and focuses the following tab, or the previous one if it was last. If a tabpanel has no focusable content, give it `tabindex="0"`.

Activation: the page recommends automatic activation on focus only if panels display without noticeable latency (content preloaded); otherwise use manual activation with Space or Enter.

# Accordion
Each header is a `button` that is the only child of a heading element (native `h*` is fine, with an appropriate level). The button has `aria-expanded` true/false and `aria-controls` pointing to the panel. Enter or Space toggles it (collapsing the other panel if only one may be open). If an open panel may not be collapsed, set `aria-disabled="true"` on its button. Tab and Shift+Tab move through all focusable elements; arrow navigation between headers is not part of the page's keyboard interaction. Optionally give panels `role="region"` with `aria-labelledby` pointing to the header button, but avoid it for accordions with more than about 6 panels open at once.

## Verify
- [ ] Arrow keys move among tabs; only the active tab's panel is shown.
- [ ] Accordion header buttons toggle with Enter and Space, and `aria-expanded` matches the visible state.

## Checked
2026-11-09. Read the whole APG Tabs and Accordion pattern pages (w3.org/WAI/ARIA/apg/patterns/tabs/ and /accordion/). Removed the unsupported claims about roving tabindex in tabs, the native details/summary tip, the screen reader announcement text and the optional accordion arrow keys. The disclosure pattern is not covered by either source and is not described here.

Method: documentation only; no commands were run.
