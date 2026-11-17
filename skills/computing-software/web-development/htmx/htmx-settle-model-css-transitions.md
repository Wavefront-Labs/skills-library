---
id: computing-software.web-development.htmx.htmx-settle-model-css-transitions
name: htmx-settle-model-css-transitions
category: computing-software
field: web-development
product: htmx
tags: [htmx, css-transitions, settle, htmx-swapping, htmx-settling, htmx-added, animation]
level: practitioner
status: docs-checked
description: "Animate htmx swaps with CSS only: keep ids stable, understand swap/settle order, and use htmx-swapping, htmx-added and htmx-settling classes."
sources:
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/docs.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/reference.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/examples/animations.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: get smooth CSS transitions on swapped content without JavaScript.

Key rule: keep the element's `id` stable across requests. Example: original `<div id="div1">Original Content</div>`, response `<div id="div1" class="red">New Content</div>` with CSS `.red{color:red;transition:all ease-in 1s}` animates from old to new state.

How it works: before the swap htmx finds existing elements with matching `id`, copies their old attribute values onto the new elements, swaps the content in with the old values, then after the settle delay (default 20 ms) applies the new values, so the browser sees a change and transitions it. Settled attributes default to `htmx.config.attributesToSettle = ["class","style","width","height"]`.

Order of operations for a request:
1. Element triggers; values gathered; `htmx-request` class applied.
2. Request sent; on response the target gets `htmx-swapping`.
3. Optional swap delay (`hx-swap="... swap:100ms"`).
4. Swap happens; `htmx-swapping` removed from target; `htmx-added` added to new content; `htmx-settling` added to target.
5. Settle delay (`settle:` modifier, default 20 ms); DOM settles; `htmx-settling` and `htmx-added` removed.

Class reference: `htmx-added` (new content, until settled), `htmx-indicator`, `htmx-request`, `htmx-settling`, `htmx-swapping`. Use `htmx-swapping` for fade-outs, e.g. `.fade-me-out.htmx-swapping{opacity:0;transition:opacity 1s ease-out}` together with `hx-swap="outerHTML swap:1s"`.

Class names are configurable: `swappingClass`, `settlingClass`, `addedClass`, `requestClass`.

## Checked

2026-11-07. Confirmed against the htmx docs (CSS Transitions summary and Details, Request Order of Operations, config table) and the reference class table, plus the Animation Examples page for the fade-out example (added to `sources`). Removed the invented Verify step; nothing else needed changing.
Method: documentation only; no commands were run.
