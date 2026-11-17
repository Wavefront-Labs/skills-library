---
id: computing-software.web-development.hono.hono-combine-middleware
name: hono-combine-middleware
category: computing-software
field: web-development
product: hono
tags: [hono, middleware, combine, access-control]
level: practitioner
status: docs-checked
description: "Compose Hono middleware with some, every and except from hono/combine to build conditional auth and rate-limit rules."
sources:
  - https://github.com/honojs/website/blob/main/docs/middleware/builtin/combine.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Combine middleware

Import: `import { some, every, except } from 'hono/combine'`.

- `some(...mw)`: runs middleware in order; the first that succeeds wins and later ones do not run.
- `every(...mw)`: runs all in order; stops if any throws.
- `except(condition, ...mw)`: runs the middleware unless the condition matches. Condition is a string or function; use an array for several targets.

## Examples

Skip rate limiting for clients with a valid token:

```ts
app.use('/api/*', some(bearerAuth({ token }), myRateLimit({ limit: 100 })))
```

Skip auth and rate limiting on the local network:

```ts
app.use(
  '/api/*',
  some(
    myCheckLocalNetwork(),
    every(bearerAuth({ token }), myRateLimit({ limit: 100 }))
  )
)
```

Require a token except for public routes:

```ts
app.use('/api/*', except('/api/public/*', bearerAuth({ token })))
```

Complex rule: `some(every(ipRestriction(getConnInfo, { allowList: ['192.168.0.2'] }), bearerAuth({ token })), rateLimit())` means rateLimit is skipped only when both IP and token checks pass.

## Gotcha
`some` runs the first middleware that returns true; middleware is applied in order, and once one exits successfully the later ones do not run. In `some(bearerAuth({ token }), myRateLimit({ limit: 100 }))` a client with a valid token skips rate limiting. `every` runs all given middleware, and `except` runs them only if the path condition is not met.

## Checked

2026-11-04. Read in full from the honojs/website docs repository: docs/middleware/builtin/combine.md. Confirmed against the page: every parameter name, default, import path, option value and code example left in this skill. Removed: the invented Verify step (curl/tsc/browser checks the page does not describe).

Method: documentation only; no commands were run.
