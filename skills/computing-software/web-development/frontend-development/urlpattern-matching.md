---
id: computing-software.web-development.frontend-development.urlpattern-matching
name: urlpattern-matching
category: computing-software
field: web-development
product: frontend-development
tags: [urlpattern, url-routing, url-state, client-routing, javascript]
level: practitioner
status: docs-checked
description: "Matching and parsing URLs with the URLPattern API: pattern syntax, named groups, wildcards, use in routers and service workers, and a polyfill for older engines."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/URLPattern
  - https://developer.mozilla.org/en-US/docs/Web/API/URLPattern/URLPattern
  - https://github.com/mdn/browser-compat-data
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# URL pattern matching with URLPattern

`URLPattern` uses a path-to-regexp-style syntax. Per mdn/browser-compat-data it is in Chrome 95, Firefox 142 and Safari 26; check support or add a polyfill for older engines.

## 1. Syntax
```js
const p = new URLPattern({ pathname: "/users/:id(\\d+)/posts/:slug?" });
p.test("https://x.dev/users/42/posts");              // true (slug optional)
p.exec("https://x.dev/users/42/posts/hello").pathname.groups; // { id: "42", slug: "hello" }

new URLPattern("/files/*", "https://x.dev");         // wildcard -> groups[0]
new URLPattern({ pathname: "/docs/:lang(en|fr)/:rest*" });
```
- Each component (protocol, hostname, pathname, search, hash) is matched separately; omitted ones default to `*`.
- Regex groups need double escaping inside JS strings (`"\\d+"`).
- Pass `{ ignoreCase: true }` as the options argument for case-insensitive matching.
- Query strings: match the pathname with URLPattern and read parameters with `URLSearchParams`.

## 2. A tiny router
```js
const routes = [
  [new URLPattern({ pathname: "/" }), Home],
  [new URLPattern({ pathname: "/products/:id" }), Product],
];
function resolve(url) {
  for (const [pattern, view] of routes) {
    const m = pattern.exec(url);
    if (m) return view({ ...m.pathname.groups, query: new URL(url).searchParams });
  }
  return NotFound();
}
navigation.addEventListener("navigate", e => { if (e.canIntercept) e.intercept({ handler: () => render(resolve(e.destination.url)) }); });
```

## 3. Service worker routing
```js
const api = new URLPattern({ pathname: "/api/*" });
self.addEventListener("fetch", e => { if (api.test(e.request.url)) e.respondWith(networkFirst(e.request)); });
```

## 4. URL-held state
Keep shareable state (filters, tab, page) in the path or query so reload/back/share work; parse with URLPattern + URLSearchParams, write with `history.replaceState` for frequent changes and `pushState` for navigations the user expects Back to undo.

## Verify
- [ ] Route table covered by tests including trailing slash, encoded characters (`%20`) and optional segments; polyfill loaded only when `!("URLPattern" in globalThis)`.

## Checked

2026-10-26. MDN URLPattern and its constructor (omitted components become `*` wildcards; `ignoreCase` option) and browser-compat-data (Chrome 95, Firefox 142, Safari 26). Removed the unconfirmed Speculation Rules and static routing mentions, the search-matching comment and polyfill name. The Navigation API router example is covered by its own skill.

Method: documentation only; no commands were run.
