---
id: computing-software.web-development.payload-cms.access-control-overview
name: access-control-overview
category: computing-software
field: web-development
product: payload-cms
tags: [access-control, default-access, baseaccess, overrideaccess]
level: practitioner
status: docs-checked
description: "Understand Payload access control scopes (collection, global, field), the default logged-in-admin rule, baseAccess, and Local API overrideAccess."
sources:
  - https://payloadcms.com/docs/access-control/overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Access control overview

Goal: know how Payload decides who may do what.

Access functions are scoped to an operation (`create`, `read`, `update`, `delete`, plus `validate`) and are evaluated on the server. There are three types: collection, global and field access control.

Default behaviour: Payload secures data behind authentication. The default function returns true only when a user exists and belongs to the admin user collection:

```ts
const defaultPayloadAccess = ({ req: { payload, user } }) =>
  Boolean(user) && user.collection === payload.config.admin.user
```

So a second auth-enabled collection does not automatically get access to everything.

`baseAccess` adds an extra constraint to standard collection and global operations:

```ts
export default buildConfig({
  baseAccess: {
    collections: {
      delete: ({ req, slug }) => slug === 'public-posts' || req.user?.role === 'admin',
    },
    globals: {
      update: ({ req, slug }) => slug === 'public-settings' || req.user?.role === 'admin',
    },
  },
})
```

`baseAccess` is combined with each collection or global access function (both must allow the operation). Its `create` and `admin` entries must return booleans only. It does not apply to field access, custom endpoints or direct database calls.

Local API calls respect access control based on the passed `user` unless you pass `overrideAccess: true`.

The `validate` operation (on-demand validation) falls back to the `update` function unless set explicitly.

`GET /api/access` while logged in returns the resolved permissions. That operation passes undefined `id`, `data` and `doc` to access functions and does not run any Where query they return, so write functions that tolerate missing arguments.

## Checked

2026-11-04. Read access-control/overview and authentication/operations (the Access operation) in the payloadcms/payload docs. Confirmed: scopes, default admin-collection rule, baseAccess shape, validate falling back to update, overrideAccess behaviour. Removed: the claim that functions run for every request (the page only says they run on the server). Added: baseAccess limits and Access operation caveats.
Method: documentation only; no commands were run.
