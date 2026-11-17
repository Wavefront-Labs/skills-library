---
id: computing-software.web-development.frontend-development.url-and-urlsearchparams-state
name: url-and-urlsearchparams-state
category: computing-software
field: web-development
product: frontend-development
tags: [history-api, urlsearchparams, url-state, query-string, javascript]
level: practitioner
status: verified
description: "Keeping filter, sort and pagination state in the URL with URL and URLSearchParams: parsing, encoding, multi-value keys, replaceState updates and validation."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/URL
  - https://developer.mozilla.org/en-US/docs/Web/API/URLSearchParams
  - https://url.spec.whatwg.org/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# URL and URLSearchParams for query state

## 1. Why URL state
Shareable, bookmarkable, survives refresh, back button works. Put filters, sort, page, tab, search query in the URL; keep ephemeral UI (hover, open dropdown) out.

## 2. Read and write
```js
const url = new URL(location.href);
const p = url.searchParams;
const page = Math.max(1, Number.parseInt(p.get("page") ?? "1", 10) || 1);   // validate: URL input is untrusted
const tags = p.getAll("tag");                                                 // ?tag=a&tag=b
p.set("sort", "price"); p.delete("page"); p.append("tag", "sale");
history.replaceState(null, "", url);            // or pushState for "committed" navigations
```
- Build URLs with `new URL(path, base)` instead of string concatenation - handles encoding and relative paths.
- `new URLSearchParams({ q: "a&b", n: 2 }).toString()` -> `q=a%26b&n=2`. Spaces become `+`; `encodeURIComponent` uses `%20` - both decode fine with URLSearchParams.
- `p.sort()` for canonical ordering (cache keys, analytics).
- `URL.canParse(str)` (Chrome 120, Firefox 115, Safari 17 per MDN compat) to validate without try/catch (`canParse("x")` false, `canParse("https://a.b")` true); `URL.parse()` (Chrome/Firefox 126, Safari 18) returns null on failure.

## 3. Conventions
- Remove defaults from the URL (`page=1`, default sort) to keep URLs short and canonical.
- Arrays: repeated keys (`tag=a&tag=b`) are better supported by servers than `tag=a,b` or `tag[]=a`; agree with the backend.
- Debounce search-as-you-type URL updates (~300 ms) and use `replaceState`.
- Framework routers: Next.js `useSearchParams` + `router.replace`, React Router `useSearchParams`, Vue Router `route.query` - same principles; libraries like `nuqs` type-check params.

## 4. Pitfalls
- `p.get` returns `null` for missing, `""` for `?q=` - handle both (checked in Node 20; `p.sort()` turned `b=2&a=1&a=0` into `a=1&a=0&b=2`, a stable sort).
- `location.search` includes `?`; `URLSearchParams` tolerates it.
- Fragment (`#`) is never sent to the server - do not put server-needed state there.
- Never insert raw params into HTML (XSS) or redirects (open redirect).
- URL length: keep under ~2,000 characters for CDNs/proxies; large state belongs in storage with an id in the URL.

## Verify
Copy a filtered URL into a new window - identical results; malformed values (`page=abc`) fall back safely.
