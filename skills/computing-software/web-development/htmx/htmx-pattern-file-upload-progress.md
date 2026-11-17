---
id: computing-software.web-development.htmx.htmx-pattern-file-upload-progress
name: htmx-pattern-file-upload-progress
category: computing-software
field: web-development
product: htmx
tags: [htmx, file-upload, progress, hx-encoding, multipart, htmx-xhr-progress, hyperscript]
level: practitioner
status: docs-checked
description: "AJAX file upload with a progress bar in htmx: hx-encoding multipart/form-data, hx-post, and the htmx:xhr:progress event's loaded and total values."
sources:
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/examples/file-upload.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: submit a file through htmx and drive a `progress` element while it uploads.

Requirements
- The form must encode as multipart: set `hx-encoding='multipart/form-data'` on the form, as the example does.
- POST to the upload URL with `hx-post`.
- A `progress` element with `max='100'`.
- Listen for the `htmx:xhr:progress` event; its `detail` has `loaded` and `total` byte counts.

Plain JavaScript:

```html
<form id='form' hx-encoding='multipart/form-data' hx-post='/upload'>
  <input type='file' name='file'>
  <button>Upload</button>
  <progress id='progress' value='0' max='100'></progress>
</form>
<script>
  htmx.on('#form', 'htmx:xhr:progress', function(evt) {
    htmx.find('#progress').setAttribute('value', evt.detail.loaded/evt.detail.total * 100)
  });
</script>
```

Hyperscript variant, with the handler on the form itself (hyperscript destructures `loaded` and `total` out of the event detail):

```html
<form hx-encoding='multipart/form-data' hx-post='/upload'
      _='on htmx:xhr:progress(loaded, total) set #progress.value to (loaded/total)*100'>
  <input type='file' name='file'>
  <button>Upload</button>
  <progress id='progress' value='0' max='100'></progress>
</form>
```

Notes
- `htmx.on` and `htmx.find` are the htmx utility methods the pure-JavaScript example uses.
- The example attaches the listener to the form that issues the request.
- If the server returns validation errors and re-renders the form, keep the chosen file with htmx-pattern-form-state-after-swap.

## Checked

2026-11-07. Confirmed against the htmx file-upload example page (multipart encoding, `/upload` POST, `progress` element, `htmx:xhr:progress` with `loaded` and `total`, both code samples, hyperscript destructuring). Removed an unconfirmed claim that `hx-encoding` can sit on a different element and the invented Verify step.
Method: documentation only; no commands were run.
