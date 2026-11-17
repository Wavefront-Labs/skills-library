---
id: computing-software.web-development.hono.hono-context-variables-env
name: hono-context-variables-env
category: computing-software
field: web-development
product: hono
tags: [hono, api, context, typescript, bindings]
level: practitioner
status: docs-checked
description: "Pass typed data between Hono middleware and handlers with c.set/c.get/c.var, Bindings and Variables generics, c.env, executionCtx, c.error and ContextVariableMap."
sources:
  - https://github.com/honojs/website/blob/main/docs/api/context.md
  - https://github.com/honojs/website/blob/main/docs/api/hono.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Context variables, bindings and env

## Typed Variables and Bindings
```ts
type Bindings = { TOKEN: string }
type Variables = { user: User }

const app = new Hono<{ Bindings: Bindings; Variables: Variables }>()

app.use('/auth/*', async (c, next) => {
  const token = c.env.TOKEN   // string
  c.set('user', user)         // typed User
  await next()
})
```

`c.set('message', 'Hono is cool!!')` / `c.get('message')` hold values only for the current request; they are not shared across requests. `c.var.message` is the property form.

## Middleware that adds a custom method
```ts
type Env = { Variables: { echo: (str: string) => string } }
const echoMiddleware = createMiddleware<Env>(async (c, next) => {
  c.set('echo', (str) => str)
  await next()
})
app.get('/echo', echoMiddleware, (c) => c.text(c.var.echo('Hello!')))
```
To use it via `app.use(echoMiddleware)`, pass `Env` to `new Hono<Env>()`.

## Cloudflare helpers
- `c.env.MY_KV.get('my-key')`: bindings (variables, secrets, KV, D1, R2) via `c.env.BINDING_KEY`.
- `c.executionCtx.waitUntil(c.env.KV.put(key, data))`.
- `c.event` is only set with Service Worker syntax and is not recommended now.
- To type `exports`: `declare module 'hono' { interface ExecutionContext { readonly exports: Cloudflare.Exports } }`.

## c.error
If a handler throws, the error is placed in `c.error`, readable in middleware after `await next()`: `if (c.error) { /* ... */ }`.

## ContextVariableMap (global typing)
```ts
declare module 'hono' {
  interface ContextVariableMap { result: string }
}
```

## Gotcha
`ContextVariableMap` types the variable on ALL contexts, even handlers where the middleware never ran, so `c.get('result')` looks like `string` but may be `undefined` at runtime. The page says it is appropriate only when the variable is set by middleware applied app-wide and guaranteed to exist.

## Checked

2026-11-04. Read in full from the honojs/website docs repository: docs/api/context.md, docs/api/hono.md. Confirmed against the page: every parameter name, default, import path, option value and code example left in this skill. Removed: the invented Verify step (curl/tsc/browser checks the page does not describe); the "otherwise use per-app Variables generics" advice (not stated as a rule).

Method: documentation only; no commands were run.
