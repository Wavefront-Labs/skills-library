---
id: computing-software.web-development.htmx.htmx-http-verb-attributes
name: htmx-http-verb-attributes
category: computing-software
field: web-development
product: htmx
tags: [htmx, hx-get, hx-post, hx-put, hx-patch, hx-delete, ajax]
level: intro
status: docs-checked
description: "Issue GET, POST, PUT, PATCH or DELETE from any element with hx-get/post/put/patch/delete; defaults, params and DELETE response rules."
sources:
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/docs.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/attributes/hx-get.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/attributes/hx-post.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/attributes/hx-put.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/attributes/hx-patch.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/attributes/hx-delete.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: make any element issue an HTTP request and swap the HTML response into the page.

The five attributes each take a URL: `hx-get`, `hx-post`, `hx-put`, `hx-patch`, `hx-delete`.

```html
<button hx-put="/messages">Put To Messages</button>
<button hx-delete="/account" hx-target="body">Delete Your Account</button>
```

Defaults:
- Trigger is the element's natural event: `change` for `input`/`textarea`/`select`, `submit` for `form`, `click` for everything else.
- Target is the requesting element and the swap is `innerHTML` (so the first example loads the response into the button itself).
- None of these attributes is inherited; set `hx-target`, `hx-swap`, `hx-trigger` per element or hoist the inheritable ones to a parent.

Parameters:
- An element with a value (e.g. an input) sends it as a parameter unless removed with `hx-params`.
- `GET` and `DELETE` encode parameters in the URL (`htmx.config.methodsThatUseUrlParams` defaults to `["get", "delete"]`); other verbs use the body and also include the values of the enclosing form.
- An empty `hx-get=""` requests the current URL and swaps the current HTML page.

DELETE responses: to remove the element after success return `200` with an empty body; a `204` means no swap happens.

Responses should normally be HTML fragments, not JSON.

Related: `computing-software.web-development.htmx.htmx-request-parameters`, `...htmx-trigger-events-and-filters`.

## Checked

2026-11-07. Confirmed on docs.md (natural triggers, parameters section, `methodsThatUseUrlParams` default, 204/error handling) and attributes/hx-get.md, hx-post.md, hx-put.md, hx-patch.md, hx-delete.md (not inherited, default `innerHTML` swap into the requesting element, element value included unless removed, empty `hx-get`, DELETE 200-empty versus 204). The two cross-references are other library skills, not documentation claims.
Removed: the invented Verify step.
Method: documentation only; no commands were run.
