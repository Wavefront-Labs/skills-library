---
id: computing-software.web-development.payload-cms.hooks-overview
name: hooks-overview
category: computing-software
field: web-development
product: payload-cms
tags: [hooks, root-hooks, aftererror, awaited-hooks]
level: practitioner
status: docs-checked
description: "Choose between root, collection, global and field hooks, understand awaited vs non-blocking behaviour, afterError and APIError messages."
sources:
  - https://payloadcms.com/docs/hooks/overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Hooks overview

Goal: pick the right hook type and avoid blocking pitfalls.

Four types: Root Hooks, Collection Hooks, Global Hooks and Field Hooks. (Payload also ships React hooks for the Admin Panel; they are a different thing.)

Root hook example - the only root hook is `afterError`:

```ts
export default buildConfig({
  hooks: {
    afterError: [async ({ error }) => { /* log to a third party */ }],
  },
})
```

Awaited vs non-blocking: if a hook returns a Promise (including any `async` function) Payload waits for it. A hook that returns nothing is fire-and-forget. Declaring `async` does not make a function synchronous; it makes Payload await it.

Return a custom error from a hook with `APIError`:

```ts
import { APIError } from 'payload'
throw new APIError('You have sent too many requests', 429)
```

Hooks run only on the server and are excluded from the client bundle, so sensitive logic is safe there.

Performance tips from the docs: keep hooks cheap, share data through hook context, and offload long-running work that does not affect the response to the jobs queue.

`afterError` receives `error`, `context`, `req`, `graphqlResult` (GraphQL), `collection` and `result` (REST). Hooks that return Promises run in series at the same stage. `beforeChange` also runs during on-demand validation, so skip side effects when `operation === 'validate'`.

## Checked

2026-11-04. Read hooks/overview in the payloadcms/payload docs. Confirmed: four hook types, afterError as the only root hook, awaited versus non-blocking, server-only execution, APIError, performance tips. Added: afterError arguments and validate caveat. Removed: the console.log verify step.
Method: documentation only; no commands were run.
