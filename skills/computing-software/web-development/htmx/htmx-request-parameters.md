---
id: computing-software.web-development.htmx.htmx-request-parameters
name: htmx-request-parameters
category: computing-software
field: web-development
product: htmx
tags: [htmx, hx-include, hx-params, parameters, forms, configrequest]
level: practitioner
status: docs-checked
description: "Control which values an htmx request sends: implicit form values, hx-include selectors, hx-params filtering, and htmx:configRequest edits."
sources:
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/docs.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/attributes/hx-include.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/attributes/hx-params.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/events.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/api.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: send exactly the field values the server needs.

Defaults: an element sending a request includes its own value if it has one; a form includes all its inputs; parameter names come from `name`. For non-GET requests the values of the associated form (nearest enclosing form, or one set via `<button form="id">`) are also included.

`hx-include` - add other elements' values. Value is one of: CSS selector (all matches, via querySelectorAll), `this` (descendants), `closest <sel>`, `find <sel>`, `next <sel>`, `previous <sel>` (extended ones return a single element). Including a non-input element includes all inputs inside it. Disabled inputs are ignored. Inherited; `inherit, [name='email']` adds to a parent value.
```html
<button hx-post="/register" hx-include="[name='email']">Register!</button>
Enter email: <input name="email" type="email"/>
```
Gotcha: inherited `hx-include="find input"` is resolved from the requesting element, not the element holding the attribute; a button without input children then errors.

`hx-params` - filter parameters: `*` (all, default), `none`, `not <a,b>` (all except), `<a,b>` (only those). Inherited.
```html
<div hx-get="/example" hx-params="*">Get Some HTML, Including Params</div>
```

Programmatic edit in `htmx:configRequest` (`detail.parameters`, `detail.unfilteredParameters`, `detail.headers`, `detail.elt`, `detail.target`, `detail.verb`); a repeated input name yields an array:
```javascript
document.body.addEventListener('htmx:configRequest', e => { e.detail.parameters['auth_token'] = getAuthToken(); });
```
Extra constants: see `htmx-vals-and-headers-attributes`. Inspect resolved values with `htmx.values(elt, 'post')`.

## Checked

2026-11-07. Confirmed against the htmx docs Parameters section, the hx-include and hx-params references, the events page (`htmx:configRequest` details, array for repeated names) and the API page (`htmx.values`, defaults to `post`). Added the API page to `sources`; removed the invented Verify step. No claims needed trimming.
Method: documentation only; no commands were run.
