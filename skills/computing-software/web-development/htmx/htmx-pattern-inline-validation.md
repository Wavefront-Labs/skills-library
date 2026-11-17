---
id: computing-software.web-development.htmx.htmx-pattern-inline-validation
name: htmx-pattern-inline-validation
category: computing-software
field: web-development
product: htmx
tags: [htmx, validation, forms, inline-validation, hx-post, hx-indicator]
level: practitioner
status: docs-checked
description: "Validate one form field on the server as the user edits it with htmx: the field's wrapper div swaps itself with a re-rendered group that carries an error class and message."
sources:
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/examples/inline-validation.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: server-side validation of one input (here an email) with the feedback shown beside the field, while the rest of the form is untouched.

Form. The wrapper div around the validated input targets itself and swaps outerHTML; the input posts its own value to a dedicated validation endpoint:

```html
<form hx-post="/contact">
  <div hx-target="this" hx-swap="outerHTML">
    <label>Email Address</label>
    <input name="email" hx-post="/contact/email" hx-indicator="#ind">
    <img id="ind" src="/img/bars.svg" alt="Checking..." class="htmx-indicator"/>
  </div>
  <input type="text" name="firstName">
  <button class="btn primary">Submit</button>
</form>
```

The input posts on its default event for inputs (the page calls it `changed`), so the check runs when the user tabs out of the field. `hx-indicator="#ind"` shows the spinner during the request.

The `POST /contact/email` response is the whole wrapper re-rendered with an `error` class and message, including the input with its current value and the same htmx attributes so it can validate again:

```html
<div hx-target="this" hx-swap="outerHTML" class="error">
  <label>Email Address</label>
  <input name="email" hx-post="/contact/email" hx-indicator="#ind" value="test@foo.com">
  <img id="ind" src="/img/bars.svg" alt="Checking..." class="htmx-indicator"/>
  <div class='error-message'>That email is already taken.  Please enter another email.</div>
</div>
```

Light styling:

```css
.error-message { color:red; }
.error input { box-shadow: 0 0 3px #CC0000; }
.valid input { box-shadow: 0 0 3px #36cc00; }
```

Return a wrapper with class `valid` (no message) on success; the page's CSS styles `.valid input`.

## Checked

2026-11-07. Confirmed against the htmx Inline Validation example page (form markup, `hx-target="this"`, `outerHTML`, `hx-post="/contact/email"`, `hx-indicator`, error partial, CSS, `valid`/`error` classes). Removed the unsourced security-boundary advice and the invented Verify step.
Method: documentation only; no commands were run.
