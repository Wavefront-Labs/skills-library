---
id: computing-software.web-development.htmx.htmx-pattern-update-other-content
name: htmx-pattern-update-other-content
category: computing-software
field: web-development
product: htmx
tags: [htmx, hx-swap-oob, hx-trigger, hx-target, path-deps, out-of-band, events]
level: practitioner
status: docs-checked
description: "Update a second region after a form POST in htmx: widen hx-target, send an hx-swap-oob fragment, fire an HX-Trigger event the table listens for, or use the path-deps extension."
sources:
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/examples/update-other-content.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: a form `POST /contacts` must also refresh `<tbody id="contacts-table">` elsewhere on the page. Four solutions, in the source's recommended order.

1. Expand the target (simplest, most reliable when elements are near each other). Wrap table and form in `<div id="table-and-form">`, set `hx-target="#table-and-form"` on the form `hx-post="/contacts"`, and have the POST response render both the table and the form.

2. Out-of-band swap. HTML stays unchanged; the POST response contains an extra fragment that appends itself to the table, followed by the re-rendered form fields:

```html
<tbody hx-swap-oob="beforeend:#contacts-table">
  <tr><td>Joe Smith</td><td>joe@smith.com</td></tr>
</tbody>
<label>Name <input name="name" type="text"></label>
<label>Email <input name="email" type="email"></label>
```

3. Trigger an event. Make the table refresh itself on a custom event:

```html
<tbody id="contacts-table" hx-get="/contacts/table" hx-trigger="newContact from:body">
```

On successful creation the POST response carries the header `HX-Trigger:newContact`. The event bubbles to `body`, where `from:body` catches it, and the table issues `GET /contacts/table`, which re-renders the whole table including the new row.

4. Path dependencies extension (`path-deps`, from the htmx-extensions repo). Load the extension JS, then:

```html
<tbody id="contacts-table" hx-get="/contacts/table" hx-ext="path-deps"
       hx-trigger="path-deps" path-deps="/contacts">
```

When the form posts to `/contacts`, the extension triggers a `path-deps` event on the table. No response headers are needed, but a request is issued on every POST, even if no contact was created.

Which to use: the source recommends 1 first, then a toss-up between 2 and 3 (the author leans to events; choose by which fits your server stack), path-deps last.

## Checked

2026-11-07. Confirmed against the htmx Updating Other Content example page (all four solutions and their code, `HX-Trigger:newContact`, `from:body`, path-deps trade-offs, the author's recommended order). Narrowed the path-deps trigger wording to the form POST the page describes and removed the invented Verify step.
Method: documentation only; no commands were run.
