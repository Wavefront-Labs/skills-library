---
id: computing-software.web-development.htmx.htmx-pattern-click-to-edit
name: htmx-pattern-click-to-edit
category: computing-software
field: web-development
product: htmx
tags: [htmx, click-to-edit, inline-editing, hx-target, outerhtml, forms]
level: practitioner
status: docs-checked
description: "Build inline edit-in-place for a record with htmx: a display view swaps itself for a form via hx-get, the form PUTs back and swaps the display view in."
sources:
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/examples/click-to-edit.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: edit all or part of a record inline, without a page refresh, using only two server fragments (display and form).

1. Display fragment. The wrapper targets itself and swaps its own outer HTML; the button fetches the edit form:

```html
<div hx-target="this" hx-swap="outerHTML">
  <div><label>First Name</label>: Joe</div>
  <div><label>Email</label>: joe@blow.com</div>
  <button hx-get="/contact/1/edit" class="btn primary">Click To Edit</button>
</div>
```

2. `GET /contact/1/edit` returns a form that replaces the display div. It PUTs to the record URL (the usual REST shape) and also targets itself:

```html
<form hx-put="/contact/1" hx-target="this" hx-swap="outerHTML">
  <label for="firstName">First Name</label>
  <input autofocus type="text" id="firstName" name="firstName" value="Joe">
  <input type="email" name="email" value="joe@blow.com">
  <button type="submit">Submit</button>
  <button hx-get="/contact/1">Cancel</button>
</form>
```

3. `PUT /contact/1` saves and responds with the display fragment from step 1 (now with the new values). The Cancel button GETs `/contact/1` (the display fragment) again.

Notes
- `hx-target="this"` plus `hx-swap="outerHTML"` on the wrapper and on the form replaces that element with the response.
- The page's server code builds the form (with `autofocus` and a `for`/`id` pair on the first input) and the display fragment from the same contact data.
- For tables use the row variant (see htmx-pattern-edit-row).

## Checked

2026-11-07. Confirmed on examples/click-to-edit.md (display markup, edit form, `GET /contact/1/edit`, `PUT /contact/1`, Cancel `hx-get`, and the fake server's routes and templates).
Removed: the unconfirmed notes on id syncing, form value inclusion and cursor focus, the template-sharing advice, and the invented Verify step.
Method: documentation only; no commands were run.
