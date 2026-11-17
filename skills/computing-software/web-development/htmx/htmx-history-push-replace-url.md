---
id: computing-software.web-development.htmx.htmx-history-push-replace-url
name: htmx-history-push-replace-url
category: computing-software
field: web-development
product: htmx
tags: [htmx, hx-push-url, hx-replace-url, history, location-bar, back-button]
level: practitioner
status: docs-checked
description: "Update the browser URL and history from htmx with hx-push-url and hx-replace-url, their server-header overrides, and the full-page-on-restore rule."
sources:
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/attributes/hx-push-url.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/attributes/hx-replace-url.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/headers/hx-push-url.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/headers/hx-replace-url.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/docs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: make AJAX navigation behave like page navigation (shareable URLs, working back button).

`hx-push-url` creates a new history entry. Values: `true` (push the request URL), `false` (disable a push that would otherwise happen via inheritance or `hx-boost`), or a URL (relative or absolute, per `history.pushState()`).
```html
<a hx-get="/blog" hx-push-url="true">Blog</a>
<div hx-get="/account" hx-push-url="/account/home">Go to My Account</div>
```
Before the swap htmx snapshots the current DOM into its history cache (`localStorage`).

`hx-replace-url` takes the same three values but calls `history.replaceState()`, so no new entry is created (the previous current URL is effectively dropped).

Server overrides: response headers `HX-Push-Url` and `HX-Replace-Url` take the same values (a URL, or `false` to prevent the update) and override any attribute. For `HX-Replace-Url` the URL must have the same origin as the current URL. Neither header is processed on 3xx responses.

Both attributes are inherited. Events: `htmx:beforeHistoryUpdate` (modify `detail.history.path`/`type`), `htmx:pushedIntoHistory`, `htmx:replacedInHistory` (each with `detail.path`).

Critical rule: any URL you push must return a FULL page when requested directly (users paste it into email or a new tab), and htmx needs the full page when restoring history on a cache miss (that request carries the header `HX-History-Restore-Request` set to true).

`hx-history-elt` can narrow what gets snapshotted; see `htmx-history-cache-snapshots`.

## Checked

2026-11-07. Confirmed on attributes/hx-push-url.md and hx-replace-url.md (three values, inherited, snapshot to `localStorage`, header precedence), headers/hx-push-url.md and hx-replace-url.md (values, same-origin rule, 3xx note), events.md (`htmx:beforeHistoryUpdate`, `htmx:pushedIntoHistory`, `htmx:replacedInHistory`) and docs.md (full page required for pushed URLs, restore request header).
Removed: the invented Verify step.
Method: documentation only; no commands were run.
