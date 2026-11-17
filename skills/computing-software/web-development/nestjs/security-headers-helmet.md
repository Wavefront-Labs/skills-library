---
id: computing-software.web-development.nestjs.security-headers-helmet
name: security-headers-helmet
category: computing-software
field: web-development
product: nestjs
tags: [nestjs, security, helmet, csp, security-headers]
level: practitioner
status: docs-checked
description: "Set security headers in NestJS v12.1+ with app.useSecurityHeaders, tune Content-Security-Policy, or use Helmet and fastify-helmet directly."
sources:
  - https://github.com/nestjs/docs.nestjs.com/blob/master/content/security/helmet.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
From NestJS v12.1 `app.useSecurityHeaders()` sets Helmet 8 defaults on Express and Fastify with no extra package. It runs on every response including 404s, errors and SSE, and removes `X-Powered-By`.

```typescript
const app = await NestFactory.create(AppModule);
app.useSecurityHeaders();
```

Call it right after `NestFactory.create()`, before `init()` or `listen()` (calling it later or twice throws). Middleware registered with `app.use()` earlier runs first and its own responses lack the headers.

Configure per header: `false` omits it, `true` sends the default, an object tunes it.

```typescript
app.useSecurityHeaders({
  xFrameOptions: false,
  strictTransportSecurity: { maxAge: 63072000, preload: true },
  referrerPolicy: { policy: 'strict-origin-when-cross-origin' },
});
```

CSP directives: camelCase or kebab-case names; a set directive replaces the default of the same name (keep `'self'`); `null` or `false` removes one; keywords must be single-quoted (`"'self'"`). `useDefaults: false` drops the defaults (then provide `defaultSrc`). `reportOnly: true` sends `Content-Security-Policy-Report-Only`.

```typescript
app.useSecurityHeaders({
  contentSecurityPolicy: {
    directives: { scriptSrc: ["'self'", 'https://cdn.example.com'], upgradeInsecureRequests: null },
  },
});
```

A route can override a header with `@Header('Cross-Origin-Resource-Policy', 'cross-origin')`.

Gotchas:
- Helmet's legacy names are rejected (`hsts` should be `strictTransportSecurity`, `frameguard` is `xFrameOptions`, `hidePoweredBy` is `xPoweredBy`, and so on). Function-valued CSP directives (nonces) are not supported.
- The default `upgrade-insecure-requests` breaks Swagger UI served over plain HTTP outside local development. `'unsafe-inline'` in `script-src` removes most XSS protection.
- To use Helmet itself: `app.use(helmet())` on Express, `await app.register(helmet)` from `@fastify/helmet` on Fastify, registered before other middleware.

## Checked

2026-11-04. Confirmed against the official NestJS docs source: useSecurityHeaders from v12.1, Helmet 8 defaults, option values, CSP directive rules, useDefaults and reportOnly, legacy names rejected, function directives unsupported, Swagger note, using Helmet directly (helmet page). Removed: wrong lower-case method name usesecurityheaders (now useSecurityHeaders); localhost wording; invented Verify step.

Method: documentation only; no commands were run.
