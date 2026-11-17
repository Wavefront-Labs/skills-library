---
id: computing-software.web-development.htmx.htmx-response-headers
name: htmx-response-headers
category: computing-software
field: web-development
product: htmx
tags: [htmx, response-headers, hx-location, hx-redirect, hx-refresh, hx-retarget, hx-reswap]
level: practitioner
status: docs-checked
description: "Server-side control of htmx via response headers: HX-Location vs HX-Redirect, HX-Refresh, HX-Retarget, HX-Reswap, HX-Reselect and URL headers; 3xx caveat."
sources:
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/headers/hx-location.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/headers/hx-redirect.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/docs.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/reference.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: pick the right response header to redirect, retarget or refresh from the server.

Header list:
- `HX-Location` - client-side redirect without a full reload.
- `HX-Redirect` - client-side redirect that does a full page reload.
- `HX-Refresh: true` - full refresh of the current page.
- `HX-Push-Url` / `HX-Replace-Url` - update the URL bar (see `htmx-history-push-replace-url`).
- `HX-Reswap` - override swap style (same values as `hx-swap`).
- `HX-Retarget` - CSS selector that changes the target element.
- `HX-Reselect` - CSS selector choosing which part of the response to swap; overrides `hx-select` on the triggering element.
- `HX-Trigger`, `HX-Trigger-After-Swap`, `HX-Trigger-After-Settle` - client events (see `htmx-hx-trigger-response-headers`).

HX-Location: acts like clicking an `hx-boost` link (AJAX request, history entry, pushes path). Plain: `HX-Location: /test`. With options as JSON: `HX-Location: {"path":"/test2", "target":"#testdiv"}`. `path` is required; other keys mirror the `htmx.ajax` context: `source`, `event`, `handler`, `target`, `swap`, `values`, `headers`, `select`, `push` (`'false'` or a path to prevent/override the pushed URL), `replace` (path string).

HX-Redirect: `HX-Redirect: /test` makes the browser load the URL as if typed or via a non-boosted link, useful for non-htmx endpoints with different `<head>` content or scripts.

Critical gotcha: none of the response headers are processed on 3xx responses, because the browser intercepts the redirection internally and returns the headers and response from the redirected URL. Where possible use an alternative code such as 200 to return these headers. After a successful POST you can return the new HTML fragment directly instead of the Post/Redirect/Get pattern.

## Checked

2026-11-07. Confirmed against the HX-Location and HX-Redirect pages (behaviour, JSON options, `path` required, `push`/`replace`), the reference Response Headers table, and the docs Response Headers/Post-Redirect-Get passages (3xx caveat). Reworded the 3xx explanation to the docs' own wording and removed the invented Verify step.
Method: documentation only; no commands were run.
