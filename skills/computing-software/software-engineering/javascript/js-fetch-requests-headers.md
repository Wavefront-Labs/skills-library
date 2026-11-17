---
id: computing-software.software-engineering.javascript.js-fetch-requests-headers
name: js-fetch-requests-headers
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, fetch-post-json, js-fetch]
level: practitioner
status: docs-checked
description: "Send JSON and credentialed requests with fetch, set headers with the Headers object, and understand cors, same-origin and no-cors modes."
sources: ["https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch", "https://developer.mozilla.org/en-US/docs/Web/API/Request/credentials", "https://developer.mozilla.org/en-US/docs/Web/API/Headers"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fetch requests: POST, headers and credentials

- JSON: `fetch(url, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(data) })`; the `Content-Type` header tells the server the body format.
- A `Headers` object normalises names to lowercase, strips whitespace around values, and refuses forbidden request headers that the browser sets itself.
- `credentials` takes `omit`, `same-origin` (the default) or `include`. `include` sends cookies, TLS client certificates and auth headers cross-origin, and the server must reply with `Access-Control-Allow-Credentials` and an explicit `Access-Control-Allow-Origin` (not `*`). Including credentials cross-origin can expose a site to CSRF.
- `mode` is `cors` (default), `same-origin` or `no-cors`. With `cors`, a non-simple request sends a preflight first and the real request goes out only if the server answers with the right CORS headers.
- `mode: "no-cors"` limits methods to GET, HEAD and POST, restricts which headers you may set, and returns an opaque response whose headers and body JavaScript cannot read. MDN says most sites should not use it.

Self-check: DevTools Network shows the preflight and the final request with the expected headers.

## Checked

2026-11-03. Confirmed on MDN: Using Fetch (JSON POST, Headers normalisation, forbidden headers, mode values, preflight, no-cors restrictions and opaque response, credentials and CSRF warning, required CORS response headers), Request.credentials (values and same-origin default). Removed: `FormData` Content-Type note, the `Access-Control-Allow-Headers/Methods` wording (not on the pages read) and the SameSite/token CSRF advice.
Method: documentation only; no commands were run.
