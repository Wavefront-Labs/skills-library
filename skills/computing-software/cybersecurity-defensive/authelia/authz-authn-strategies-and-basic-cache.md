---
id: computing-software.cybersecurity-defensive.authelia.authz-authn-strategies-and-basic-cache
name: authz-authn-strategies-and-basic-cache
category: computing-software
field: cybersecurity-defensive
product: authelia
tags: [authelia, authn-strategies, cookie-session, header-authorization, basic-auth, bearer, cache]
level: advanced
status: docs-checked
description: "Order Authelia authz authn_strategies, allow Basic or Bearer header credentials, and enable the Basic username and password cache with its lifespan."
sources:
  - https://www.authelia.com/configuration/miscellaneous/server-endpoints-authz/
  - https://www.authelia.com/reference/guides/proxy-authorization/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Each authz endpoint has an ordered `authn_strategies` list that decides how the user identity is established.

```yaml
authn_strategies:
  - name: 'HeaderAuthorization'
    schemes:
      - 'Basic'
    scheme_basic_cache_lifespan: 0
  - name: 'CookieSession'
```

Behaviour:

- Strategies are tried in order and the first that succeeds is used. If one fails for any reason other than the request lacking the information it needs, authentication short-circuits instead of falling through to the next.
- Valid case-sensitive names are `CookieSession`, `HeaderAuthorization`, `HeaderProxyAuthorization`, `HeaderAuthRequestProxyAuthorization` and `HeaderLegacy`.
- `schemes` lists `Basic` and/or `Bearer`. It applies only to the three header-authorization strategies and is unavailable on the `legacy` endpoint, which uses `Basic` only.
- `scheme_basic_cache_lifespan` enables caching of username and password combinations for Basic. Caching is completely disabled by default (value `0`). It is valid only when `Basic` is configured and cannot be used with the `Legacy` implementation.

Failure actions differ: `CookieSession` redirects the user for authentication, while `HeaderAuthorization` responds with `WWW-Authenticate` and 401. A strategy whose headers are absent from the request does not short-circuit, so the next one is tried; if none is left, the failure action is applied.

The configuration page says new options like these may not be used with the Legacy implementation, so create a separate named endpoint when you need them.

Check: call the endpoint with `curl -u user:pass` through the proxy and confirm a 2xx response with the identity headers.

## Checked

2026-11-08. Confirmed against the Server Authz Endpoints configuration page (authn_strategies order and short-circuit, strategy names, schemes Basic and Bearer, scheme_basic_cache_lifespan default and restrictions) and the Proxy Authorization reference guide (strategy results and failure actions). Removed: unsourced advice on strategy placement for API clients versus browsers. Fixed: the Legacy restriction is stated on the configuration page, not the reference guide.

Method: documentation only; no commands were run.
