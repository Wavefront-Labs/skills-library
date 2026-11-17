---
id: computing-software.web-development.htmx.htmx-swap-modifiers
name: htmx-swap-modifiers
category: computing-software
field: web-development
product: htmx
tags: [htmx, hx-swap, scroll, show, transition, settle, ignoretitle, focus-scroll]
level: practitioner
status: docs-checked
description: "Tune hx-swap with modifiers swap, settle, transition, ignoreTitle, scroll, show and focus-scroll, including selector and window scroll targets."
sources:
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/attributes/hx-swap.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/docs.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/api.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/events.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: adjust timing, scrolling, titles and transitions of a swap.

Modifiers come after the swap style, colon-separated, space between modifiers: `hx-swap="innerHTML swap:1s show:top"`.

- `transition:true|false` - use the View Transitions API. Globally: `htmx.config.globalViewTransitions = true`. Calling `preventDefault()` on `htmx:beforeTransition` skips the View Transition and the normal swapping logic happens instead.
- `swap:<time>` - delay between receiving the response and swapping (`swap:1s`).
- `settle:<time>` - delay between swap and settle (`settle:1s`). Use both to sync with CSS transitions.
- `ignoreTitle:true` - do not update the document title from a `<title>` in the response (config `ignoreTitle` is global).
- `scroll:top|bottom` - change the scrolling of the target element (the example scrolls a fixed-height div to its bottom).
- `show:top|bottom` - ensure the top or bottom of the target is visible in the viewport.
- Another element: `show:#another-div:top`, `scroll:#panel:bottom`; the window: `show:window:top`.
- `show:none` disables the default scroll for boosted links/forms (boosted default is `show:top`; global switch `htmx.config.scrollIntoViewOnBoost`).
- `focus-scroll:true|false` - htmx preserves focus for inputs with an `id`, but by default does not scroll to them; `focus-scroll:true` enables it (global `htmx.config.defaultFocusScroll`).

```html
<div style="height:200px;overflow:scroll" hx-get="/example" hx-swap="beforeend scroll:bottom">Load more</div>
<button hx-post="/like" hx-swap="outerHTML ignoreTitle:true">Like</button>
```

Scroll animation is governed by `htmx.config.scrollBehavior` (`instant` default, `smooth`, `auto`).

Same options exist programmatically in `htmx.swap()`'s `swapSpec` (`swapDelay`, `settleDelay`, `transition`, `ignoreTitle`, `scroll`, `show`, `focusScroll`).

## Checked

2026-11-07. Confirmed against the hx-swap reference (all modifiers, selector and `window` scroll targets, boosted `show:top` default, focus-scroll), the API page (`scrollBehavior` values and default, `defaultFocusScroll`, `globalViewTransitions`, `scrollIntoViewOnBoost`, `htmx.swap` `swapSpec` fields) and the events page (`htmx:beforeTransition`). Removed an unsourced "falls back if unsupported" claim, tightened the scroll and show wording, and removed the invented Verify step.
Method: documentation only; no commands were run.
