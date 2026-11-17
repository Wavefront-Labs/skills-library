---
id: computing-software.web-development.payload-cms.auth-custom-strategies
name: auth-custom-strategies
category: computing-software
field: web-development
product: payload-cms
tags: [custom-strategies, auth-strategy, authenticate, disable-local-strategy]
level: advanced
status: docs-checked
description: "Add a custom authentication strategy to an auth collection with name and authenticate, optionally disabling local email and password login."
sources:
  - https://payloadcms.com/docs/authentication/custom-strategies
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Custom auth strategies

Goal: authenticate requests by your own mechanism (since 3.0 Passport is not used).

A strategy has a `name` and an `authenticate` function that receives:

- `headers` - incoming request headers
- `payload` - the Payload instance
- `canSetHeaders` - whether response headers can be set
- `isGraphQL` - true inside the GraphQL endpoint (default `false`)
- `req` - the request, when available

`headers`, `payload` and `canSetHeaders` are required properties. It returns `{ user }` (a Payload user document, with optional `responseHeaders`) or `{ user: null }`.

```ts
export const Users: CollectionConfig = {
  slug: 'users',
  auth: {
    disableLocalStrategy: true,   // only if the custom one replaces email/password
    strategies: [
      {
        name: 'my-strategy',
        authenticate: async ({ payload, headers }) => {
          const key = headers.get('x-custom-key')
          if (!key) return { user: null }
          const found = await payload.find({
            collection: 'users', where: { customKey: { equals: key } }, limit: 1, overrideAccess: true,
          })
          return { user: found.docs[0] ? { collection: 'users', ...found.docs[0] } : null }
        },
      },
    ],
  },
  fields: [{ name: 'customKey', type: 'text' }],
}
```

Gotcha: strategy changes need a full server restart; they are not hot-reloaded.

## Checked

2026-11-04. Read authentication/custom-strategies in the payloadcms/payload docs. Confirmed: authenticate arguments, return shape, disableLocalStrategy, restart requirement. Changed: example find now passes overrideAccess: true as the docs example does; removed the unconfirmed default for canSetHeaders and the /me verify step.
Method: documentation only; no commands were run.
