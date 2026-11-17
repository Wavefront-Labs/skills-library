---
id: computing-software.web-development.htmx.htmx-sync-requests
name: htmx-sync-requests
category: computing-software
field: web-development
product: htmx
tags: [htmx, hx-sync, race-condition, abort, queue, request-cancel]
level: practitioner
status: docs-checked
description: "Coordinate overlapping htmx requests with hx-sync strategies drop, abort, replace and queue, plus htmx:abort for manual cancellation."
sources:
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/attributes/hx-sync.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/docs.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/events.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: prevent races between requests from different elements (or the same one).

Syntax: `hx-sync="<selector>[:<strategy>]"`. The selector names the element whose requests to coordinate with (`this`, `closest form`, `#id`). Strategies:
- `drop` (default) - ignore this request if one is already in flight.
- `abort` - ignore this request if one is in flight; and if not, abort this one if another request occurs while it is in flight.
- `replace` - abort the current request, if any, and use this one.
- `queue` - place this request in the request queue associated with the element. Add `first`, `last` or `all`: `queue first` queues the first request to show up while one is in flight, `queue last` the last, `queue all` all of them.

`hx-sync` is inherited.

Examples:
```html
<!-- input validation is aborted if the form submits -->
<form hx-post="/store">
  <input id="title" name="title" hx-post="/validate" hx-trigger="change" hx-sync="closest form:abort">
  <button type="submit">Submit</button>
</form>

<!-- submit wins: cancel in-flight validations -->
<form hx-post="/store" hx-sync="this:replace">
  <input name="title" hx-post="/validate" hx-trigger="change"/>
</form>

<!-- active search keeps only the latest request -->
<input type="search" hx-get="/search" hx-trigger="keyup changed delay:500ms, search"
       hx-target="#search-results" hx-sync="this:replace">
```
Use `closest form:drop` on an input to prioritise validation: the form cannot submit while it is in flight. Use `this:abort` on the form to prioritise existing validation over submit.

Manual cancel: send `htmx:abort` to the element making the request, e.g. `htmx.trigger('#request-button', 'htmx:abort')`. `htmx:sendAbort` is triggered when a request is aborted.

## Checked

2026-11-07. Confirmed against the hx-sync reference (syntax, four strategies and their wording, queue variants, inheritance, all four examples and the closing advice), the events page (`htmx:abort` example, `htmx:sendAbort`), the docs (programmatic cancel) and the reference event table. Reworded the queue line to the page's wording and dropped an inferred claim that htmx "listens rather than emits" the abort event. Removed the invented Verify step.
Method: documentation only; no commands were run.
