---
id: computing-software.web-development.payload-cms.hook-context
name: hook-context
category: computing-software
field: web-development
product: payload-cms
tags: [hook-context, context, infinite-loop, req-context]
level: advanced
status: docs-checked
description: "Share data between hooks with context and prevent infinite loops when an afterChange hook updates the same collection."
sources:
  - https://payloadcms.com/docs/hooks/context
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Hook context

Goal: pass data between hooks and avoid recursion.

`context` is an object shared by all hooks during one request. Use it to pass data between hooks, prevent infinite loops, pass data in from the Local API, or from hooks to custom endpoints and middleware.

Pass data between hooks:

```ts
hooks: {
  beforeChange: [async ({ context, data }) => {
    context.customerData = await fetchCustomerData(data.customerID)
    return { ...data, name: context.customerData.name }
  }],
  afterChange: [async ({ context }) => {
    if (context.customerData.contacted === false) { /* ... */ }
  }],
}
```

Prevent an infinite loop: updating the same collection from `afterChange` triggers the hook again. Set a flag in the nested call:

```ts
afterChange: [async ({ context, doc, req }) => {
  if (context.triggerAfterChange === false) return
  await req.payload.update({
    collection: 'customers',
    id: doc.id,
    data: { /* ... */ },
    context: { triggerAfterChange: false },
  })
}]
```

Pass context from the Local API: `payload.create({ collection, data, context: { source: 'seed' } })`; hooks read it from `context` and `req.context`.

The default context type is `{ [key: string]: unknown }`; add typed keys by augmenting `RequestContext` with `declare module 'payload'`.

## Checked

2026-11-04. Read hooks/context in the payloadcms/payload docs. Confirmed: the four use cases, both examples, req.context, TypeScript augmentation. Note: the page's fixed example references an undefined contextHooksSlug and data, so the sketch above is simplified rather than copied. Removed: the verify step.
Method: documentation only; no commands were run.
