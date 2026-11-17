---
id: computing-software.web-development.node-express.production-hardening-and-security
name: production-hardening-and-security
category: computing-software
field: web-development
product: node-express
tags: [express, node, security, helmet, cors, rate-limiting, validation, graceful-shutdown, csrf, headers, production, web-development]
level: advanced
status: verified
description: "Hardening an Express app for production: helmet headers, CORS that isn't wildcard-open, rate limiting, input validation, and graceful shutdown."
sources:
  - https://helmetjs.github.io/
  - https://expressjs.com/en/advanced/best-practice-security.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hardening Express for production

**Goal:** the baseline a security review will ask about before an Express API
goes live — most of it is middleware you add once, not architecture.

## 1. Headers: `helmet`, not hand-rolled
```js
app.use(helmet());   // helmet 8.3.0 set 13 security headers in a run (CSP, HSTS, X-Content-Type-Options, X-Frame-Options, COOP, CORP, Referrer-Policy, ...)
```
Default is a reasonable baseline; the one header most apps need to customise is
Content-Security-Policy, which defaults restrictively (ran: `default-src 'self'`, `script-src 'self'`, `script-src-attr 'none'`, `style-src 'self' https: 'unsafe-inline'`, `object-src 'none'`, ...) and will block inline
scripts/third-party widgets until explicitly allowed:
```js
app.use(helmet({ contentSecurityPolicy: { directives: { scriptSrc: ["'self'", 'https://trusted-cdn.com'] } } }));
```
Don't disable `helmet()` wholesale because one header broke something — scope the
fix to that directive.

## 2. CORS — never `cors()` with no options in production
`app.use(cors())` with no config sends `Access-Control-Allow-Origin: *` (ran with cors 2.8.6), which
is fine for a public read-only API but disastrous combined with
`credentials: true` (browsers reject wildcard origin + credentials, but a careless
"reflect whatever Origin header the request sent" implementation effectively
allows any site to make authenticated requests on a logged-in user's behalf).
```js
app.use(cors({ origin: ['https://app.example.com'], credentials: true }));
```
Maintain an explicit allowlist; validate `Origin` against it rather than echoing
it back unconditionally.

## 3. Rate limiting — per-route, not just global
```js
const authLimiter = rateLimit({ windowMs: 15 * 60 * 1000, limit: 5 });   // `max` is the older name; both worked on express-rate-limit 8.7.1 (6th request got 429)
app.post('/login', authLimiter, loginHandler);
```
A single global limiter set loose enough not to bother normal API traffic does
nothing to stop credential-stuffing on `/login` specifically — apply tighter limits
to auth and any expensive endpoint (search, export, password reset) separately. In
a multi-instance deployment, use a shared store (`rate-limit-redis`) — an in-memory
limiter resets per instance and per restart, making it trivially bypassable.

## 4. Input validation at the boundary, not inside business logic
Validate (and coerce/strip) request bodies with `zod`/`joi`/`express-validator`
*before* a handler touches them — don't rely on the ORM or a downstream function
to reject bad shapes. Validation failures should return 400 with a field-level
error, not bubble up as a 500 from a type error three functions deep.
```js
const schema = z.object({ email: z.string().email(), age: z.number().int().positive() });
app.post('/users', (req, res, next) => {
  const parsed = schema.safeParse(req.body);
  if (!parsed.success) return res.status(400).json(parsed.error.flatten());   // ran on zod 4.6.7: {formErrors, fieldErrors}
  // parsed.data is now trustworthy
});
```

## 5. Errors shouldn't leak and shouldn't crash the process
A synchronous throw inside an async route handler without `next(err)` becomes an
unhandled rejection; register a centralized error-handling middleware (4 args,
last registered) and wrap async handlers (or use Express 5's native async
support) so every error reaches it. Never send `err.stack` to the client in
production — log it server-side, return a generic message.

## 6. Graceful shutdown
```js
const server = app.listen(port);
process.on('SIGTERM', () => {
  server.close(() => { db.end(); process.exit(0); });
  setTimeout(() => process.exit(1), 10_000).unref(); // force-exit if close hangs
});
```
Without this, a rolling deploy/orchestrator SIGTERM kills in-flight requests and
leaves DB connections dangling. Always set a hard timeout fallback — a stuck
request can block `server.close()`'s callback indefinitely. (Ran on Node 24: an idle keep-alive connection did not block it, since recent Node closes idle connections on `close()`; `server.closeIdleConnections()` and `closeAllConnections()` exist for older behaviour and stuck sockets.)

## Verify
- [ ] `helmet()` is applied; CSP is scoped (not disabled) if something is blocked.
- [ ] CORS uses an explicit origin allowlist, not `*` combined with credentials.
- [ ] Auth/expensive routes have a tighter rate limit than the global default, backed by a shared store if multi-instance.
- [ ] Every input is validated against a schema before the handler's business logic runs.
- [ ] A central error handler exists; `SIGTERM` triggers `server.close()` with a force-exit timeout.
