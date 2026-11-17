---
id: computing-software.web-development.htmx.htmx-pattern-bulk-update
name: htmx-pattern-bulk-update
category: computing-software
field: web-development
product: htmx
tags: [htmx, bulk-update, checkboxes, forms, toast, accessibility]
level: practitioner
status: docs-checked
description: "Bulk-update table rows with htmx: wrap the table in a form, post checkbox state in one request, and answer with a fading toast inside an output element."
sources:
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/examples/bulk-update.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/docs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: select several rows, apply one server update, and tell the user the outcome without re-rendering the table.

Markup: a form around the table, one checkbox per row, results shown in an `output` element.

```html
<form id="checked-contacts" hx-post="/users" hx-swap="innerHTML settle:3s" hx-target="#toast">
  <table>
    <tbody id="tbody">
      <tr>
        <td>Joe Smith</td><td>joe@smith.org</td>
        <td><input type="checkbox" name="active:joe@smith.org"></td>
      </tr>
    </tbody>
  </table>
  <input type="submit" value="Bulk Update" class="btn primary">
  <output id="toast"></output>
</form>
```

Server (as in the example's fake server): params look like `{"active:joe@smith.org":"on", ...}`. It treats a listed email as active and every other known user as inactive, applies the changes, and returns text such as `Activated 1 and deactivated 2 users`.

Fade-out toast using the settle phase (the `settle:3s` in hx-swap keeps the `htmx-settling` class on the target for 3 s):

```css
#toast.htmx-settling { opacity: 100; }
#toast { background: #E1F0DA; opacity: 0; transition: opacity 3s ease-out; }
```

Why it works
- HTML checkboxes already hold their own state, so the table is not re-rendered; checked rows stay checked.
- Use `output` for a result tied to one form. For general messages not tied to a form, use an ARIA live region instead, e.g. `<p id="toast" aria-live="polite"></p>`.
- Encode the row key in the checkbox `name` (here `active:<email>`) so the server can split on `:`.

## Checked

2026-11-07. Confirmed on examples/bulk-update.md (markup, CSS, `output` versus ARIA live region note, form-managed state, the fake server's param format and activate/deactivate logic) and docs.md (swap and settle phases with the `htmx-settling` class).
Fixed: the server paragraph now states only what the example's server does. Removed the invented Verify step.
Method: documentation only; no commands were run.
