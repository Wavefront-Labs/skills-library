---
id: computing-software.web-development.htmx.htmx-ext-response-targets
name: htmx-ext-response-targets
category: computing-software
field: web-development
product: htmx
tags: [htmx, extensions, response-targets, error-handling, hx-target, status-codes]
level: practitioner
status: docs-checked
description: "Swap error responses into their own targets with the htmx response-targets extension: hx-target-404, hx-target-5*, hx-target-error, wildcard lookup order and config flags."
sources:
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/extensions/response-targets.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: choose the swap target by HTTP status, so 4xx/5xx bodies show in an error area instead of being dropped.

Install: load the extension after core htmx (npm package `htmx-ext-response-targets`, file `dist/response-targets.js`) and enable it with `hx-ext="response-targets"` on a parent that contains the `hx-target` and `hx-target-...` attributes.

```html
<div hx-ext="response-targets">
  <div id="response-div"></div>
  <button hx-post="/register"
          hx-target="#response-div"
          hx-target-5*="#serious-errors"
          hx-target-404="#not-found">Register!</button>
  <div id="serious-errors"></div>
  <div id="not-found"></div>
</div>
```
200 goes to `#response-div`, any 5xx to `#serious-errors`, 404 to `#not-found`. To treat all errors alike use `hx-target-error="#any-errors"` (4xx and 5xx; 2xx behaves as before).

Wildcard resolution. If no exact `hx-target-[CODE]` exists, the last digit is replaced by `*` repeatedly. For 404 the lookup order is `hx-target-404`, `hx-target-40*`, `hx-target-4*`, `hx-target-*`. If your tooling rejects `*` in attribute names, use `x`, for example `hx-target-4xx`.

Notes
- `hx-target-...` is inherited, so it can sit on a parent.
- It cannot handle status 200.
- It honours the `HX-Retarget` response header by default and prefers it over its own calculated target.

Config flags (set on `htmx.config`)
- `responseTargetPrefersRetargetHeader` (default `true`): set `false` to ignore `HX-Retarget` when an `hx-target-...` matches. With the header present the extension's own lookup is disabled but error responses still swap.
- `responseTargetPrefersExisting` (default `false`): `true` keeps a target set earlier by htmx or other extensions instead of overwriting it; the page calls this risky.
- `responseTargetUnsetsError` (default `true`): `isError` on the event `detail` is set to `false` when an error status is swapped via `hx-target-[CODE]`.
- `responseTargetSetsError` (default `false`): controls how `isError` on the event `detail` is handled when a non-error code is swapped via `hx-target-[CODE]`; never affects 200 (the page's wording is terse, so read it before relying on it).

## Checked

2026-11-07. Confirmed on extensions/response-targets.md (attribute forms, `hx-target-error`, example, wildcard lookup order and the `x` alternative, notes, and the four `htmx.config.responseTarget*` flags with defaults), plus the npm package and file names from its install section.
Trimmed: the `responseTargetSetsError` description, which the page does not state as "sets isError"; the invented Verify step.
Method: documentation only; no commands were run.
