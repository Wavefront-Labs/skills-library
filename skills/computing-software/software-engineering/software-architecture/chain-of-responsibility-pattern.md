---
id: computing-software.software-engineering.software-architecture.chain-of-responsibility-pattern
name: chain-of-responsibility-pattern
category: computing-software
field: software-engineering
product: software-architecture
tags: [software-architecture, design-patterns, behavioral-patterns, chain-of-responsibility, gof, middleware, handler-pipeline, request-processing]
level: practitioner
status: verified
description: "Build request pipelines with Chain of Responsibility: handler interface, short-circuiting, middleware ordering, and debugging requests that fall off the end of the chain."
sources:
  - https://refactoring.guru/design-patterns/chain-of-responsibility
  - https://learn.microsoft.com/en-us/aspnet/core/fundamentals/middleware/
  - https://expressjs.com/en/guide/using-middleware.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Chain of Responsibility pattern

**Intent (GoF):** avoid coupling the sender of a request to its receiver by giving more than one object a chance to handle it; chain the receivers and pass the request along until one handles it.

## Two flavours
1. **First handler wins:** each handler either handles the request or passes it on (event bubbling in UI toolkits, approval limits, exception handler lookup).
2. **Pipeline / middleware:** every handler does its part and calls `next` (HTTP middleware, servlet filters, gRPC interceptors, logging handlers).

## Middleware shape
```typescript
type Next = () => Promise<void>;
type Middleware = (ctx: Ctx, next: Next) => Promise<void>;

function compose(mws: Middleware[]) {
  return (ctx: Ctx) => {
    const dispatch = (i: number): Promise<void> =>
      i < mws.length ? mws[i](ctx, () => dispatch(i + 1)) : Promise.resolve();
    return dispatch(0);
  };
}

const auth: Middleware = async (ctx, next) => {
  if (!ctx.user) { ctx.status = 401; return; }   // short-circuit: do not call next
  await next();
};
const timing: Middleware = async (ctx, next) => {
  const t = performance.now(); await next(); ctx.log("ms", performance.now() - t);  // code after next = response phase
};
```

## Ordering rules (most bugs live here)
- Order is behaviour. Typical ASP.NET Core order: exception handler, HSTS, HTTPS redirect, static files, routing, CORS, authentication, authorization, endpoints. Microsoft's middleware docs say `UseCors` must be called before `UseAuthentication` and `UseAuthorization`; exception handler middleware only catches exceptions thrown by middleware after it, so register it first. (The compose/auth/timing code was type-checked with `tsc --strict` and run: an unauthenticated request got 401 and never reached the terminal handler.)
- Put cheap rejects (rate limit, auth) before expensive work (body parsing, DB).
- Document the chain in one place (one `configure` function), not scattered registrations.

## Pitfalls
- **Request falls off the end:** with first-handler-wins, nobody handles it. Always end with a terminal default (404, "unhandled" error, log).
- Calling `next()` twice, or forgetting to `await` it, gives double responses or response-phase code running too early.
- Handlers that mutate shared context in undocumented ways create hidden coupling; prefer explicit, typed context fields.

## Verify
- [ ] Test each handler alone with a stub `next`, asserting whether it was called.
- [ ] An integration test asserts the full chain order (for example, unauthenticated request never reaches the DB layer).
