---
id: computing-software.web-development.htmx.htmx-pattern-edit-row
name: htmx-pattern-edit-row
category: computing-software
field: web-development
product: htmx
tags: [htmx, edit-row, table, hx-include, custom-events, hx-trigger]
level: practitioner
status: docs-checked
description: "Editable table rows with htmx: swap a row for inputs, save with hx-put plus hx-include closest tr, and allow only one row in edit mode via custom events."
sources:
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/examples/edit-row.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: row-level editing in a table where only one row is editable at a time.

Table body: every request from inside targets and replaces its own row.

```html
<tbody hx-target="closest tr" hx-swap="outerHTML"> ... </tbody>
```

Read-only row. The Edit button listens for a custom `edit` event instead of click, so JavaScript can decide whether the request is allowed:

```html
<tr>
  <td>${contact.name}</td><td>${contact.email}</td>
  <td>
    <button class="btn danger" hx-get="/contact/${contact.id}/edit" hx-trigger="edit"
            onClick="let editing = document.querySelector('.editing')
                     if (editing) { /* confirm, then: */
                       htmx.trigger(editing, 'cancel'); htmx.trigger(this, 'edit')
                     } else { htmx.trigger(this, 'edit') }">Edit</button>
  </td>
</tr>
```

The example asks for confirmation with SweetAlert2 before cancelling the other row. On confirm it fires `cancel` on the row being edited and `edit` on this button.

Editing row. It carries the `editing` class, listens for `cancel`, and uses `hx-include` because a `form` cannot live directly inside a `tr`:

```html
<tr hx-trigger='cancel' class='editing' hx-get="/contact/${contact.id}">
  <td><input autofocus name='name' value='${contact.name}'></td>
  <td><input name='email' value='${contact.email}'></td>
  <td>
    <button class="btn danger" hx-get="/contact/${contact.id}">Cancel</button>
    <button class="btn danger" hx-put="/contact/${contact.id}" hx-include="closest tr">Save</button>
  </td>
</tr>
```

Notes
- Without the one-at-a-time rule you can drop the JavaScript and custom `hx-trigger`; a plain click on `hx-get` works.
- Another way to enforce exclusivity is to target the whole table when Edit is clicked.
- `hx-include="closest tr"` sends every input in that row with the PUT.
- The cancel path simply re-GETs the read-only row.

## Checked

2026-11-07. Confirmed on examples/edit-row.md (tbody attributes, read-only row and its custom `edit` trigger, SweetAlert2 confirm and `cancel` event, editing row with `hx-include`, the notes on dropping the JavaScript or targeting the table).
Removed: the invented Verify step.
Method: documentation only; no commands were run.
