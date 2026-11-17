---
id: computing-software.devops-ci-cd.backstage.plugin-proxy
name: plugin-proxy
category: computing-software
field: devops-ci-cd
product: backstage
tags: [proxy-backend, proxy-endpoints, change-origin, backstage]
level: practitioner
status: docs-checked
description: "Reach external APIs from frontend plugin code through the built-in HTTP proxy configured under proxy.endpoints."
sources:
  - https://backstage.io/docs/plugins/proxying
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

The Backstage backend includes a basic HTTP proxy so frontend plugin code can reach backend service APIs. Add it to the backend:

```ts
backend.add(import('@backstage/plugin-proxy-backend'));
```

Configure endpoints in `app-config.yaml`:

```yaml
proxy:
  reviveConsumedRequestBodies: true
  endpoints:
    /simple-example: http://simple.example.com:8080
    '/larger-example/v1':
      target: http://larger.example.com:8080/svc.v1
      credentials: require
      headers:
        Authorization: Bearer ${EXAMPLE_AUTH_TOKEN}
```

Requests to `/api/proxy/<endpoint>/...` are forwarded to the target. Options include:

- `target`: the destination URL.
- `changeOrigin`: set to `true` when not specified (object targets are passed to http-proxy-middleware).
- `pathRewrite`: when not specified, a rewrite removes the whole prefix and route, for example `'^<url prefix><the string>/': '/'`.
- `credentials`: `require` (the default) needs Backstage credentials from the caller and does not forward them; `forward` also forwards them to the target; `dangerously-allow-unauthenticated` needs none.
- `headers`: values for the proxied request, for example `Authorization: Bearer ${EXAMPLE_AUTH_TOKEN}`.
- `allowedMethods` (for example `['GET']`) and `allowedHeaders` (for example `['Authorization']`); by default only safe, CORS-style headers are forwarded.

The proxy page is marked legacy documentation, but the configuration applies to both backend systems. Set `reviveConsumedRequestBodies: true` to fix missing POST bodies (set `Content-Type` to `application/json` or `application/x-www-form-urlencoded`). With `backend.auth.dangerouslyDisableDefaultAuthPolicy: true` the `credentials` value does not apply.

## Checked

2026-11-03. Confirmed against the Backstage Proxying page: plugin line, config shape, route mounting under `/api/proxy`, `credentials` values and default, defaults for `changeOrigin` and `pathRewrite`, header allow-lists, body revival. Removed: the CORS and browser-secrecy claims and the open-relay remark.

Method: documentation only; no commands were run.
