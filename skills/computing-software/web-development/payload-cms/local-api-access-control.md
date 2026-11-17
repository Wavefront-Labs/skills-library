---
id: computing-software.web-development.payload-cms.local-api-access-control
name: local-api-access-control
category: computing-software
field: web-development
product: payload-cms
tags: [overrideaccess, local-api-permissions, user-scoped-queries, trusted-server]
level: practitioner
status: docs-checked
description: "Decide between overrideAccess true and false in Local API calls and pass the acting user to enforce permissions."
sources:
  - https://payloadcms.com/docs/local-api/access-control
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Local API access control

Goal: avoid accidentally bypassing or enforcing permissions.

- `overrideAccess: false` respects access control. Pass the authenticated `user` when acting on their behalf.
- `overrideAccess: true` skips access control and runs with full permissions.

```ts
const authed = await payload.create({
  collection: 'posts',
  overrideAccess: false,
  user,                 // whose permissions to check
  data: { title: 'Hello' },
})

const seeded = await payload.create({
  collection: 'users',
  overrideAccess: true,
  data: { email: 'test@test.com', password: 'test' },
})
```

Choose `false` for anything driven by an end user (server functions, route handlers); choose `true` for seeds, migrations and system jobs. Forgetting `user` with `overrideAccess: false` behaves like an anonymous request.

Get the current user with `payload.auth({ headers })`.

Verify: the same call with a low-privilege user is rejected.

## Checked

2026-11-04. Read local-api/access-control, local-api/overview and local-api/server-functions. Confirmed: overrideAccess false respects access control and true skips it, passing user to act on their behalf, omitting user evaluating as an anonymous request, the use cases for each value, and payload.auth({ headers }) to get the current user.
Method: documentation only; no commands were run.
