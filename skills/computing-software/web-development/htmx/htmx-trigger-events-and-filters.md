---
id: computing-software.web-development.htmx.htmx-trigger-events-and-filters
name: htmx-trigger-events-and-filters
category: computing-software
field: web-development
product: htmx
tags: [htmx, hx-trigger, events, filters, custom-events, htmx-trigger]
level: practitioner
status: docs-checked
description: "Choose what fires an htmx request with hx-trigger: event names, bracketed JS filters, multiple triggers, custom events and the htmx:trigger event."
sources:
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/attributes/hx-trigger.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/docs.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/events.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/api.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: control which event triggers a request.

Syntax of `hx-trigger`: an event name, optionally followed by a filter and modifiers; or a polling spec `every <time>`; or a comma-separated list of those. Each comma-separated trigger has its own options.

```html
<div hx-post="/mouse_entered" hx-trigger="mouseenter">...</div>
<div hx-get="/news" hx-trigger="load, click delay:1s"></div>
```

Defaults when `hx-trigger` is absent: `change` on `input`/`textarea`/`select`, `submit` on `form`, `click` on everything else.

Filters: a JavaScript boolean expression in square brackets right after the event name; the event fires only if it is true.
```html
<div hx-get="/clicked" hx-trigger="click[ctrlKey&&shiftKey]">Ctrl-Shift Click</div>
<div hx-get="/clicked" hx-trigger="click[checkGlobalState()]">...</div>
```
Symbols resolve first against the triggering event (`ctrlKey` is `event.ctrlKey`), then the global namespace. Standard event filters require eval, so `htmx.config.allowEval=false` disables them.

Other facts:
- `hx-trigger` is not inherited.
- With no request verb, `hx-trigger` only fires the `htmx:trigger` event (useful to run client scripts); real requests have `htmx:beforeRequest` / `htmx:afterRequest`.
- Custom events work: `hx-trigger="my-custom-event from:body"`.
- A request can also be started from JavaScript with `htmx.trigger(elt, name, detail)`.
- A `reset` trigger can fire before the browser resets form values; add a delay, e.g. `hx-trigger="change, reset delay:0.01s"`.

## Checked

2026-11-07. Confirmed against the hx-trigger reference (value forms, filter syntax and examples, symbol resolution, custom events with `from:body`, multiple triggers, `htmx.trigger()`, non-inheritance, `htmx:trigger`-only behaviour, `reset` workaround), the docs (natural-event defaults, `allowEval` and trigger filters), the events page (`htmx:trigger`, `htmx:beforeRequest`, `htmx:afterRequest`) and the API page (`htmx.trigger` parameters; page added to `sources`). Removed an unsourced claim that `this` is available in filters and the invented Verify step.
Method: documentation only; no commands were run.
