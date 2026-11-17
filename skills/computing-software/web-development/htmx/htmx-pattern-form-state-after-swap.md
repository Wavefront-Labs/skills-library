---
id: computing-software.web-development.htmx.htmx-pattern-form-state-after-swap
name: htmx-pattern-form-state-after-swap
category: computing-software
field: web-development
product: htmx
tags: [htmx, forms, hx-preserve, file-input, reset, hx-on, after-request]
level: practitioner
status: docs-checked
description: "Control form state around htmx swaps: keep a chosen file with hx-preserve or the form attribute after validation errors, and clear inputs with hx-on::after-request."
sources:
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/examples/file-upload-input.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/examples/reset-user-input.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/attributes/hx-preserve.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: stop forms from losing input they should keep (a file) or keeping input they should lose (a submitted note).

A. Keep a file input when the form is re-rendered with errors. Re-swapping a form that contains `<input type="file">` empties the file, forcing a re-upload. Two fixes:

1. Put `hx-preserve` on the file input (it needs a stable `id`):

```html
<form method="POST" id="binaryForm" enctype="multipart/form-data" hx-swap="outerHTML" hx-target="#binaryForm">
  <input hx-preserve id="someId" type="file" name="binaryFile">
  <!-- other fields, error messages -->
  <button type="submit">Submit</button>
</form>
```
Put `hx-preserve` only on the `input`, not on the element that shows its errors, so errors still appear. To discard the file (e.g. wrong type), have the server omit `hx-preserve` when that field has the error.

2. Or move the input outside the swapped region and link it with the `form` attribute:

```html
<input form="binaryForm" type="file" name="binaryFile">
<form method="POST" id="binaryForm" enctype="multipart/form-data" hx-swap="outerHTML" hx-target="#binaryForm">
  <button type="submit">Submit</button>
</form>
```

B. Reset inputs after a successful request. Use an `hx-on` handler on the after-request event and only reset when the response has a 20x status code:

```html
<form hx-post="/note" hx-target="#notes" hx-swap="afterbegin"
      hx-on::after-request="if(event.detail.successful) this.reset()">
  <input type="text" name="note-text" placeholder="blank canvas">
  <button class="btn">Add</button>
</form>
<ul id="notes"></ul>
```

`reset()` exists only on `form` elements. For a non-form control, include the input and clear it by hand:

```html
<button hx-post="/note" hx-target="#notes" hx-swap="afterbegin" hx-include="#note-input"
        hx-on::after-request="if(event.detail.successful) document.getElementById('note-input').value = ''">Add</button>
```

## Checked

2026-11-07. Confirmed against the htmx pages "Preserving File Inputs after Form Errors", "Reset user input" and the hx-preserve reference (stable `id` required, error display, server omitting `hx-preserve`, `form` attribute restructuring, `hx-on::after-request`, `event.detail.successful`, 20x, `reset()` form-only). Corrected the non-form example target to `#notes` to match its list. Removed the invented Verify step.
Method: documentation only; no commands were run.
