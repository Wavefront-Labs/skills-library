---
id: computing-software.web-development.htmx.htmx-swap-styles
name: htmx-swap-styles
category: computing-software
field: web-development
product: htmx
tags: [htmx, hx-swap, innerhtml, outerhtml, beforeend, swap-strategy]
level: intro
status: docs-checked
description: "Choose how htmx inserts a response with hx-swap: innerHTML, outerHTML, textContent, beforebegin, afterbegin, beforeend, afterend, delete, none."
sources:
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/attributes/hx-swap.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/docs.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/events.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/attributes/hx-preserve.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: decide where in the DOM the returned HTML goes relative to the target.

Values for `hx-swap` (default is `htmx.config.defaultSwapStyle`, which is `innerHTML`):
- `innerHTML` - replace the target's inner HTML.
- `outerHTML` - replace the whole target with the response.
- `textContent` - replace target text without parsing the response as HTML.
- `beforebegin` - insert before the target.
- `afterbegin` - insert before the target's first child.
- `beforeend` - insert after the target's last child (append).
- `afterend` - insert after the target.
- `delete` - delete the target regardless of the response.
- `none` - do not insert response content; out-of-band swaps and response headers are still processed.

These mirror `Element.insertAdjacentHTML` naming.

```html
<div hx-get="/example" hx-swap="afterend">Get Some HTML & Append It</div>
<ul id="feed"></ul>
<button hx-get="/more" hx-target="#feed" hx-swap="beforeend">More</button>
```

Notes:
- `hx-swap` is inherited, so it can sit on a parent.
- `outerHTML` on `<body>` is not possible due to DOM limits; htmx uses `innerHTML` instead.
- Default swap delay is 0 ms, default settle delay 20 ms (see `htmx-swap-modifiers`).
- A server can override with the `HX-Reswap` response header (same values), and `htmx:beforeSwap` can set `detail.swapOverride`.
- Morphing swaps come from extensions (e.g. idiomorph, which supplies the `morph` swap strategy). They merge new content into the existing DOM, often preserving focus and video state better, at the cost of more CPU.
- Avoid `none` for requests that could contain an `hx-preserve` element, to avoid losing it.

## Checked

2026-11-07. Confirmed against the hx-swap reference (all nine values, default, `insertAdjacentHTML` note, `afterend` example, inheritance, `<body>` outerHTML note, delay defaults), the docs (Morph Swaps section, `morph` via idiomorph, `HX-Reswap`), the events page (`detail.swapOverride`) and the hx-preserve page (the `none` caution; page added to `sources`). Trimmed the "(as a sibling)" gloss and rephrased the morph note to the docs' wording. Removed the invented Verify step.
Method: documentation only; no commands were run.
