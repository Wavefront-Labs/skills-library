---
id: computing-software.web-development.hono.hono-context-storage
name: hono-context-storage
category: computing-software
field: web-development
product: hono
tags: [hono, middleware, context, asynclocalstorage]
level: practitioner
status: docs-checked
description: "Access the Hono Context outside handlers with contextStorage, getContext and tryGetContext, including Cloudflare bindings and AsyncLocalStorage needs."
sources:
  - https://github.com/honojs/website/blob/main/docs/middleware/builtin/context-storage.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Context storage

Import: `import { contextStorage, getContext, tryGetContext } from 'hono/context-storage'`.

It stores the Hono `Context` in `AsyncLocalStorage` so any function can reach it. The runtime must support `AsyncLocalStorage`. On Cloudflare Workers add the `nodejs_compat` or `nodejs_als` flag to `wrangler.toml`.

```ts
type Env = { Variables: { message: string } }
const app = new Hono<Env>()

app.use(contextStorage())
app.use(async (c, next) => {
  c.set('message', 'Hello!')
  await next()
})

const getMessage = () => getContext<Env>().var.message

app.get('/', (c) => c.text(getMessage()))
```

Bindings outside handlers (Workers):

```ts
type Env = { Bindings: { KV: KVNamespace } }
const app = new Hono<Env>()
app.use(contextStorage())
const setKV = (value: string) => getContext<Env>().env.KV.put('key', value)
```

## tryGetContext
Like `getContext()` but returns `undefined` instead of throwing when no context is available:

```ts
const context = tryGetContext<Env>()
if (context) console.log(context.var.message)
```

## Gotcha
`getContext()` returns the current Context only if `contextStorage()` is applied as middleware; `tryGetContext()` is the variant that returns `undefined` instead of throwing when the context is not available.

## Checked

2026-11-04. Read in full from the honojs/website docs repository: docs/middleware/builtin/context-storage.md. Confirmed against the page: every parameter name, default, import path, option value and code example left in this skill. Removed: the invented Verify step (curl/tsc/browser checks the page does not describe); the ordering claim ("register it first").

Method: documentation only; no commands were run.
