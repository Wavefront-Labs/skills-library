---
id: computing-software.devops-ci-cd.verdaccio.configure-cors
name: configure-cors
category: computing-software
field: devops-ci-cd
product: verdaccio
tags: [cors, access-control, preflight, cors-headers, access-control-allow-origin, server-cors]
level: practitioner
status: docs-checked
description: "Replace Verdaccio's permissive Access-Control-Allow-Origin * with server.cors options on 7.x, and why CORS is not access control for npm clients."
sources:
  - https://verdaccio.org/docs/configuration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Available from 7.x. By default every response carries `Access-Control-Allow-Origin: *`. `server.cors` is passed straight to the `cors` middleware:

```yaml
server:
  cors:
    origin: 'https://apps.example.com'
    methods: ['GET', 'PUT']
    allowedHeaders: ['Authorization']
    exposedHeaders: ['X-Custom-Header']
    credentials: true
    maxAge: 600
```
Properties: `origin` (string, boolean, regexp or array), `methods` (default GET,HEAD,PUT,PATCH,POST,DELETE), `allowedHeaders` (default reflects the request), `exposedHeaders`, `credentials` (default false), `maxAge`, `preflightContinue` (false), `optionsSuccessStatus` (204). Omit the section to keep today's behaviour.

Gotchas:
- CORS is a browser rule only. npm, yarn and pnpm send no Origin header, so restricting `origin` does not protect the registry; use `packages` access rules.
- `origin: '*'` with `credentials: true` is rejected by browsers; name origins.
- The web UI is served from the registry's own origin, so tightening CORS does not affect it.

## Checked

2026-11-04. Confirmed against the Verdaccio Configuration page (CORS section: 7.x only, default permissive header, option table and defaults, caution notes). Removed: the closing Verify tip.
Method: documentation only; no commands were run.
