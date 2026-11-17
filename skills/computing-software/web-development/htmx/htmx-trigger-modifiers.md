---
id: computing-software.web-development.htmx.htmx-trigger-modifiers
name: htmx-trigger-modifiers
category: computing-software
field: web-development
product: htmx
tags: [htmx, hx-trigger, debounce, throttle, delay, queue, from, consume]
level: practitioner
status: docs-checked
description: "hx-trigger modifiers once, changed, delay, throttle, from, target, consume and queue, with extended selectors and the whitespace-selector gotcha."
sources:
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/attributes/hx-trigger.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/docs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: debounce, throttle, limit or redirect events that fire htmx requests.

Modifiers follow the event name (and any `[filter]`), space-separated:
- `once` - fire only for the first event.
- `changed` - only if the element's value changed (note: `change` is the event, `changed` is the modifier).
- `delay:<time>` - wait (e.g. `1s`, `500ms`); if the event is seen again it resets the delay.
- `throttle:<time>` - a throttle occurs after an event triggers a request; if the event is seen again before the delay completes it is ignored, and the element will trigger at the end of the delay.
- `from:<extended selector>` - listen on another element. A plain selector matches all elements, evaluated once (not re-evaluated when the page changes). Extras: `document`, `window`, `closest <sel>`, `find <sel>`, `next`, `next <sel>`, `previous`, `previous <sel>`.
- `target:<selector>` - filter via a CSS selector on the target of the event; useful for elements that might not be in the DOM at initialization, e.g. listen on the body with a target filter for a child element.
- `consume` - the event will not trigger any other htmx requests on parents (or on elements listening on parents).
- `queue:<first|last|all|none>` - how events are queued if an event occurs while a request for another event is in flight: `first`, `last` (default), `all` (a request for each event) or `none` (do not queue new events).

Example (active search):
```html
<input name="q" hx-get="/search" hx-trigger="input changed delay:1s" hx-target="#search-results"/>
```

Dynamic elements (catch click events from every button on the page):
```html
<div hx-get="/x" hx-trigger="click[event.target.matches('button')] from:body"></div>
```

Gotcha: a selector containing whitespace in `from:` or `target:` must be wrapped, e.g. `from:(form input)` or `from:closest (form input)`.

## Checked

2026-11-07. Confirmed against the hx-trigger reference (every modifier, the extended `from:` selector values, evaluated-once note, the active-search example, the `click[event.target.matches('button')] from:body` example, the whitespace-selector note). The `keyup[key=='s'] from:body` hotkey example is not on the page and was removed; the page only describes hot keys listened for on the body. Reworded delay, throttle, target, consume and queue to the page's wording and removed the "(debounce)" label and the invented Verify step.
Method: documentation only; no commands were run.
