---
id: computing-software.web-development.directus.sdk-client-composables
name: sdk-client-composables
category: computing-software
field: web-development
product: directus
tags: [sdk-composables, directus-sdk, sdk-typescript-schema, sdk-custom-endpoint]
level: practitioner
status: docs-checked
description: "Build a Directus SDK client from composables (rest, graphql, authentication, realtime, staticToken), type it with a Schema and call custom endpoints."
sources:
  - https://raw.githubusercontent.com/directus/docs/main/content/guides/04.connect/6.sdk.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```bash
npm install @directus/sdk
```

The client starts empty; add features with `.with()`:
- `rest()` adds `.request()`
- `graphql()` adds `.query()`
- `authentication()` adds `.login()`, `.logout()`, `.refresh()` and token handling
- `realtime()` adds `.connect()`, `.subscribe()`, `.sendMessage()`, `.onWebSocket()` and reconnect logic
- `staticToken()` adds `.setToken()` and `.getToken()`

```ts
import { createDirectus, rest, readItems } from '@directus/sdk';
interface Schema { posts: { id: number; title: string }[] }
const directus = createDirectus<Schema>('https://directus.example.com').with(rest());
const posts = await directus.request(readItems('posts', {
  filter: { status: { _eq: 'published' } }, sort: ['-date_created'], fields: ['id', 'title'], limit: 3,
}));
```

Without a `Schema` type parameter you lose type hints and completion.

Custom endpoint: `directus.request(customEndpoint<Out>({ path: '/custom/endpoint', method: 'GET' }))`; in plain JS return `{ path, method }` from a function.

GraphQL: `createDirectus(url).with(graphql())` then call `directus.query()` with a GraphQL query string.

## Checked

2026-11-04: confirmed against the Directus docs SDK page: install, composable table, Schema typing, readItems example, customEndpoint, GraphQL usage. Replaced an escaped-backtick snippet with plain wording and removed the unsupported verify line.

Method: documentation only; no commands were run.
