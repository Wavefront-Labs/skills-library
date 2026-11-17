---
id: computing-software.software-engineering.javascript.js-url-urlsearchparams-formdata-blob
name: js-url-urlsearchparams-formdata-blob
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, js-url-api, urlsearchparams, formdata, blob, file-api]
level: practitioner
status: docs-checked
description: "Parse and build URLs with URL and URLSearchParams, collect form fields with FormData, and read Blob and File data with the promise methods."
sources: ["https://developer.mozilla.org/en-US/docs/Web/API/URL", "https://developer.mozilla.org/en-US/docs/Web/API/URL/URL", "https://developer.mozilla.org/en-US/docs/Web/API/URL/canParse_static", "https://developer.mozilla.org/en-US/docs/Web/API/URLSearchParams", "https://developer.mozilla.org/en-US/docs/Web/API/FormData", "https://developer.mozilla.org/en-US/docs/Web/API/Blob", "https://developer.mozilla.org/en-US/docs/Web/API/File"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# URL, FormData, Blob

- `new URL(url, base)` throws a `TypeError` when the URL (or base plus url) is not valid; `URL.canParse(url, base)` returns a boolean instead (feature-detect with `"canParse" in URL`).
- `URLSearchParams` has `get`, `getAll` (repeated keys), `append`, `set`, `delete`, `toString`, and is iterable with `for...of`. Pass unencoded keys and values to `append()`; it percent-encodes on serialisation and encodes a space as `+`. Never build one from interpolated strings: the constructor reads `+` as a space, so base64 data gets corrupted.
- `url.searchParams` updates `url.search`, but `URL.search` encodes spaces as `%20` while `URLSearchParams` uses `+`, so touching `searchParams` can re-serialise the URL differently.
- `new FormData(formEl)` fills itself from the form's named controls (and encodes file input content); it matches the `multipart/form-data` format and works directly with `fetch()`. It is iterable with `for...of`; `getAll(key)` returns every value for a key.
- `Blob` is immutable raw data with a `type` (MIME type, empty if unknown) and `size`; read it with `text()`, `arrayBuffer()` or `stream()`, and cut part of it with `slice()`. `File` is a kind of Blob that adds `name` and `lastModified`.
- `FileReader` is the older asynchronous reader for File and Blob objects.
- Never trust `file.type` or the name for security; validate on the server.

## Checked

2026-11-03. Confirmed on MDN: URL and URL() constructor (TypeError, base handling, origin, protocol), URL.canParse, URLSearchParams (methods, iteration, percent-encoding, `+` for space, constructor `+` pitfall, searchParams vs search encoding), FormData and its constructor, Blob (immutable, type, slice/text/arrayBuffer/stream), File (extends Blob, name, lastModified), FileReader. Removed: `Object.fromEntries(fd)` note, `encodeURIComponent`/`encodeURI` advice, the download-link recipe (see js-file-api-blob-urls), the "prefer promise methods" opinion, and the ECMAScript and MDN JavaScript root sources.
Method: documentation only; no commands were run.
