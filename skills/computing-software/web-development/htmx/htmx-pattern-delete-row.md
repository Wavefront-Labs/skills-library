---
id: computing-software.web-development.htmx.htmx-pattern-delete-row
name: htmx-pattern-delete-row
category: computing-software
field: web-development
product: htmx
tags: [htmx, delete, table, hx-confirm, hx-swap, fade-out]
level: practitioner
status: docs-checked
description: "Delete table rows with htmx: put hx-confirm, hx-target closest tr and hx-swap outerHTML swap:1s on the tbody, return an empty 200, and fade the row out."
sources:
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/examples/delete-row.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/docs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: a delete button per row that confirms, deletes server-side, and removes the row with a fade.

Configure once on the `tbody`; the attributes are inherited by every button inside:

```html
<table class="table delete-row-example">
  <tbody hx-confirm="Are you sure?" hx-target="closest tr" hx-swap="outerHTML swap:1s">
    <tr>
      <td>Angie MacDowell</td><td>angie@macdowell.org</td><td>Active</td>
      <td><button class="btn danger" hx-delete="/contact/1">Delete</button></td>
    </tr>
  </tbody>
</table>
```

What each part does
- `hx-confirm` confirms the delete action.
- `hx-target="closest tr"` targets the enclosing row of whichever button was clicked (`hx-target` is inherited from parent elements).
- `hx-swap="outerHTML swap:1s"` replaces the whole target but waits 1 s after the response arrives, keeping the `htmx-swapping` class on the row during the wait.
- `hx-delete` issues a `DELETE` to the given URL.

The server deletes the record and responds `200` with empty content, so the row is replaced by nothing. docs.md notes that a `204 No Content` response by default does nothing (the content is ignored, no swap), so the example's `200` with empty content is what replaces the row with nothing.

Fade-out CSS that uses the swap delay:

```css
tr.htmx-swapping td { opacity: 0; transition: opacity 1s ease-out; }
```

Note: the `swap:1s` delay is what lets the CSS fade the row out before it is swapped and removed; the example styles the row's `td` cells.

## Checked

2026-11-07. Confirmed on examples/delete-row.md (table body attributes, inheritance of `hx-target`, `swap:1s`, fade CSS, per-row `hx-delete`, `200` with empty content) and docs.md (swapping class during the swap delay, 204 handling).
Fixed: removed the claim that `hx-confirm` shows the browser dialog and the "at least as long" rule, which the page does not state; the 204 sentence now follows docs.md. Removed the invented Verify step.
Method: documentation only; no commands were run.
