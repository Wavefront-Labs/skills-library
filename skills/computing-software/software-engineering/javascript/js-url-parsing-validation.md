---
id: computing-software.software-engineering.javascript.js-url-parsing-validation
name: js-url-parsing-validation
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, url-canparse, js-url-blob]
level: practitioner
status: docs-checked
description: "Parse and build URLs with the URL class, check with URL.canParse, and validate redirect targets by origin and protocol."
sources: ["https://developer.mozilla.org/en-US/docs/Web/API/URL", "https://developer.mozilla.org/en-US/docs/Web/API/URL/URL", "https://developer.mozilla.org/en-US/docs/Web/API/URL/canParse_static", "https://developer.mozilla.org/en-US/docs/Web/API/URLSearchParams"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# URL parsing and validation

- `new URL(input, base)` throws `TypeError` when the input (or base plus input) is not a valid URL. A relative input with no base is invalid. `URL.canParse(input, base)` returns a boolean instead of throwing and is Baseline, though MDN shows feature detection with `"canParse" in URL`.
- With a base, the result is not a concatenation: relative references resolve against the base's directory, and root-relative ones against the base origin.
- Build queries with `url.searchParams.set/append`, which take unencoded values and encode them when serialising; avoid interpolating raw strings into a query.
- `url.origin` is scheme, domain and port; `url.protocol` is the scheme including the final `:`. For redirect targets, parse against your own origin as the base, then allow only an `origin` you expect, and reject any protocol other than `https:` (or `http:`) such as `javascript:` or `data:`.
- `URLSearchParams.getAll(key)` returns every value of a repeated key.

Self-check: `URL.canParse("/en-US/docs")` is false, and `URL.canParse("/en-US/docs", "https://example.com")` is true.

## Checked

2026-11-03. Confirmed on MDN: URL, URL() constructor (TypeError, base resolution rules, the relative-without-base example), URL.canParse, URLSearchParams (getAll, append, encoding), URL origin and protocol properties. The allowlist advice is the skill's own security guidance, not documented behaviour. Removed: the scheme-relative `//host` self-check, the `encodeURIComponent`/`encodeURI` and percent-encoded `pathname` claims, which no page read states, and the placeholder host `app.test`.
Method: documentation only; no commands were run.
