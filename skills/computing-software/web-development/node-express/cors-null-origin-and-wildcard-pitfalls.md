---
id: computing-software.web-development.node-express.cors-null-origin-and-wildcard-pitfalls
name: cors-null-origin-and-wildcard-pitfalls
category: computing-software
field: web-development
product: node-express
tags: [cors-null-origin, cors-misconfiguration, origin-reflection, cors-regex, cors, security]
level: practitioner
status: verified
description: "CORS misconfigurations that leak data: trusting Origin null, reflecting any origin with credentials, broken regex and suffix checks, wildcard misuse and subdomain trust."
sources:
  - https://portswigger.net/web-security/cors
  - https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS
  - https://cheatsheetseries.owasp.org/cheatsheets/HTML5_Security_Cheat_Sheet.html#cross-origin-resource-sharing
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CORS null origin and wildcard pitfalls

CORS only matters for responses that carry user-specific data or require credentials. The bugs below let an attacker's page read those responses.

## 1. Origin: null
Browsers send `Origin: null` from sandboxed iframes (without `allow-same-origin`), `file:` and `data:` documents and cross-origin redirects (MDN lists more cases; a sandboxed iframe sending `Origin: null` was reproduced in Chromium 156). An attacker can produce it trivially:
```html
<iframe sandbox="allow-scripts" srcdoc="<script>fetch('https://api.example.com/me',{credentials:'include'}).then(r=>r.text()).then(leak)</script>"></iframe>
```
Never allowlist `"null"`, even "for local development".

## 2. Reflecting any origin
```js
res.set("Access-Control-Allow-Origin", req.headers.origin);   // with Allow-Credentials: true = any site reads user data
```
Use an explicit allowlist and exact comparison.

## 3. Broken matching
| Check | Bypass |
|---|---|
| `origin.endsWith("example.com")` | `https://evilexample.com` |
| `/https:\/\/.*example.com/` | `https://example.com.evil.net`, `https://exampleXcom.evil` (unescaped dot) |
| `origin.includes("example.com")` | `https://example.com.evil.net` |
| `startsWith("https://example.com")` | `https://example.com.evil.net` |
Correct:
```js
const ALLOWED = new Set(["https://app.example.com", "https://admin.example.com"]);
const ok = ALLOWED.has(req.headers.origin);
// or parse: const { protocol, hostname } = new URL(origin); protocol === "https:" && (hostname === "example.com" || hostname.endsWith(".example.com"))
```

## 4. Wildcards
- `Access-Control-Allow-Origin: *` is fine for public, cookie-less data (fonts, public APIs). Browsers refuse `*` together with credentials, which is why people "fix" it by reflecting origins (worse).
- Trusting all subdomains means one XSS or subdomain takeover on `anything.example.com` reads your API. Keep the list tight; monitor dangling DNS.

## 5. Also
- Send `Vary: Origin` whenever the allow-origin value depends on the request.
- `Access-Control-Allow-Headers`/`-Methods` reflection is less dangerous but keep it explicit.
- Intranet APIs relying on "only internal sites can call this" are readable by any public page a staff member visits if they reflect origins.

## Verify
- [ ] `curl -H "Origin: null" -I` and `-H "Origin: https://example.com.evil.net"` return no `Access-Control-Allow-Origin`.
