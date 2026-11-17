---
id: computing-software.cloud-infrastructure-engineering.contour.contour-cookie-rewriting
name: contour-cookie-rewriting
category: computing-software
field: cloud-infrastructure-engineering
product: contour
tags: [cookierewritepolicies, set-cookie, samesite, secure, pathrewrite, domainrewrite, session-affinity-cookie]
level: practitioner
status: docs-checked
description: "HTTPProxy cookieRewritePolicies on routes or services: rewrite Set-Cookie Path, Domain, Secure, SameSite, including the X-Contour-Session-Affinity cookie."
sources: ["https://github.com/projectcontour/contour/blob/main/site/content/docs/main/config/cookie-rewriting.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# HTTPProxy cookie rewriting

`cookieRewritePolicies` customises attributes of `Set-Cookie` response headers, per route or per service. Rewritable: `Path`, `Domain`, `Secure`, `SameSite`. It helps when Contour rewrites paths or hostnames so the application cannot know the right values.

Per route:

```yaml
routes:
- conditions: [{prefix: /payments}]
  services: [{name: payment-app, port: 80}]
  cookieRewritePolicies:
  - name: X-User-Session
    pathRewrite:
      value: /payments
    sameSite: Lax
  - name: X-User-Data
    sameSite: Lax
```

Per service (to treat backends in one route differently):

```yaml
services:
- name: backend-1
  port: 80
  cookieRewritePolicies:
  - name: X-User-Data-1
    domainRewrite:
      value: cookie-rewrite-service.com
```

Fields: `name` (the cookie), `pathRewrite.value`, `domainRewrite.value`, `secure`, `sameSite` (examples use `Lax` and `Strict`).

Session affinity cookie: Envoy generates a bare-bones `X-Contour-Session-Affinity` cookie for `loadBalancerPolicy.strategy: Cookie` and does not set `SameSite` or `Secure`. Harden it:

```yaml
loadBalancerPolicy:
  strategy: Cookie
cookieRewritePolicies:
- name: X-Contour-Session-Affinity
  sameSite: Strict
  secure: true
```

If the backing service returns the named cookie in a `Set-Cookie` response header, it is rewritten with the configured values.

## Checked

2026-11-08. Read the Contour main-branch config page cookie-rewriting.md in full. Confirmed: per-route and per-service placement, the four rewritable attributes, field names and examples, and the session affinity cookie behaviour and hardening example. Removed the claim that `sameSite` accepts only listed values beyond those shown in the examples.

Method: documentation only; no commands were run.
