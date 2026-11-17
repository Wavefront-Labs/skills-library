---
id: computing-software.web-development.node-express.cors-origin-allowlist-and-vary
name: cors-origin-allowlist-and-vary
category: computing-software
field: web-development
product: node-express
tags: [cors, cors-origin-allowlist, vary-origin, origin-reflection, security, caching]
level: practitioner
status: verified
description: "Building a safe CORS origin allowlist: exact matching instead of reflection or regex mistakes, null origin, Vary Origin for caches, and per-environment configuration."
sources:
  - https://portswigger.net/web-security/cors
  - https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Vary
  - https://cheatsheetseries.owasp.org/cheatsheets/HTML5_Security_Cheat_Sheet.html#cross-origin-resource-sharing
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CORS origin allowlists and the reflection vulnerability

## 1. The vulnerability
```js
res.set("Access-Control-Allow-Origin", req.get("origin"));   // reflects ANY origin
res.set("Access-Control-Allow-Credentials", "true");
```
Any website a logged-in user visits can read their API data. Common causes: copying "fix CORS" snippets, `cors({ origin: true, credentials: true })`, broken regexes.

## 2. Exact allowlist
```js
const ALLOWED = new Set((process.env.CORS_ORIGINS ?? "").split(",").filter(Boolean));
// e.g. "https://app.example.com,https://admin.example.com"
app.use(cors({
  origin(origin, cb) {
    if (!origin) return cb(null, false);                 // no Origin: not a CORS request; no ACAO header
    cb(null, ALLOWED.has(origin));                       // true -> echoes the origin; false -> no header
  },
  credentials: true,
}));
```
- Compare full origins exactly. Regex bugs seen in the wild: `/example\.com$/` matches `evilexample.com`; unescaped dot `/app.example.com/` matches `appXexample.com`; `startsWith("https://app.example.com")` matches `https://app.example.com.evil.io`.
- If you need subdomain wildcards: `new URL(origin)` then `url.protocol === "https:" && (url.hostname === "example.com" || url.hostname.endsWith(".example.com"))` - and remember any XSS on any subdomain then reads your API.
- Never allow `null` (sandboxed iframes and `file:` produce it - attackers can too).
- Do not allow `http://` origins in production.

## 3. Vary: Origin
When the ACAO value depends on the request origin, send `Vary: Origin` on **every** response (including those without ACAO), or a CDN/browser cache may serve origin A's response (with A's ACAO) to origin B or serve a header-less cached copy. The `cors` package (2.8.6) adds it when the origin is allowed or when `origin` is an array, but with an `origin(origin, cb)` function that answers `false` the denied response carries no `Vary` header at all (tested). Add `app.use((req, res, next) => { res.vary("Origin"); next(); })` before `cors()` so denied responses are keyed by origin too.

## 4. Public resources
Truly public, uncredentialed data (fonts, open APIs) can use `Access-Control-Allow-Origin: *` - safe precisely because credentials are not allowed with `*`.

## Verify
`curl -s -I -H "Origin: https://evil.example" https://api.example.com/me | grep -i access-control` returns nothing; allowed origin returns its exact value plus `Vary: Origin`. Burp Scanner/ZAP CORS checks pass.
