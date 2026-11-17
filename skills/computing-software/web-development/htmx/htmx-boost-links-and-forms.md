---
id: computing-software.web-development.htmx.htmx-boost-links-and-forms
name: htmx-boost-links-and-forms
category: computing-software
field: web-development
product: htmx
tags: [htmx, hx-boost, progressive-enhancement, accessibility, hx-boosted, navigation]
level: intro
status: docs-checked
description: "Convert normal links and forms to AJAX with hx-boost: defaults, limits, HX-Boosted header, disabling, and progressive-enhancement patterns."
sources:
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/attributes/hx-boost.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/docs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: speed up a conventional multi-page site with one attribute while keeping it working without JavaScript.

```html
<div hx-boost="true">
  <a href="/page1">Go To Page 1</a>
  <form action="/example" method="post"><input name="email"><button>Submit</button></form>
</div>
```

Behaviour:
- Anchors: click issues a `GET` to the `href`, targets `<body>` with `innerHTML` swap, and pushes the URL into history. Only the `click` trigger is fixed; target, swap etc. can be changed with the usual attributes.
- Forms: become `GET` or `POST` per the `method` attribute, triggered on `submit`, also targeting `body` with `innerHTML` and pushing the URL (set `hx-push-url="false"` to prevent that).
- `htmx.config.scrollIntoViewOnBoost` defaults to `true`: the target of a boosted element is scrolled into the viewport. If `hx-target` is omitted the target is `body`, so the page scrolls to the top.

Notes:
- `hx-boost` is inherited. Switch it off for part of a tree with `hx-boost="false"`.
- Only same-domain links that are not local anchors (`#...`) are boosted.
- Everything runs over AJAX, so think about redirects; the server can detect boosted requests via the `HX-Boosted` request header.
- `hx-preserve="true"` stops listed elements, and their children, being replaced by boosted swaps.
- `hx-boost` does not update the `<html>` or `<body>` tags (docs.md, CSRF section).

Progressive enhancement: with JS disabled boosted links and forms continue to work as normal. Other patterns need more thought; e.g. wrap an active-search input in `<form action="/search" method="POST">` with a mirrored `hx-post="/search"`, and use the `HX-Request` header server-side to choose full page vs fragment. Keep normal accessibility practice: semantic HTML, visible focus, labels on fields.

## Checked

2026-11-07. Confirmed on hx-boost.md (anchor and form behaviour, body target, `innerHTML`, `hx-push-url` false, same-domain and local-anchor limits, `hx-boost="false"`, `hx-preserve`, `HX-Boosted`), docs.md (progressive enhancement, `HX-Request`, accessibility list, CSRF note that boost does not update `<html>`/`<body>`) and reference.md (`scrollIntoViewOnBoost`, `HX-Boosted`).
Removed: the `show:top` default, `hx-swap="show:none"`, the `HX-Boosted: true` literal value and the invented Verify step; none appear on the cited pages.
Method: documentation only; no commands were run.
