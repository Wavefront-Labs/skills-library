---
id: computing-software.web-development.htmx.htmx-confirm-and-prompt
name: htmx-confirm-and-prompt
category: computing-software
field: web-development
product: htmx
tags: [htmx, hx-confirm, hx-prompt, htmx-confirm, dialogs, issuerequest]
level: practitioner
status: docs-checked
description: "Gate requests behind confirm and prompt dialogs with hx-confirm, hx-prompt (HX-Prompt header) and custom async confirmation via the htmx:confirm event."
sources:
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/attributes/hx-confirm.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/attributes/hx-prompt.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/events.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/docs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: make users confirm destructive actions or supply a value before a request goes out.

`hx-confirm="message"` shows the browser's `window.confirm`; cancel stops the request. Inherited, so a wrapper `<div hx-confirm="Are you sure?">` covers its buttons; opt a child out with `hx-confirm="unset"`.
```html
<button hx-delete="/account" hx-confirm="Are you sure you wish to delete your account?">Delete</button>
```

`hx-prompt="message"` shows `window.prompt`; the answer is sent in the `HX-Prompt` request header. Inherited. The `htmx:prompt` event fires after the prompt is shown (`detail.prompt` holds the reply); cancelling that event means the request does not occur.
```html
<button hx-delete="/account" hx-prompt="Enter your account name to confirm deletion">Delete</button>
```

Custom dialogs via `htmx:confirm`: fired on every request trigger, not only elements with `hx-confirm`. Call `evt.preventDefault()` to hold the request, then later call `evt.detail.issueRequest(skipConfirmation=false)`; pass `true` to skip the built-in `window.confirm`.
```javascript
document.body.addEventListener('htmx:confirm', function(evt) {
  if (!evt.detail.target.hasAttribute('confirm-with-sweet-alert')) return;
  const question = evt.detail.target.getAttribute('confirm-with-sweet-alert');
  evt.preventDefault();
  swal({title: "Are you sure?", text: question || "Are you sure you want to continue?", icon: "warning", buttons: true})
    .then(ok => { if (ok) evt.detail.issueRequest(true); });
});
```
`evt.detail` has `elt`, `etc`, `issueRequest`, `path`, `target`, `triggeringEvent`, `verb`, and `question` (only if `hx-confirm` is present).

To reuse the `hx-confirm` text in a custom dialog, the confirm example page checks `evt.detail.question` and returns early when it is empty; the question exists only when `hx-confirm` is present.

## Checked

2026-11-07. Confirmed on hx-confirm.md (inherited, `window.confirm`, `issueRequest(skipConfirmation=false)`, `question`, `triggeringEvent`), hx-prompt.md (`HX-Prompt` header, inherited), events.md (`htmx:confirm` fires on every trigger and its detail fields; `htmx:prompt` detail and cancel behaviour), docs.md (`hx-confirm="unset"`, confirm event example) and examples/confirm.md.
Removed: the sweet-alert sample read `evt.detail.question` on an element that has no `hx-confirm`, which is undefined per events.md, so it now reads the custom attribute as the events page does; the invented Verify step.
Method: documentation only; no commands were run.
