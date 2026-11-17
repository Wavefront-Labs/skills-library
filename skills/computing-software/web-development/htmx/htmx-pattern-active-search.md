---
id: computing-software.web-development.htmx.htmx-pattern-active-search
name: htmx-pattern-active-search
category: computing-software
field: web-development
product: htmx
tags: [htmx, active-search, search-as-you-type, hx-trigger, debounce, hx-indicator]
level: practitioner
status: docs-checked
description: "Search-as-you-type with htmx: hx-trigger 'input changed delay:500ms, keyup[key==Enter], load' posts the query, fills a table body, and shows an indicator."
sources:
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/examples/active-search.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/docs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: query the server as the user types, without flooding it, and render results in place.

```html
<h3>Search Contacts
  <span class="htmx-indicator"><img src="/img/bars.svg" alt=""/> Searching...</span>
</h3>
<input class="form-control" type="search" name="search"
       placeholder="Begin Typing To Search Users..."
       hx-post="/search"
       hx-trigger="input changed delay:500ms, keyup[key=='Enter'], load"
       hx-target="#search-results"
       hx-indicator=".htmx-indicator">
<table class="table">
  <tbody id="search-results"></tbody>
</table>
```

The trigger is a comma-separated list of three triggers:
- `input changed delay:500ms` fires on the `input` event, but only if the value actually changed (`changed`, so arrow keys or pasting the same text do nothing), and only after 500 ms of quiet; each new event resets the countdown (`delay`).
- `keyup[key=='Enter']` is an event filter: a JavaScript expression in square brackets resolved against the KeyboardEvent first, then the global scope. Enter searches immediately.
- `load` runs one search at page load so the table starts populated.

The input has `name="search"`, and the example's fake server reads the `search` parameter. It returns only `<tr>` rows, which the example places inside `#search-results` as the body of the table.

The `htmx-indicator` class makes an element invisible (opacity 0, still in the DOM). During a request htmx puts `htmx-request` on the requesting element or on the element named by `hx-indicator`; here `hx-indicator=".htmx-indicator"` points at the indicator span, which the docs' CSS `.htmx-request.htmx-indicator` covers.

Variations
- `throttle:<interval>` instead of `delay`: unlike `delay`, an event that arrives before the time limit is discarded, so the request triggers at the end of the period (docs.md).
- docs.md shows the same idea with GET: `hx-get="/trigger_delay" hx-trigger="keyup changed delay:500ms"` and `name="q"`.

## Checked

2026-11-07. Confirmed on examples/active-search.md (markup, trigger list, `delay`, `changed`, `keyup[key=='Enter']`, `load`, indicator) and docs.md (trigger modifiers including the `delay` reset and `throttle`, trigger filters resolved against the event then global scope, request indicators, the `/trigger_delay` GET example).
Fixed: reworded the form-value sentence to what the example shows and the indicator sentence to the docs wording; throttle now matches docs.md. Removed the invented Verify step.
Method: documentation only; no commands were run.
