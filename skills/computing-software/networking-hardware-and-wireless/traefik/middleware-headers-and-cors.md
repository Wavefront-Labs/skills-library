---
id: computing-software.networking-hardware-and-wireless.traefik.middleware-headers-and-cors
name: middleware-headers-and-cors
category: computing-software
field: networking-hardware-and-wireless
product: traefik
tags: [networking-hardware-and-wireless, traefik, headers, cors, security-headers, custom-headers, accesscontrolalloworiginlist, middleware]
level: practitioner
status: docs-checked
description: "Set custom request and response headers, CORS and security headers with the headers middleware in Traefik."
sources:
  - https://github.com/traefik/traefik/blob/master/docs/content/reference/routing-configuration/http/middlewares/headers.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# middleware headers and cors
The `headers` middleware manages request and response headers. `customRequestHeaders` and `customResponseHeaders` map names to values; an empty string value removes the header.

```yaml
http:
  middlewares:
    testHeader:
      headers:
        customRequestHeaders:
          X-Script-Name: "test"
          X-Custom-Request-Header: ""
        customResponseHeaders:
          X-Custom-Response-Header: ""
        accessControlAllowMethods: ["GET", "POST"]
        accessControlAllowOriginList: ["https://app.example.com"]
        accessControlMaxAge: 100
        addVaryHeader: true
```
CORS options: `accessControlAllowCredentials` (default false), `accessControlAllowHeaders`, `accessControlAllowMethods`, `accessControlAllowOriginList` (a `*` wildcard matches all; a value set by the backend is overwritten by Traefik; `null` is no longer supported), `accessControlAllowOriginListRegex` (partial regex match), `accessControlExposeHeaders`, `accessControlMaxAge` (seconds to cache preflight, default 0) and `addVaryHeader` (used with `accessControlAllowOriginList` to add or modify `Vary`).

Security options include `allowedHosts`, `hostsProxyHeaders`, `sslProxyHeaders`, `stsSeconds`, `stsIncludeSubdomains`, `stsPreload`, `forceSTSHeader`, `frameDeny`, `customFrameOptionsValue`, `contentTypeNosniff`, `browserXssFilter`, `customBrowserXSSValue`, `contentSecurityPolicy`, `contentSecurityPolicyReportOnly`, `referrerPolicy`, `permissionsPolicy` and `isDevelopment`.

Traefik also adds by default when proxying: `X-Forwarded-For`, `X-Real-Ip`, `X-Forwarded-Host`, `X-Forwarded-Port`, `X-Forwarded-Proto` and `X-Forwarded-Server`.

Gotcha: in YAML, escaped characters in `accessControlAllowOriginListRegex` must be escaped twice (`example\\.com`).

## Checked
2026-11-03. Confirmed against the Traefik headers reference page (docs/content/reference/routing-configuration/http/middlewares/headers.md): add/remove semantics, all option names and defaults, default forwarded headers, origin and regex notes. Removed: "do not combine wildcard origin with credentials", the "caches key on Origin" rationale, the curl Verify step, and the hedge about checking field names.
Method: documentation only; no commands were run.
