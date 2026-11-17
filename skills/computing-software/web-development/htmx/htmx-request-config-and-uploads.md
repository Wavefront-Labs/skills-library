---
id: computing-software.web-development.htmx.htmx-request-config-and-uploads
name: htmx-request-config-and-uploads
category: computing-software
field: web-development
product: htmx
tags: [htmx, hx-encoding, hx-request, file-upload, multipart, timeout, credentials]
level: practitioner
status: docs-checked
description: "Per-request settings: hx-encoding multipart file uploads with progress events, and hx-request timeout, credentials, noHeaders."
sources:
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/attributes/hx-encoding.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/attributes/hx-request.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/docs.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/events.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: upload files and tweak individual request behaviour.

File upload: set `hx-encoding="multipart/form-data"` (the page says that is the value to use; the usual encoding is `application/x-www-form-urlencoded`). htmx then submits a `FormData` object that includes the file; depending on your server-side technology you may have to handle such bodies very differently. The attribute is inherited, so it can sit on a parent.
```html
<form hx-post="/upload" hx-encoding="multipart/form-data">
  <input type="file" name="file"><button>Upload</button>
</form>
```
Progress: htmx fires `htmx:xhr:progress` periodically during upload (based on the standard `progress` event), plus `htmx:xhr:loadstart`, `htmx:xhr:loadend` and `htmx:xhr:abort`; hook the progress event to drive a progress bar (all have `detail.elt`).

`hx-request` - JSON-like object with:
- `timeout` - the timeout for the request, in milliseconds (the global `htmx.config.timeout` defaults to 0).
- `credentials` - whether the request will send credentials (the related global `htmx.config.withCredentials` defaults to `false`).
- `noHeaders` - strips all headers from the request.
```html
<div hx-get="/slow" hx-request='{"timeout":100}'>...</div>
<div hx-get="/x" hx-request='js: timeout:getTimeoutSetting() '>...</div>
```
The `js:` / `javascript:` prefix makes values dynamically evaluated. `hx-request` is merge-inherited: child values merge with parents.

A timeout fires `htmx:timeout` (wraps the XHR `timeout` event; `detail.xhr`, `detail.elt`).

## Checked

2026-11-07. Confirmed against the hx-encoding and hx-request references, the docs File Upload section and config table (`htmx.config.timeout`, `htmx.config.withCredentials`), and the events page (`htmx:xhr:*`, `htmx:timeout` details). Softened the "only documented value", "0 = none" and "server must parse multipart" wording to what the pages say and removed the invented Verify step.
Method: documentation only; no commands were run.
