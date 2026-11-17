---
id: computing-software.web-development.web-accessibility.apg-disclosure-and-accordion
name: apg-disclosure-and-accordion
category: computing-software
field: web-development
product: web-accessibility
tags: [aria-patterns, accordion-pattern, disclosure-pattern, aria-expanded, wai-aria-apg]
level: practitioner
status: docs-checked
description: "Building disclosure and accordion widgets per the APG: button inside a heading, aria-expanded/aria-controls, hidden panels, optional arrow-key navigation, and details/summary."
sources:
  - https://www.w3.org/WAI/ARIA/apg/patterns/accordion/
  - https://www.w3.org/WAI/ARIA/apg/patterns/disclosure/
  - https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/details
  - https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Global_attributes/hidden
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/interpolate-size
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Disclosure and accordion

## 1. Disclosure (show/hide one section)
```html
<button type="button" aria-expanded="false" aria-controls="more-info">Show delivery details</button>
<div id="more-info" hidden>…</div>
```
Toggle `aria-expanded` and `hidden` together. Or native `<details><summary>` - no JS, keyboard and AT support built in.

## 2. Accordion (stack of disclosures with headings)
```html
<div class="accordion">
  <h3>
    <button type="button" aria-expanded="true" aria-controls="sect1" id="acc1">Shipping</button>
  </h3>
  <div id="sect1" role="region" aria-labelledby="acc1">…</div>
  <h3>
    <button type="button" aria-expanded="false" aria-controls="sect2" id="acc2">Returns</button>
  </h3>
  <div id="sect2" role="region" aria-labelledby="acc2" hidden>…</div>
</div>
```
- The **button goes inside the heading** (not the heading inside the button) so heading navigation still works and the button keeps its role.
- `role="region"` with `aria-labelledby` on panels is optional and helps with few panels; APG says to avoid it when more than approximately 6 panels can be expanded at once, to avoid landmark proliferation.
- Enter/Space toggles (native buttons do this).
- Optional keys: Down/Up Arrow between headers, Home/End. Not required - Tab works. Space/Enter on an expanded header collapses its panel when the design supports collapsing.
- Allowing multiple panels open is usually friendlier than forcing one; `<details name="group">` gives exclusive behaviour natively.

## 3. Pitfalls
- Using `div`/`a href="#"` as the trigger.
- Animating height while toggling `hidden` too early or late: toggle `hidden` after the collapse animation; MDN documents `interpolate-size: allow-keywords` and the `::details-content` pseudo-element for animating `<details>`.
- Hiding content with only `max-height: 0` - still focusable and read; add `hidden`/`visibility: hidden` when collapsed.
- Find-in-page can't search hidden panels; `hidden="until-found"` keeps the content searchable and reveals it when found; the `beforematch` event fires on the element so you can expand the matching section.
- Using an accordion to hide essential content on desktop where space allows.

## Verify
Screen reader announces "Shipping, button, expanded/collapsed" inside a heading level; heading navigation lists all sections; collapsed content is not reachable by Tab.

## Checked

2026-10-26, against WCAG 2.2 / APG as of 2026-10-26 (w3c repos). Confirmed against the APG accordion and disclosure patterns (Enter/Space toggle, optional arrow/Home/End keys, button inside heading, region role guidance of about 6 panels) and MDN (details name grouping gives exclusive open, hidden=until-found with beforematch, interpolate-size allow-keywords, ::details-content). Removed the unconfirmed grid-template-rows animation recipe and the Chromium-only wording.

Method: documentation only; no commands were run.
