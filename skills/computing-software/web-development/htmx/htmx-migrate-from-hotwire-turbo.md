---
id: computing-software.web-development.htmx.htmx-migrate-from-hotwire-turbo
name: htmx-migrate-from-hotwire-turbo
category: computing-software
field: web-development
product: htmx
tags: [htmx, migration, hotwire, turbo, hx-boost, stimulus, hx-swap-oob]
level: practitioner
status: docs-checked
description: "Map Hotwire/Turbo features to htmx: Turbo Drive to hx-boost, Frames and Streams to core attributes, request interception events, disabling buttons on submit, Stimulus."
sources:
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/migration-guide-hotwire-turbo.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: translate Hotwire / Turbo behaviours into htmx equivalents.

Turbo Drive
- `<body hx-boost="true">` gives a Turbo Drive-like experience; like Turbo Drive it still works with JavaScript disabled.
- `hx-boost="false"` equals `data-turbo="false"` and turns boosting off for a specific link or form.
- Redirect after form submission (302, 303, 307 and other 3xx): `hx-target="body" hx-swap="outerHTML" hx-push-url="true"`.
- Disable buttons during submission. Disable buttons only, because a `form` does not submit disabled fields:

```javascript
addEventListener("submit", (event) => {
    event.target.querySelectorAll("button").forEach(node => { node.disabled = true })
})
addEventListener("htmx:afterOnLoad", (event) => {
    event.target.querySelectorAll("button").forEach(node => { node.disabled = false })
})
```
Inline alternatives: `hx-on:submit='...disabled = true'` plus `hx-on:htmx:afterOnLoad='...disabled = false'` with the same bodies, or hyperscript `_="on submit toggle @disabled <button/> in me until htmx:afterOnLoad"`.

Turbo Frames: htmx folds them into the base attributes, so no `<turbo-frame>` element is needed. Lazy loading becomes `hx-trigger="load, submit"`.

Turbo Streams: also folded in, with no `<turbo-stream>` or `<template>`. Streams can act anywhere on the page, similar to `hx-select-oob` and `hx-swap-oob`; Frames only update what they wrap.

Intercepting or pausing requests (`turbo:before-fetch-request`): use `htmx:configRequest` (same as `htmx:config-request`):

```javascript
document.body.addEventListener('htmx:configRequest', (event) => {
    event.detail.headers['Authorization'] = `Bearer ${token}`
})
```
Other options: an `hx-trigger` condition such as `hx-trigger="submit[action(target)]"` (does not resolve async calls; htmx issue 912); `hx-on:click="event.preventDefault(); action(this); htmx.trigger(this, 'ready')"` with `hx-trigger="ready"`; or hyperscript `_="on submit halt the event action(target) trigger ready"` with `hx-trigger="ready"`, which does resolve async calls such as `fetch`.

Stimulus: `hx-on` is an inline vanilla substitute for many cases; hyperscript is a close analogue and official companion project, though the two are fully separate.

## Checked

2026-11-07. Confirmed on migration-guide-hotwire-turbo.md (Turbo Drive, Frames, Streams, Events and Stimulus sections, including the button-disabling samples, the `hx-trigger` condition caveat and issue 912).
Removed: the invented Verify step.
Method: documentation only; no commands were run.
