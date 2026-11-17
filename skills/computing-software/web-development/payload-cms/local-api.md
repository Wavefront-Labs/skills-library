---
id: computing-software.web-development.payload-cms.local-api
name: local-api
category: computing-software
field: web-development
product: payload-cms
tags: [local-api, getpayload, payload-find, overrideaccess]
level: practitioner
status: docs-checked
description: "Use the Local API (getPayload, find, create, update, delete) with its options such as depth, locale, select, user and overrideAccess."
sources:
  - https://payloadcms.com/docs/local-api/overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Local API

Goal: run Payload operations directly on the server.

```ts
import { getPayload } from 'payload'
import config from '@payload-config'

const payload = await getPayload({ config })
const posts = await payload.find({ collection: 'posts', where: { _status: { equals: 'published' } } })
```

Inside hooks and access control use `req.payload` instead.

Options: `collection`, `data`, `depth`, `locale`, `fallbackLocale`, `select`, `populate`, `overrideAccess`, `overrideLock` (locks ignored by default), `user`, `showHiddenFields`, `pagination`, `context`, `disableErrors` (return null or empty instead of throwing), `disableTransaction`.

Good uses: React Server Components, seed scripts, custom server logic, hooks, and access control. `payload.validate()` validates a candidate document without saving.

Gotcha: where `overrideAccess` is optional it defaults to `false` (access control is respected, and with no `user` the request counts as anonymous); pass `overrideAccess: true` only for trusted server-side work.

Verify: a seed script run with `payload run src/seed.ts` creates documents.

## Checked

2026-11-04. Read local-api/overview, local-api/outside-frameworks and validation/overview. Confirmed: getPayload with the config import, req.payload inside hooks and access control, the local options list (collection, data, depth, locale, fallbackLocale, select, populate, overrideAccess, overrideLock, user, showHiddenFields, pagination, context, disableErrors, disableTransaction), payload.validate(), and the payload run command. Corrected: overrideAccess defaults to false regardless of whether a user is passed.
Method: documentation only; no commands were run.
