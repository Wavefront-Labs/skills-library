---
id: computing-software.web-development.node-express.cache-control-for-sensitive-responses
name: cache-control-for-sensitive-responses
category: computing-software
field: web-development
product: node-express
tags: [no-store-sensitive, cache-control, web-cache-deception, private-cache, logout-caching, security]
level: practitioner
status: verified
description: "Keeping personal data out of caches: no-store vs private, CDN caching of authenticated responses, web cache deception, logout and back-button exposure, framework helpers."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cache-Control
  - https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html#cache-control
  - https://portswigger.net/web-security/web-cache-deception
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cache-Control for sensitive responses

## 1. Pick the directive
| Directive | Meaning | Use |
|---|---|---|
| `no-store` | nobody stores it (browser disk, proxies, CDN) | account pages, API responses with personal data, tokens |
| `private` | browser may store, shared caches must not | per-user but non-sensitive (preferences UI) |
| `no-cache` | may store, must revalidate every time | HTML shells you want fresh |
| `public, max-age=...` | anyone may cache | static, anonymous content only |
```js
app.use("/account", (req, res, next) => { res.set("Cache-Control", "no-store"); next(); });
```
Framework helpers: Django `@never_cache` (ran on Django 6.1: `max-age=0, no-cache, no-store, must-revalidate, private` plus an `Expires` header), Rails `response.headers["Cache-Control"] = "no-store"` (set the header directly; Rails' cache-control parser only exposes a `no_store?` reader). Check what your Next.js version sends for dynamic routes with `curl -I`; do not assume it.

## 2. CDN leaks
- A CDN rule "cache everything" or a path-based rule can cache an authenticated response and serve user A's page to user B. Default CDNs to respect origin headers; never cache responses that set cookies or have `Authorization`.
- **Web cache deception**: `/account/settings/x.css` hits the account handler (framework ignores the suffix) but the CDN caches it because of `.css`. Defences: return 404 for unexpected path suffixes, cache by `Content-Type` not extension, `no-store` on authenticated responses wins.
- Cache keys must include anything that varies the response (`Vary: Cookie` is usually uncacheable; better not to cache).

## 3. Logout and shared computers
- Browser history/back button can redisplay cached account pages after logout; `no-store` prevents disk storage.
- Send `Clear-Site-Data: "cache", "storage"` (quotes required; MDN: Baseline widely available since September 2023; `storage` clears localStorage, sessionStorage, IndexedDB and service worker registrations) on the logout response for high-sensitivity apps (also wipes local data; test the cost).
- Service workers caching API responses must exclude personal endpoints or clear caches on logout.

## 4. Also
`Pragma: no-cache` and `Expires: 0` only matter for HTTP/1.0-era caches; harmless to add for legacy proxies.

## Verify
- [ ] `curl -sI https://site/account` (with session cookie) shows `Cache-Control: no-store`; CDN logs show MISS/BYPASS for authenticated paths.
- [ ] Requesting `/account/foo.css` returns 404 or uncacheable headers.
