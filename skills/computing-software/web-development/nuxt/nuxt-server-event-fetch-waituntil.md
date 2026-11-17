---
id: computing-software.web-development.nuxt.nuxt-server-event-fetch-waituntil
name: nuxt-server-event-fetch-waituntil
category: computing-software
field: web-development
product: nuxt
tags: [nuxt, server, event-fetch, waituntil, nitro]
level: advanced
status: docs-checked
description: "Forward headers and context between internal Nuxt server calls with event.$fetch and run background work after the response with event.waitUntil."
sources:
  - https://github.com/nuxt/nuxt/blob/main/docs/2.directory-structure/1.server.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default neither the incoming request's headers nor its context are forwarded when a server route makes a fetch. Use `event.$fetch` to forward both:

```ts
export default defineEventHandler((event) => {
  return event.$fetch('/api/forwarded')
})
```

Headers not meant to be forwarded are not included, for example `transfer-encoding`, `connection`, `keep-alive`, `upgrade`, `expect`, `host`, `accept`.

Background work: `event.waitUntil(promise)` awaits a promise in the background without delaying the response. The promise is awaited before the handler terminates, so the task completes even if the server would otherwise end the handler right after the response is sent (examples given: caching and logging). The page says this integrates with runtime providers' native capabilities for async work after the response.

```ts
const timeConsumingBackgroundTask = async () => {
  await new Promise(resolve => setTimeout(resolve, 1000))
}
export default eventHandler((event) => {
  event.waitUntil(timeConsumingBackgroundTask())
  return 'done'
})
```

Nitro configuration can be set directly through the `nitro` key of `nuxt.config`. The page warns it is an advanced option: custom config can affect production deployments, because the interface might change when Nitro is upgraded in semver-minor Nuxt versions.

## Checked

2026-11-08. Read in full from the nuxt/nuxt docs repository: docs/2.directory-structure/1.server.md (Forwarding Context and Headers, Awaiting Promises After Response, Nitro Config sections). Confirmed: all behaviour and code above. Removed: the claim about serverless/edge targets (the page only mentions runtime providers) and the invented Verify step.

Method: documentation only; no commands were run.
