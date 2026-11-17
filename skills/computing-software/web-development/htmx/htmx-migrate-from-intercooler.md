---
id: computing-software.web-development.htmx.htmx-migrate-from-intercooler
name: htmx-migrate-from-intercooler
category: computing-software
field: web-development
product: htmx
tags: [htmx, migration, intercooler, hyperscript, path-deps, headers, events]
level: practitioner
status: docs-checked
description: "Map intercooler.js attributes, request parameters, headers, events, JS methods and meta tags to htmx equivalents, with extension and hyperscript workarounds."
sources:
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/migration-guide-intercooler.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: port an intercooler.js (`ic-*`) app to htmx. htmx keeps a small core of loading and swapping attributes; client-side conveniences move to hyperscript, events, or extensions.

Attributes with direct equivalents
- `ic-get-from`/`ic-post-to`/`ic-put-to`/`ic-patch-to`/`ic-delete-from` map to `hx-get`/`hx-post`/`hx-put`/`hx-patch`/`hx-delete`.
- `ic-target` to `hx-target`; `ic-swap-style` to `hx-swap`; `ic-select-from-response` to `hx-select`; `ic-confirm` to `hx-confirm`; `ic-prompt` to `hx-prompt`; `ic-push-url` to `hx-push-url`; `ic-include` to `hx-include`; `ic-indicator` to `hx-indicator`; `ic-history-elt` to `hx-history-elt`; `ic-enhance` to `hx-boost`; `ic-trigger-on` to `hx-trigger`; `ic-trigger-delay` to `hx-trigger` modifiers; `ic-trigger-from` to the `from:` clause.
- `ic-replace-target` is `hx-swap="outerHTML"`; `ic-append-from` and `ic-prepend-from` are approximated with `hx-get` plus `hx-swap` (the guide names `beforeend` for both).
- `ic-scroll-to-target`: see the `scroll` and `show` swap modifiers.
- `ic-deps` becomes `hx-trigger="path-deps"` with `path-deps="/foo/bar"` (needs the `path-deps` extension). `ic-src` needs `hx-get` with triggers or `path-deps`.
- `ic-poll`/`ic-poll-repeats`: `<div hx-get="/news" hx-trigger="every 2s"></div>`.
- `ic-verb`: htmx sends the real HTTP method; to send non-GET verbs as POST use the `method-override` extension.
- `ic-transform-response`: the `client-side-templates` extension (mustache, handlebars, nunjucks).
- `ic-global-include` and `ic-global-indicator`: no equivalent, but `hx-include` and `hx-indicator` give similar results. `ic-local-vars`: `hx-vars` could help.

No equivalent, use hyperscript: `ic-action`, `ic-action-target`, `ic-add-class`, `ic-remove-class`, `ic-remove-after`, `ic-switch-class` (with `htmx:beforeOnLoad`), and the `ic-on-*` callbacks (use events such as `htmx:beforeRequest`, `htmx:afterRequest`), e.g. `<button _="on click add .clicked">`.

Gaps named by the guide (no direct equivalent): `ic-attr-src`, `ic-disable-when-doc-hidden`, `ic-disable-when-doc-inactive`, `ic-fix-ids`, `ic-limit-children`, `ic-style-src`, `ic-scroll-offset`.

Request side: `ic-request` is the `HX-Request` header; `ic-target-id`, `ic-trigger-id`, `ic-trigger-name`, `ic-current-url`, `ic-prompt-value` become the `HX-Target`, `HX-Trigger`, `HX-Trigger-Name`, `HX-Current-URL` and `HX-Prompt` headers. `X-IC-Request` is `HX-Request`.

Response headers: `X-IC-Trigger` to `HX-Trigger` (also `HX-Trigger-After-Settle`, `HX-Trigger-After-Swap`); `X-IC-Refresh` to `HX-Refresh`; `X-IC-Redirect` to `HX-Redirect`; `X-IC-PushURL` to `HX-Push`; `X-IC-CancelPolling` to HTTP status `286`; `X-IC-SetPollInterval`: with load polling, return content with a different interval.

Events (htmx fires both camelCase and kebab-case): `beforeAjaxSend.ic` to `htmx:configRequest`; `beforeSend.ic` to `htmx:beforeRequest`; `success.ic` to `htmx:afterOnLoad`; `complete.ic` to `htmx:afterRequest`; `elementAdded.ic` to `htmx:load`; `beforeHistorySnapshot.ic` to `htmx:beforeHistorySave`; `error.ic` to one of the error events (`htmx:sendError`, `htmx:sseError`, `htmx:responseError`, `htmx:swapError`, `htmx:onLoadError`; the guide marks this one TBC).

JS API: `Intercooler.triggerRequest` to `htmx.trigger()`; `processNodes` to `htmx.process()`; `closestAttrValue` to `htmx.closest()`; `Intercooler.ready` to `htmx.onLoad()`; `Intercooler.refresh` to `PathDeps.refresh()`.

Meta tags: `intercoolerjs:use-data-prefix` is unnecessary since `data-hx-post="/click"` works automatically.

## Checked

2026-11-07. Confirmed on migration-guide-intercooler.md (attribute, request parameter, request and response header, event, JS method and meta tag tables, and the approach notes).
Fixed: the `error.ic` mapping now includes `htmx:sseError` and the TBC mark. Removed the invented Verify step.
Method: documentation only; no commands were run.
