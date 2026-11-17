---
id: computing-software.web-development.htmx.htmx-vals-and-headers-attributes
name: htmx-vals-and-headers-attributes
category: computing-software
field: web-development
product: htmx
tags: [htmx, hx-vals, hx-headers, hx-vars, json, csrf, js-prefix]
level: practitioner
status: docs-checked
description: "Add extra values and request headers with hx-vals and hx-headers: JSON syntax rules, the js: prefix, precedence, hx-vars deprecation and CSRF use."
sources:
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/attributes/hx-vals.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/attributes/hx-headers.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/attributes/hx-vars.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/docs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: attach constant or computed parameters and headers to requests declaratively.

`hx-vals` - extra parameters as JSON:
```html
<div hx-get="/example" hx-vals='{"myVal": "My Value"}'>Get</div>
<button hx-post="/submit" hx-vals='{"action": "save", "draft": "true"}'>Save as Draft</button>
```
- Works with all verbs; on GET the values are query parameters.
- Evaluate JavaScript with a `js:` or `javascript:` prefix: `hx-vals='js:{myVal: calculateValue()}'`, `hx-vals='js:{lastKey: event.key}'` (the `event` is available), spread works: `hx-vals='js:{...foo()}'`. `this` is the element.
- JSON must be valid. `hx-vals="{'a': 'b'}"` (single quotes inside) is ignored with a console error; use single quotes for the attribute and double quotes inside, or, if the attribute itself uses double quotes, escape the inner double quotes.
- Inherited; a child declaration overrides the parent; a declared value overrides an input with the same name.

`hx-headers` - extra request headers, JSON by default with an optional `javascript:` / `js:` prefix to evaluate:
```html
<div hx-get="/example" hx-headers='{"myHeader": "My Value"}'>Get</div>
```
Inherited; a child header overrides a parent. Put it on `<body>`/`<html>` for global values such as `hx-headers='{"X-CSRF-TOKEN": "CSRF_TOKEN_INSERTED_HERE"}'` (far from a foolproof CSRF solution; it can support backend CSRF prevention. `hx-boost` does not update the `html` or `body` tags, so with boost put the token on an element that will get replaced).

`hx-vars` is deprecated (comma-separated `name:expression`, expressions are dynamically computed, e.g. `hx-vars="myVar:computeMyVar()"`); prefer `hx-vals`, which is safer by default. `hx-vars` is inherited, a child overrides a parent, and declared values override same-named inputs.

Security: the `js:` / `javascript:` forms are dynamically evaluated and can introduce XSS, especially with user input such as query strings or user-generated content. `htmx.config.allowEval=false` disables `hx-vals` and `hx-headers` with the `js:` prefix.

## Checked

2026-11-07. Confirmed against the hx-vals, hx-headers and hx-vars references (JSON default, `js:` / `javascript:` prefix, `event` access, spread, all-verbs and GET behaviour, JSON syntax rules and console error, inheritance and override notes, `this`, deprecation, security notes) and the docs (`allowEval` list, CSRF Prevention section and the `hx-boost` caveat). Reworded the headers line, CSRF note and security note to the pages' wording, added the hx-vars inheritance facts, and replaced an HTML-entity example with prose. Removed the invented Verify step.
Method: documentation only; no commands were run.
