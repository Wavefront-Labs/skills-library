---
id: computing-software.software-engineering.javascript.js-file-api-blob-urls
name: js-file-api-blob-urls
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, createobjecturl, js-url-blob]
level: practitioner
status: docs-checked
description: "Read File and Blob data, create and revoke object URLs, and build Blobs without leaking memory."
sources: ["https://developer.mozilla.org/en-US/docs/Web/API/URL/createObjectURL_static", "https://developer.mozilla.org/en-US/docs/Web/API/URL/revokeObjectURL_static", "https://developer.mozilla.org/en-US/docs/Web/API/Blob", "https://developer.mozilla.org/en-US/docs/Web/API/File", "https://developer.mozilla.org/en-US/docs/Web/API/FileReader"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# File, Blob and object URLs

- A `File` is a specific kind of `Blob` (adding `name` and `lastModified`) and works anywhere a Blob does. Read with `text()`, `arrayBuffer()` or `stream()`; `FileReader` is the older asynchronous reader for File and Blob objects.
- `const url = URL.createObjectURL(blob)` returns a URL for the object, usable as an `<img>` `src`. Release it with `URL.revokeObjectURL(url)` when done; revoking an invalid or already revoked URL does nothing. `createObjectURL` is not available in Service Workers because of the memory-leak risk.
- Build data with `new Blob([data], { type: "text/csv" })`; `blob.slice()` creates a Blob with a subset of the data (for example for chunked upload).
- `Blob.type` is the MIME type string, empty when unknown. Do not rely on client-side type or size checks alone; validate on the server too.

Self-check: revoke each preview URL and confirm the old URL no longer loads.

## Checked

2026-11-03. Confirmed on MDN: URL.createObjectURL (release with revokeObjectURL, not in Service Workers), URL.revokeObjectURL (no-op on invalid or revoked URLs), Blob (immutable, type, slice/text/arrayBuffer/stream), File (a kind of Blob, name, lastModified), FileReader. Removed: `<a download>` download recipe, drag-and-drop `dataTransfer.files` and `dragover` advice, `input.files[0]`, the Memory-panel check, and the sentence that `file.type` is user-controlled (reworded as validate on the server).
Method: documentation only; no commands were run.
