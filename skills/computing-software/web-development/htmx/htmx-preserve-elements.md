---
id: computing-software.web-development.htmx.htmx-preserve-elements
name: htmx-preserve-elements
category: computing-software
field: web-development
product: htmx
tags: [htmx, hx-preserve, swap, video, state, history]
level: practitioner
status: docs-checked
description: "Keep elements such as video players unchanged across htmx swaps with hx-preserve: id requirement, limits, relocation, OOB usage and history behaviour."
sources:
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/attributes/hx-preserve.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/docs.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/attributes/hx-boost.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: stop an element (e.g. a playing video) being replaced when an ancestor is swapped.

Rules:
- Add `hx-preserve` (boolean attribute, or `hx-preserve="true"`) to the element.
- The element MUST have a stable `id`. The response must contain an element with the same `id`; its type and other attributes are ignored.
- `hx-preserve` is not inherited.

```html
<div id="player-wrap">
  <video id="player" hx-preserve src="/movie.mp4"></video>
</div>
```

Known limits: some elements cannot be preserved properly, such as `<input type="text">` (focus and caret position are lost), iframes and certain videos. For those the docs recommend the morphdom swap extension, which does fuller DOM reconciliation.

Behaviour notes:
- A preserved element can be moved: if the response places the same-id element inside a different container, the existing node is relocated there.
```html
<div id="new_location">Moved here <div id="video" hx-preserve></div></div>
```
- It works inside the content of an `hx-swap-oob` element:
```html
<div id="notify" hx-swap-oob="true">Updated <div id="retain" hx-preserve></div></div>
```
- On history restoration (back button), preserved elements also keep their state.
- Avoid `hx-swap="none"` for requests whose response may contain a preserved element, to avoid losing it.
- Boosting: `hx-preserve="true"` disables replacement of that element and its children by boosted navigation.

## Checked

2026-11-07. Confirmed against the hx-preserve reference (id requirement, boolean or `"true"` form, not inherited, limits, morphdom recommendation, relocation, OOB use, history, `hx-swap="none"` warning), the hx-boost reference (`hx-preserve="true"` disables boost replacement) and the docs page (video player example). Removed the invented Verify step.
Method: documentation only; no commands were run.
