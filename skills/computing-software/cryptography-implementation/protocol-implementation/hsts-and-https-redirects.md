---
id: computing-software.cryptography-implementation.protocol-implementation.hsts-and-https-redirects
name: hsts-and-https-redirects
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [cryptography-implementation, protocol-implementation, tls-configuration, hsts, strict-transport-security, hsts-preload, https-redirect, ssl-stripping, rfc6797]
level: practitioner
status: docs-checked
description: "Deploy HSTS safely: max-age ramp-up, includeSubDomains risks, preload list requirements and removal delay, redirect order, and checking every subdomain first."
sources: ["https://datatracker.ietf.org/doc/html/rfc6797", "https://hstspreload.org/", "https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Strict_Transport_Security_Cheat_Sheet.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HSTS and HTTPS redirects

A redirect from `http://` to `https://` can be stripped by a network attacker
on the first request (SSL stripping). HSTS (RFC 6797) tells the browser to use
HTTPS only for the host for `max-age` seconds, and to refuse click-through on
certificate errors.

## Header

```
Strict-Transport-Security: max-age=63072000; includeSubDomains; preload
```

- Send only over HTTPS responses (RFC 6797: a UA ignores the header on responses received over insecure transport).
- Send it on error responses too, and on every HTTPS redirect you serve.
- OWASP's example uses `max-age=63072000` (2 years); `includeSubDomains` and `preload` only after the checks below.

## Ramp up

1. Start with a short `max-age` such as `86400` (the OWASP rollout example) and no `preload`; watch for breakage.
2. Raise `max-age` in steps as you gain confidence, up to 1-2 years.
3. Add `includeSubDomains` only after inventorying every subdomain (DNS zone,
   certificate-transparency logs): any HTTP-only internal host (printer admin, legacy
   intranet, `http://` callback URLs) becomes unreachable for browsers that
   saw the header on the parent.
4. `preload` + submission at hstspreload.org: requirements are a valid cert,
   redirect HTTP to HTTPS on the same host (if listening on port 80), HTTPS on all
   subdomains (including internal ones), and on the base domain an HSTS header with
   max-age >= 31536000 (1 year), includeSubDomains and preload. A redirect you serve
   from the HTTPS site must itself carry the HSTS header.

Preload entries are hardcoded into browser releases and removal takes months to reach
users. Treat it as permanent. hstspreload.org also notes that browsers such as Chrome and Safari already upgrade
HTTP navigations and that preloading is not recommended for most sites.

## Redirect order

`http://example.com` -> `https://example.com` (same host first, so the HSTS
header is set for the apex) -> then `https://www.example.com` if canonical.
The preload requirements ask for the HTTP-to-HTTPS redirect on the same host,
so redirect `http://example.com` to `https://example.com` rather than straight to `https://www.`.

## Non-browser clients

HSTS is a browser feature. APIs and mobile apps should simply not speak HTTP:
do not listen on port 80 for API hostnames, or return an error rather than a
redirect (redirects leak credentials sent over HTTP on the first request).

## Verify

- [ ] `curl -sI https://host` shows a `strict-transport-security` header (also on error responses).
- [ ] All subdomains serve valid HTTPS before includeSubDomains/preload.
- [ ] `http://apex` redirects to `https://apex` first.

## Checked

2026-10-31. Confirmed in RFC 6797 (UA ignores the header over insecure transport; no user recourse on certificate
errors), the OWASP HSTS cheat sheet (63072000 and 86400 examples, includeSubDomains blocking HTTP-only subdomains,
no click-through) and hstspreload.org (submission requirements, 31536000 minimum, same-host redirect, HSTS header on
redirects, months to reach browsers). Removed as unconfirmed: the nginx `add_header` notes, the 300-second and
"a week" ramp steps, the `crt.sh` reference and the claim that the preload checker rejects a redirect straight to www.
Method: documentation only; no commands were run.
