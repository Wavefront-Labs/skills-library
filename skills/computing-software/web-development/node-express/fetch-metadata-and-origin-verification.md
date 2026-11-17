---
id: computing-software.web-development.node-express.fetch-metadata-and-origin-verification
name: fetch-metadata-and-origin-verification
category: computing-software
field: web-development
product: node-express
tags: [csrf, fetch-metadata, origin-check, sec-fetch-site, resource-isolation, security, origin-header-check]
level: practitioner
status: docs-checked
description: "Blocking cross-site requests server-side with Sec-Fetch-Site and Origin header checks: a resource isolation policy, allowed exceptions, and fallbacks for older clients."
sources:
  - https://web.dev/articles/fetch-metadata
  - https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Sec-Fetch-Site
  - https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html#fetch-metadata-headers
  - https://pkg.go.dev/net/http#CrossOriginProtection
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Fetch Metadata and Origin verification

Browsers attach headers the page cannot forge: `Sec-Fetch-Site` (`same-origin`, `same-site`, `cross-site`, `none`), `Sec-Fetch-Mode`, `Sec-Fetch-Dest`, and `Origin` on POST/CORS requests. Checking them is a token-free CSRF defence (Go 1.25's `http.CrossOriginProtection` implements it).

## 1. Resource isolation policy (Express)
```js
const ALLOWED_ORIGINS = new Set(["https://app.example.com"]);
app.use((req, res, next) => {
  if (["GET", "HEAD", "OPTIONS"].includes(req.method)) return next();
  const site = req.get("sec-fetch-site");
  if (site) {
    if (site === "same-origin" || site === "none") return next();       // none = typed URL/bookmark
    return res.status(403).send("cross-site request blocked");
  }
  const origin = req.get("origin");                                      // older browsers
  if (!origin) return next();                                            // only safe for non-browser clients; OWASP: otherwise reject unless a CSRF token or other defence succeeds
  if (ALLOWED_ORIGINS.has(origin)) return next();
  return res.status(403).send("bad origin");
});
```
- Decide whether `same-site` (sibling subdomains) is acceptable; default to rejecting.
- Exempt endpoints that are intentionally cross-site (OAuth callbacks receiving form POSTs, payment webhooks, public APIs) by path - and authenticate those differently (signatures).

## 2. Origin checks
- Compare the full origin (`scheme://host:port`), exact match against an allowlist - never `startsWith`/`includes` (`https://app.example.com.evil.net`).
- Cross-origin redirects can produce `Origin: null`; OWASP says `Origin: null` is not evidence of a same-origin request, so treat it as untrusted.
- Behind proxies, compare to the configured public origin, not `req.get("host")` which may be internal.

## 3. Coverage
`Sec-Fetch-*` has been supported in all major browsers since March 2023 (Safari 16.4+); OWASP makes a fallback to Origin/Referer verification mandatory for any Fetch Metadata implementation. Pair with SameSite cookies; keep tokens if you must support very old clients or have GET handlers with side effects (fix those).

## Verify
`curl -X POST -H "Sec-Fetch-Site: cross-site" ...` -> 403; app traffic unaffected (log-only mode first: log decisions for a week before enforcing).

## Checked

2026-10-25 against OWASP Cheat Sheet Series (OWASP/CheatSheetSeries, commit of 2026-10-24) and the Go 1.25 net/http documentation it links. Confirmed: Sec-Fetch-Site values same-origin, same-site, cross-site and none; Go 1.25 http.CrossOriginProtection is a Fetch Metadata based CSRF defence; Sec-Fetch-* is supported in all major browsers since March 2023 (Safari 16.4+) and an Origin/Referer fallback is mandatory; Origin: null can come from cross-origin redirects and is not evidence of same-origin; exact-origin matching rather than prefix matching.

Method: documentation only; no commands were run.
