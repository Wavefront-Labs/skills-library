---
id: computing-software.web-development.htmx.htmx-pattern-dependent-selects
name: htmx-pattern-dependent-selects
category: computing-software
field: web-development
product: htmx
tags: [htmx, select, cascading-selects, hx-get, hx-target, forms]
level: intro
status: docs-checked
description: "Cascading selects with htmx: the make select GETs /models on change and its response replaces the options of the model select, with a spinner indicator."
sources:
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/examples/value-select.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/docs.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/attributes/hx-get.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: make the options of one `select` depend on the value chosen in another.

Render the page with a default make (Audi) and the models list for that make already in the second select. Then let the first select fetch replacement options:

```html
<div>
  <label>Make</label>
  <select name="make" hx-get="/models" hx-target="#models" hx-indicator=".htmx-indicator">
    <option value="audi">Audi</option>
    <option value="toyota">Toyota</option>
    <option value="bmw">BMW</option>
  </select>
</div>
<div>
  <label>Model</label>
  <select id="models" name="model">
    <option value="a1">A1</option>
    ...
  </select>
  <img class="htmx-indicator" width="20" src="/img/bars.svg" alt="Saving...">
</div>
```

How it works
- A `select` is triggered on the `change` event by default (docs.md), and an element's own value is included as a parameter (hx-get.md), so choosing a make sends a GET to `/models` with the select's `make` value; the example's fake server reads `params['make']`.
- `hx-target="#models"` aims the response at the model select; the default swap is `innerHTML` (docs.md), and the example's server returns only `option` elements:

```html
<option value='325i'>325i</option>
<option value='325ix'>325ix</option>
<option value='X5'>X5</option>
```

- `hx-indicator` points at the spinner, which becomes visible while the request is in flight.

Note: the page starts with a default make (Audi) and renders the model select for it; the GET happens when the make select changes.

## Checked

2026-11-07. Confirmed on examples/value-select.md (markup, `/models` GET, returned options, fake server) and docs.md (select triggers on `change`, default `innerHTML`, request indicators), plus attributes/hx-get.md (element value included as a parameter).
Removed: the `outerHTML` gotcha and the form-submission claim in the invented Verify step, neither of which the page states.
Method: documentation only; no commands were run.
