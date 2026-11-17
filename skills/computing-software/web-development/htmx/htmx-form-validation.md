---
id: computing-software.web-development.htmx.htmx-form-validation
name: htmx-form-validation
category: computing-software
field: web-development
product: htmx
tags: [htmx, validation, hx-validate, reportvalidity, setcustomvalidity, constraint-validation]
level: practitioner
status: docs-checked
description: "Client-side validation in htmx: HTML5 Constraint Validation before requests, hx-validate for non-forms, reportValidityOfForms and custom validation events."
sources:
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/docs.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/attributes/hx-validate.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/events.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: block invalid requests in the browser and add custom rules.

Behaviour: htmx integrates with the HTML5 Validation API and will not issue a request for a form if a validatable input is invalid; also applies to WebSocket sends. Standard attributes (`required`, `type="email"`, `pattern`, ...) just work.

Non-form elements do not validate by default. Add `hx-validate="true"` to an `<input>`, `<textarea>` or `<select>` that issues its own request. `hx-validate` is not inherited.

User feedback: normal browser submission shows errors and focuses the first invalid field, but for backwards compatibility htmx does not. Set `htmx.config.reportValidityOfForms = true` to restore the native behaviour (docs recommend enabling it). Note the config text in the source says htmx 4 validates forms by default.

Events (all carry `detail.elt`):
- `htmx:validation:validate` - fired before `checkValidity()`; use it with `setCustomValidity()` for custom rules.
- `htmx:validation:failed` - an element failed; `detail.message`, `detail.validity`. `preventDefault()` prevents the `reportValidity()` call.
- `htmx:validation:halted` - request not sent; `detail.errors` is an array of error objects with the invalid elements and the errors associated with them.

Example (require the value "foo"):
```html
<form id="example-form" hx-post="/test">
  <input name="example"
         onkeyup="this.setCustomValidity('')"
         hx-on:htmx:validation:validate="if(this.value != 'foo') {
             this.setCustomValidity('Please enter the value foo')
             htmx.find('#example-form').reportValidity() }">
</form>
```
Remember: client validation can be bypassed, so re-validate on the server (and return 422 with a rendered form; see `htmx-response-status-handling`).

## Checked

2026-11-07. Confirmed on docs.md (Validation section, the `reportValidityOfForms` default and htmx 4 note, example, 422 response-handling example), hx-validate.md (non-form elements, not inherited) and events.md (the three `htmx:validation:*` events, their detail fields and the `preventDefault()` rule on `failed`).
Fixed: `detail.errors` wording now matches events.md. Removed the invented Verify step.
Method: documentation only; no commands were run.
