---
id: computing-software.web-development.htmx.htmx-quirks-and-gotchas
name: htmx-quirks-and-gotchas
category: computing-software
field: web-development
product: htmx
tags: [htmx, quirks, gotchas, inheritance, responsehandling, hx-boost, hx-include, config]
level: practitioner
status: docs-checked
description: "htmx surprises and their config fixes: attribute inheritance, innerHTML default, body swaps, 4xx/5xx not swapping, GET form values, history cache, hx-boost costs."
sources:
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/QUIRKS.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: recognise htmx's known quirks and apply the documented fix. Config can be set in a meta tag: `<meta name="htmx-config" content='{"key": value}'>`.

1. Attribute inheritance. Many attributes inherit, so `<div hx-target="#output">` gives both child buttons that target. Downsides: lost Locality of Behavior, and adding an attribute to a parent can inadvertently change children. Disable with `{"disableInheritance":true}`.

2. Default swap is `innerHTML`. Prefer `outerHTML` globally with `{"defaultSwapStyle":"outerHTML"}`.

3. Targeting `body` always does an `innerHTML` swap (historical), so you cannot change attributes of the `body` tag with an htmx request.

4. `4xx` and `5xx` responses do not swap, and `204 No Content` does not swap either. A framework returning `422 Unprocessable Entity` for invalid forms is the common surprise. Fix via `htmx:beforeSwap` or `htmx.config.responseHandling`. Default:

```json
{"responseHandling": [
  {"code":"204", "swap": false},
  {"code":"[23]..", "swap": true},
  {"code":"[45]..", "swap": false, "error":true},
  {"code":"...", "swap": false}]}
```
Swap everything: `[{"code":"...", "swap": true}]`. Allow 422 only: put `{"code":"422", "swap": true}` first in the default list. As a meta tag: `<meta name="htmx-config" content='{"responseHandling": [{"code":"...", "swap": true}]}'>`.

5. `GET` from a non-form element does not include the enclosing form's values (non-GET requests do). Add `hx-include`:

```html
<button hx-get="/search" hx-include="closest form">Search</button>
```

6. History is tricky, especially with third-party JS that modifies the DOM, and has security concerns. Most issues go away by disabling the cache so back navigation asks the server (slower): `{"historyCacheSize": 0}`.

7. `hx-boost` costs: history issues; only the body updates, so styles and scripts in the new `head` are discarded; the global JavaScript scope is not refreshed (a global `let` may fail as already defined). Some of the core team advise unboosted links and forms; the author still uses it on htmx.org.

8. Load htmx with a standard blocking `<script>`, not a module or `defer`. There is only a best-effort init for other timings; bundling or AJAX insertion of htmx itself are the cases that slip through. If DOM content loads before htmx, htmx features do nothing until it loads; prefetching htmx is one mitigation.

9. The JavaScript API is not a focus. If you lean heavily on it, especially `htmx.ajax()`, look for a more htmx-style approach.

## Checked

2026-11-07. Confirmed against the htmx QUIRKS page (all nine items, meta-tag config snippets, the default `responseHandling` list, `422` and swap-everything variants, `hx-include="closest form"`, `historyCacheSize`, loading and JavaScript API notes). Removed the invented Verify step; nothing else needed changing.
Method: documentation only; no commands were run.
