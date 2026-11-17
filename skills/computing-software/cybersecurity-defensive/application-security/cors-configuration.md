---
id: computing-software.cybersecurity-defensive.application-security.cors-configuration
name: cors-configuration
category: computing-software
field: cybersecurity-defensive
product: application-security
tags: [security-headers, cors-configuration, cors, access-control-allow-origin, preflight, credentialed-requests]
level: practitioner
status: docs-checked
description: "Configure CORS correctly: explicit origin allow-lists, no reflected origins with credentials, Vary Origin, scoped methods and headers, and tests for misconfiguration."
sources: ["https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CORS configuration

**Goal:** only the browser origins you trust can read responses from your API, especially with cookies.

## Rules
- CORS relaxes the same-origin policy; it never protects the server. No CORS headers = most restrictive.
- Allow-list exact origins: compare the `Origin` header to a set like `{"https://app.example.com"}`.
- With `Access-Control-Allow-Credentials: true` you must echo a specific origin; `*` is rejected by browsers.
  Echoing whatever `Origin` arrives (reflection) with credentials lets any site read authenticated data.
- Always send `Vary: Origin` when the response depends on Origin, or caches serve the wrong header.
- Never allow the `null` origin (MDN notes the Origin value can be `null`).
- Restrict `Access-Control-Allow-Methods` and `-Headers` to what is used; set `Access-Control-Max-Age` for preflight caching.

## Common bugs
- Regex `^https://.*example.com$` matches `https://evilexample.com`; anchor and escape: `^https://([a-z0-9-]+\.)?example\.com$`.
- Allowing any subdomain trusts every subdomain's XSS.
- Prefix check `startsWith("https://app.example.com")` matches `https://app.example.com.evil.net`.

## Test
```
curl -s -I -H "Origin: https://evil.example" https://api.example.com/me | grep -i access-control
curl -s -I -H "Origin: null" https://api.example.com/me | grep -i access-control
```
Expect no `Access-Control-Allow-Origin` echoing those origins.

## Verify
- [ ] Untrusted and `null` origins get no ACAO header.
- [ ] Credentialed endpoints return a specific origin plus `Vary: Origin`.

## Checked
2026-10-28. Confirmed against official pages: wildcard and credentials rules, Vary: Origin, Access-Control-Max-Age and the null Origin value (MDN CORS guide).
Removed or rewritten: Express, Spring and NGINX examples and the sandboxed-iframe explanation (not in the fetched page); non-URL sources replaced.
Method: documentation only; no commands were run.
