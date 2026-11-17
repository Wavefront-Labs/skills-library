---
id: computing-software.web-development.frontend-development.formdata-submission-and-progressive-enhancement
name: formdata-submission-and-progressive-enhancement
category: computing-software
field: web-development
product: frontend-development
tags: [html-forms, formdata, form-submission, progressive-enhancement, fetch-api, requestsubmit, submitter, post-redirect-get]
level: practitioner
status: docs-checked
description: "Submitting forms with FormData and fetch while keeping a working no-JS POST, handling submitter buttons, double-submits and the post/redirect/get pattern."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/FormData
  - https://developer.mozilla.org/en-US/docs/Web/API/HTMLFormElement/requestSubmit
  - https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Type
  - https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status/303
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# FormData submission and progressive enhancement

**Goal:** a form that works as a plain HTML POST, upgraded with JavaScript for inline feedback without losing that baseline.

## 1. Baseline first
```html
<form method="post" action="/comments">
  <textarea name="body" required></textarea>
  <button name="intent" value="publish">Publish</button>
  <button name="intent" value="draft">Save draft</button>
</form>
```
Server: validate, then send a **303 See Other** redirect to a GET page (post/redirect/get): the redirected request always uses GET, so a refresh does not resubmit. On validation failure re-render the form with values and errors (422 Unprocessable Content is one option).

## 2. Enhance with fetch
```js
form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const fd = new FormData(form, e.submitter);   // includes the clicked button's name=value
  const btn = e.submitter; btn.disabled = true;
  try {
    const res = await fetch(form.action, { method: 'POST', body: fd, headers: { Accept: 'application/json' } });
    if (!res.ok) return showErrors(await res.json());
    form.reset();
  } finally { btn.disabled = false; }
});
```
- `new FormData(form, submitter)` (second arg) includes which button was pressed; older code loses `intent`.
- Pass `FormData` directly as the body: the browser sends `multipart/form-data` and generates the required `boundary`. **Do not set `Content-Type` yourself** or the boundary will be missing.
- For urlencoded: `new URLSearchParams(fd)`. For JSON: `Object.fromEntries(fd)` (loses repeated keys - use `fd.getAll('tag')`).
- Only successful controls (with a `name`, not disabled) are included, and an unchecked checkbox sends neither name nor value; use `readonly` if the value must submit.

## 3. Submitting programmatically
`form.requestSubmit(submitter?)` runs validation and fires `submit`, and includes the submitter's `name`/`value`; `form.submit()` raises no `submit` event and skips constraint validation - avoid it.

## 4. Double-submit and server negotiation
Disable the submitter during the request (re-enable in `finally`) and make the server endpoint idempotent where it matters. Have the server return JSON when `Accept: application/json` and redirect/HTML otherwise.

## Verify
- [ ] Disable JavaScript: form still submits, errors re-render, refresh after success doesn't repost.
- [ ] Network panel shows multipart body with correct boundary, and the `intent` value.
- [ ] Double-clicking submit sends one request.

## Checked

Checked 2026-10-26 against mdn/content (main) FormData, FormData() constructor, HTMLFormElement.requestSubmit and submit, URLSearchParams(), Content-Type header, HTTP 303 and 422 pages, input type=checkbox, and mdn/browser-compat-data.

- Confirmed: the `FormData(form, submitter)` constructor argument (Chrome 112, Firefox 111, Safari 16.4); only controls with a name and not disabled are included; an unchecked checkbox sends nothing; `URLSearchParams` accepts a `FormData`; `submit()` skips the `submit` event and validation, `requestSubmit()` validates and includes the submitter's data; multipart bodies need a `boundary`; 303 always redirects with GET; 422 is named Unprocessable Content.
- Changed: the 422 status is now offered as an option rather than a rule.

Method: documentation only; no commands were run.
