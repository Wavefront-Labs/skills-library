---
id: computing-software.web-development.htmx.htmx-partial-swap-commands
name: htmx-partial-swap-commands
category: computing-software
field: web-development
product: htmx
tags: [htmx, hx-partial, swap-command, multi-target, template, processtemplate]
level: advanced
status: docs-checked
description: "Server-sent multi-target swaps with the hx-partial tag: targets, id shorthand, swap styles, partials-only responses, template fallback and events."
sources:
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/attributes/hx-partial.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/docs.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/events.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: let the server direct several swaps from one response using an envelope that is never inserted into the page. (Present in the source docs for this htmx version; check your installed version supports it.)

```html
<div>Updated main content</div>
<hx-partial hx-target="#notifications">3 new messages</hx-partial>
<hx-partial hx-target="#user-status" hx-swap="outerHTML"><span id="user-status">Online</span></hx-partial>
```

Rules:
- `hx-target` on a partial is resolved relative to the triggering element, with the extended selectors (`closest tr`, `find .status`, `next`, `previous`).
- `hx-swap` takes any normal `hx-swap` value; default `innerHTML`.
- id shorthand: `<hx-partial id="alerts">` equals `hx-target="#alerts"`.
- Partials run in document order, all before the main swap, like OOB swaps.
- If the response contains only partials, the main swap is suppressed and the original target is untouched.
- Inert fallback form so a mis-rendered full page does not show raw tags: `<template hx type="partial" hx-target="#alerts">Saved!</template>`.
- htmx converts partials into `<template>` elements before parsing, so `<tr>`, `<td>`, `<li>` survive. For strict template engines, wrap in valid markup: `<template hx type="partial" hx-target="find tbody" hx-swap="beforeend"><table><tbody><tr><td>New row</td></tr></tbody></table></template>`.
- Attributes on partials are not inherited. Partials with no matching target are ignored silently (fires `htmx:partialErrorNoTarget` on body).
- Can coexist with `hx-swap-oob`.

Events: `htmx:partialBeforeSwap` (cancel with `shouldSwap=false`, change `detail.target`, replace `detail.fragment`), `htmx:partialAfterSwap`, `htmx:partialErrorNoTarget`, and `htmx:processTemplate` for other `<hx-*>` tags such as `<hx-toast>` (`detail.type`, `detail.template`).

## Checked

2026-11-07. Confirmed on attributes/hx-partial.md (every rule and example above, template fallback, table wrapper, events list, notes) and events.md (`htmx:partialBeforeSwap` cancel, retarget and fragment replace; `htmx:partialAfterSwap`; `htmx:partialErrorNoTarget` on body; `htmx:processTemplate` with `detail.type` and `detail.template`). This page is from the master docs, which also describe htmx 4 items; the 2.0.11 install pages do not mention it.
Removed: the invented Verify step.
Method: documentation only; no commands were run.
