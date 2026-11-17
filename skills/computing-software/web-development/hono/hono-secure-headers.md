---
id: computing-software.web-development.hono.hono-secure-headers
name: hono-secure-headers
category: computing-software
field: web-development
product: hono
tags: [hono, middleware, security, csp, headers]
level: practitioner
status: docs-checked
description: "Set security headers in Hono with secureHeaders: defaults, disabling headers, CSP with nonces, Reporting-Endpoints and Permissions-Policy."
sources:
  - https://github.com/honojs/website/blob/main/docs/middleware/builtin/secure-headers.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Secure headers

Import: `import { secureHeaders, NONCE } from 'hono/secure-headers'` (type `SecureHeadersVariables`).

```ts
app.use(secureHeaders()) // sensible defaults
app.use('*', secureHeaders({ xFrameOptions: false, xXssProtection: false }))
app.use('*', secureHeaders({
  strictTransportSecurity: 'max-age=63072000; includeSubDomains; preload',
  xFrameOptions: 'DENY',
  xXssProtection: '1',
}))
```

## Defaults (option: value)
`crossOriginResourcePolicy: same-origin`, `crossOriginOpenerPolicy: same-origin`, `originAgentCluster: ?1`, `referrerPolicy: no-referrer`, `strictTransportSecurity: max-age=15552000; includeSubDomains`, `xContentTypeOptions: nosniff`, `xDnsPrefetchControl: off`, `xDownloadOptions: noopen`, `xFrameOptions: SAMEORIGIN`, `xPermittedCrossDomainPolicies: none`, `xXssProtection: 0`, and `X-Powered-By` is deleted. `crossOriginEmbedderPolicy` (require-corp) is OFF by default. No default for `contentSecurityPolicy`, `contentSecurityPolicyReportOnly`, `trustedTypes`, `requireTrustedTypesFor`, `reportingEndpoints`, `reportTo`, `permissionsPolicy`.

## CSP
`contentSecurityPolicy: { defaultSrc: ["'self'"], scriptSrc: ["'self'"], objectSrc: ["'none'"], upgradeInsecureRequests: [], reportTo: 'endpoint-1', reportUri: '/csp-report', ... }` with `reportingEndpoints: [{ name: 'endpoint-1', url: 'https://example.com/reports' }]` (or `reportTo: [{ group, max_age, endpoints: [{ url }] }]`).

## Nonce
```tsx
const app = new Hono<{ Variables: SecureHeadersVariables }>()
app.get('*', secureHeaders({ contentSecurityPolicy: { scriptSrc: [NONCE, 'https://allowed1.example.com'] } }))
app.get('/', (c) => c.html(<html><body><script src='/js/client.js' nonce={c.get('secureHeadersNonce')} /></body></html>))
```
Custom generator: a function `(c) => { const nonce = ...; c.set('myNonce', nonce); return `'nonce-${nonce}'` }` placed in `scriptSrc`; it runs on every request.

## Permissions-Policy
`permissionsPolicy: { fullscreen: ['self'], camera: false, microphone: true, geolocation: ['*'], payment: ['self', 'https://example.com'], syncXhr: [] }` yields `fullscreen=(self)`, `camera=()`, `microphone=*`, and so on.

## Gotcha
Order matters with `poweredBy()`: `secureHeaders()` before `poweredBy()` removes `x-powered-by`; the reverse order adds it back.

## Checked
2026-11-04: every claim left was read in the honojs/website docs page middleware/builtin/secure-headers.md (options table for defaults). Removed: the invented Verify step.
Method: documentation only; no commands were run.
