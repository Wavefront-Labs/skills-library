---
id: computing-software.web-development.frontend-development.https-and-hsts
name: https-and-hsts
category: computing-software
field: web-development
product: frontend-development
tags: [security-headers, http-security-headers, hsts, https-redirect, hsts-preload, mixed-content, upgrade-insecure-requests, tls]
level: practitioner
status: docs-checked
description: "Enforcing HTTPS: 301 redirects, HSTS with includeSubDomains and preload, preload-list risks, mixed content and upgrade-insecure-requests."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Strict-Transport-Security
  - https://hstspreload.org/
  - https://developer.mozilla.org/en-US/docs/Web/Security/Defenses/Mixed_content
  - https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Strict_Transport_Security_Cheat_Sheet.html
  - https://docs.djangoproject.com/en/stable/ref/settings/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HTTPS everywhere and HSTS

**Goal:** browsers only ever talk to your site over TLS, including the first request.

## 1. Redirect then pin
1. Port 80 answers with `301` to the same path on `https://` (no content).
2. HTTPS responses send:
```
Strict-Transport-Security: max-age=63072000; includeSubDomains; preload
```
After the browser sees this once, it rewrites `http://` to `https://` internally for `max-age` seconds. The `Strict-Transport-Security` header is only honoured when received over HTTPS, so do not rely on it in the redirect response from plain HTTP.

## 2. Roll out in steps
- hstspreload.org recommends ramping up: `max-age=300; includeSubDomains` (5 min), then `max-age=604800` (1 week), then `max-age=2592000` (1 month), waiting the full max-age between steps. Only add `includeSubDomains` when **every** subdomain (including internal ones and `www` if it has a DNS record) serves valid HTTPS.
- Then raise to at least `31536000` (1 year); the hstspreload.org example header uses `max-age=63072000; includeSubDomains; preload`.
To disable HSTS send `max-age=0`; clients that never revisit stay pinned until their stored policy expires.

## 3. Preload list
hstspreload.org (run by Google; all browsers use the list) bakes the domain into browsers so even the very first visit is HTTPS. Requirements: valid certificate; if port 80 is open, redirect HTTP to HTTPS on the same host; all subdomains served over HTTPS; HSTS header on the base domain's HTTPS responses with `max-age` of at least 31536000, `includeSubDomains` and `preload` (any redirect served from the HTTPS site must carry the header too). The site says inclusion cannot easily be undone and removal takes months to reach users via a Chrome update, so treat it as permanent.

## 4. Where to set it
At the edge that terminates TLS (CDN/load balancer/nginx: `add_header Strict-Transport-Security "…" always;`) or app: helmet (`hsts`), Django `SECURE_HSTS_SECONDS` (default 0), `SECURE_HSTS_INCLUDE_SUBDOMAINS`, `SECURE_HSTS_PRELOAD`, `SECURE_SSL_REDIRECT`; Rails `config.force_ssl = true` (the Security Guide says it adds the HSTS header; `config.ssl_options` tunes it). Behind a TLS-terminating proxy make sure the app sees the original scheme, or redirects can loop.

## 5. Mixed content
Per MDN, browsers auto-upgrade image, video and audio requests from HTTP to HTTPS and block insecure requests for all other resource types (scripts, stylesheets, iframes and so on). During migration the CSP directive `upgrade-insecure-requests` rewrites insecure subresource requests. Fix hard-coded `http://` URLs in content/DB.

## Verify
- [ ] `curl -sI http://example.com` -> 301 to https; `curl -sI https://example.com | grep -i strict` shows the header.
- [ ] SSL Labs / Mozilla Observatory show HSTS with the intended max-age.
- [ ] No mixed-content warnings in the console across key pages.

## Checked
Checked 2026-10-26 against MDN Strict-Transport-Security (301 redirect, header ignored over HTTP, preload needs max-age >= 31536000 and includeSubDomains, max-age=0 disables), hstspreload.org (requirements, ramp-up schedule, removal warning, example header), MDN Mixed content, the Django settings reference (SECURE_HSTS_* and SECURE_SSL_REDIRECT names; HSTS_SECONDS default 0) and the Rails Security Guide (force_ssl adds HSTS). Corrected the rollout (includeSubDomains in every ramp step; preload minimum is 1 year, not 2). Removed the unconfirmed 'refuses click-through' wording and the claim that Rails force_ssl also sets secure cookies.

Method: documentation only; no commands were run.
