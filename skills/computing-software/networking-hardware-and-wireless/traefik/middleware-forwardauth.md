---
id: computing-software.networking-hardware-and-wireless.traefik.middleware-forwardauth
name: middleware-forwardauth
category: computing-software
field: networking-hardware-and-wireless
product: traefik
tags: [networking-hardware-and-wireless, traefik, forwardauth, authentication, delegated-auth, authresponseheaders, middleware]
level: practitioner
status: docs-checked
description: "Delegate authentication to an external service with forwardAuth, controlling copied headers, body forwarding and size limits."
sources:
  - https://github.com/traefik/traefik/blob/master/docs/content/reference/routing-configuration/http/middlewares/forwardauth.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# middleware forwardauth
`forwardAuth` delegates authentication to an external service. If it answers 2XX, access is granted and the original request is performed; otherwise the authentication server's response is returned to the client.

Options: `address` (required), `authResponseHeaders` (headers copied from the auth response onto the forwarded request, replacing conflicting ones), `authResponseHeadersRegex`, `authRequestHeaders` (headers sent to the auth server; empty means all), `addAuthCookiesToResponse`, `forwardBody`, `maxBodySize`, `maxResponseBodySize`, `headerField` (header that stores the authenticated user), `preserveLocationHeader`, `preserveRequestMethod`, `authSigninURL` (redirect target when the auth server returns 401), `trustForwardHeader` and `tls.*` (`ca`, `cert`, `key`, `insecureSkipVerify`; `caSecret` and `certSecret` on the Kubernetes CRD only).

```yaml
http:
  middlewares:
    test-auth:
      forwardAuth:
        address: "https://example.com/auth"
        authResponseHeaders:
          - X-Auth-User
        maxBodySize: 1048576
```
The auth server receives the request details as `X-Forwarded-Method`, `X-Forwarded-Proto`, `X-Forwarded-Host`, `X-Forwarded-Uri` and `X-Forwarded-For`.

Gotchas: `forwardBody: true` reads the body inside Traefik, which breaks streaming. A body larger than `maxBodySize` (default -1, unlimited) gets a 401; a larger auth response than `maxResponseBodySize` also gets a 401. The docs strongly recommend setting both limits, since unlimited sizes risk DoS and memory exhaustion. `trustForwardHeader` is deprecated: configure `forwardedHeaders.trustedIPs` on the entrypoint and set `trustForwardHeader` explicitly to `true` or `false`, otherwise Traefik logs a startup warning and uses legacy behaviour. `authResponseHeadersRegex` matches partially, so anchor it with `^` and `$`.

## Checked
2026-11-03. Confirmed against the Traefik forwardAuth reference page (docs/content/reference/routing-configuration/http/middlewares/forwardauth.md): option list, defaults, 2XX behaviour, 401 on oversize bodies, forwarded headers, trustForwardHeader deprecation, regex anchoring. Removed: the claim that headers not listed in authResponseHeaders are "silently dropped", "login redirects" framing, and the invented Verify step.
Method: documentation only; no commands were run.
