---
id: computing-software.cybersecurity-defensive.authelia.authz-endpoint-implementations
name: authz-endpoint-implementations
category: computing-software
field: cybersecurity-defensive
product: authelia
tags: [authelia, forward-auth, ext-authz, auth-request, authz, reverse-proxy, endpoints]
level: practitioner
status: docs-checked
description: "Choose and configure Authelia's authz endpoints (forward-auth, ext-authz, auth-request, legacy) and map each to the proxy that speaks its protocol."
sources:
  - https://www.authelia.com/configuration/miscellaneous/server-endpoints-authz/
  - https://www.authelia.com/reference/guides/proxy-authorization/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The reverse proxy asks Authelia whether a request is allowed by calling an endpoint under `/api/authz/<name>`. The name is whatever key you give under `server.endpoints.authz`, using alphanumerics plus `-`, `_` and `/`, starting and ending alphanumeric.

```yaml
server:
  endpoints:
    authz:
      forward-auth:
        implementation: 'ForwardAuth'
      ext-authz:
        implementation: 'ExtAuthz'
      auth-request:
        implementation: 'AuthRequest'
```

`implementation` is case-sensitive and one of `ForwardAuth`, `ExtAuthz`, `AuthRequest` or `Legacy`:

- ForwardAuth serves Traefik (ForwardAuth middleware), Caddy (`forward_auth`), HAProxy (auth-request lua plugin) and Skipper. It reads method, scheme, host, path and client IP from `X-Forwarded-*` headers.
- ExtAuthz serves Envoy through the HTTP ExtAuthz filter and reads the method and host from the request itself.
- AuthRequest serves NGINX through `auth_request`, reading `X-Original-Method` and `X-Original-URL`. It cannot redirect automatically, so NGINX must redirect using the `Location` header Authelia returns.
- Legacy lives at `/api/verify` and uses the `HeaderLegacy` and `CookieSession` strategies.

The defaults are `forward-auth`, `ext-authz`, `auth-request` and `legacy`. Point each proxy at the endpoint whose implementation speaks its protocol.

Check: send a request through the proxy while logged out and confirm you are redirected to the Authelia portal.

## Checked

2026-11-08. Confirmed against the Server Authz Endpoints configuration page (name rules, /api/authz/ path, implementation values) and the Proxy Authorization reference guide (default endpoints table, proxies per implementation, metadata headers, AuthRequest redirect note, Legacy path and strategies). Removed: an unsourced claim about misread headers.

Method: documentation only; no commands were run.
