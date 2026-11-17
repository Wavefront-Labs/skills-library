---
id: computing-software.web-development.frontend-development.constraint-validation-api
name: constraint-validation-api
category: computing-software
field: web-development
product: frontend-development
tags: [html-forms, form-validation, constraint-validation-api, setcustomvalidity, validity-state, user-invalid, reportvalidity, novalidate, checkvalidity]
level: practitioner
status: docs-checked
description: "Native form validation done well: required/pattern/min, ValidityState, setCustomValidity, :user-invalid styling and replacing browser bubbles with accessible messages."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/HTML/Guides/Constraint_validation
  - https://developer.mozilla.org/en-US/docs/Web/API/ValidityState
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Selectors/:user-invalid
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Constraint Validation API

**Goal:** use the browser's validation engine for the rules, but control when and how errors are shown.

## 1. Declare the rules in HTML
`required`, `minlength`/`maxlength`, `min`/`max`/`step`, `pattern`, `type=email|url`. These populate `input.validity` (a `ValidityState`): `valueMissing`, `typeMismatch`, `patternMismatch`, `tooShort`, `tooLong`, `rangeUnderflow`, `rangeOverflow`, `stepMismatch`, `badInput`, `customError`, `valid`.

## 2. Take over the UI
```html
<form novalidate id="signup">
  <label for="pw">Password</label>
  <input id="pw" name="pw" type="password" required minlength="12" aria-describedby="pw-err">
  <p id="pw-err" class="error" hidden></p>
</form>
```
```js
const form = document.getElementById('signup');
form.addEventListener('submit', (e) => {
  let firstBad = null;
  for (const el of form.elements) {
    if (!el.willValidate) continue;
    const msg = el.validity.valid ? '' : messageFor(el);
    const out = document.getElementById(el.getAttribute('aria-describedby'));
    if (out) { out.textContent = msg; out.hidden = !msg; }
    el.setAttribute('aria-invalid', String(!el.validity.valid));
    if (!el.validity.valid && !firstBad) firstBad = el;
  }
  if (firstBad) { e.preventDefault(); firstBad.focus(); }
});
function messageFor(el) {
  if (el.validity.valueMissing) return `Enter your ${el.labels[0].textContent.toLowerCase()}`;
  if (el.validity.tooShort) return `Use at least ${el.minLength} characters`;
  return el.validationMessage; // browser's localised fallback
}
```
`novalidate` on the form turns off interactive validation but `validity` still works; `checkValidity()` returns a boolean, `reportValidity()` shows native bubbles.

## 3. Cross-field and async rules: `setCustomValidity`
```js
confirm.addEventListener('input', () => {
  confirm.setCustomValidity(confirm.value === pw.value ? '' : 'Passwords do not match');
});
```
Any non-empty string makes the field invalid **until you set `''` again** - forgetting to clear it is the classic "form never submits" bug.

## 4. Styling at the right time
`:invalid` matches immediately on page load (empty required fields show red). Use `:user-invalid` (matches only after the user has interacted/submitted), supported since Chrome 119, Firefox 88 and Safari 16.5; for older browsers fall back to a `.touched` class set on `blur` for older browsers.

## 5. Rules
- Client validation is UX only; validate again on the server.
- Validate on blur / submit, not every keystroke (except clearing an error once fixed).
- Messages say how to fix, are in text next to the field and linked with `aria-describedby`.

## Verify
- [ ] Submitting empty form focuses the first invalid field and announces its message in a screen reader.
- [ ] No red borders on initial load.
- [ ] Fixing a cross-field error lets the form submit (custom validity cleared).
- [ ] Server rejects the same bad input with JS disabled.

## Checked
2026-10-26. MDN constraint validation guide, ValidityState page, :user-invalid page and browser-compat-data (main, 2026-10-26): confirmed the ValidityState flags used (valueMissing, typeMismatch, patternMismatch, tooShort, tooLong, rangeUnderflow, rangeOverflow, stepMismatch, badInput, customError), checkValidity versus reportValidity, that novalidate disables interactive validation, that setCustomValidity with an empty string means valid, and :user-invalid support versions.
Method: documentation only; no commands were run.
