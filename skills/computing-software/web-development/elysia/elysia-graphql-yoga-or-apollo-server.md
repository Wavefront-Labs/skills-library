---
id: computing-software.web-development.elysia.elysia-graphql-yoga-or-apollo-server
name: elysia-graphql-yoga-or-apollo-server
category: computing-software
field: web-development
product: elysia
tags: [graphql, yoga, apollo, plugin]
level: practitioner
status: docs-checked
description: "Mount a GraphQL endpoint on Elysia with @elysia/graphql-yoga or @elysia/apollo, including typed resolvers and request context."
sources:
  - https://elysiajs.com/plugins/graphql-yoga.html
  - https://elysiajs.com/plugins/graphql-apollo.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: serve GraphQL at `/graphql` from an Elysia app.

Option A, GraphQL Yoga: `bun add @elysia/graphql-yoga` (optionally pin peers: `bun add graphql graphql-yoga`).

```typescript
import { Elysia } from 'elysia'
import { yoga } from '@elysia/graphql-yoga'

new Elysia()
    .use(yoga({
        typeDefs: /* GraphQL */ `type Query { hi: String }`,
        resolvers: { Query: { hi: () => 'Hello from Elysia' } }
    }))
    .listen(3000)
```

A GET to `/graphql` in a browser shows GraphiQL. Types for `resolvers` are inferred from `typeDefs` using Mobius. Add custom context with a `context` object; the docs example also adds an empty `useContext(_) {}` because a context given as a function without it fails to infer the context type:

```ts
yoga({ typeDefs, context: { name: 'Mobius' }, useContext(_) {},
  resolvers: { Query: { hi: async (parent, args, context) => context.name } } })
```

Config extends `createYoga` options with `schema` inlined at the root; plugin option `path` defaults to `/graphql`.

Option B, Apollo: `bun add graphql @elysia/apollo @apollo/server`.

```typescript
import { apollo, gql } from '@elysia/apollo'
new Elysia().use(apollo({ typeDefs: gql`type Query { books: [Book] } type Book { title: String }`, resolvers })).listen(3000)
```

`/graphql` shows the Apollo playground. Extra options: `path` (default `/graphql`) and `enablePlayground` (default `process.env.ENV !== 'production'`); the rest is Apollo's ServerRegistration (ApolloServer constructor options).

Apollo context: Elysia uses Web Standard Request/Response, so Express-style `req, res` are undefined. Use the route-style context instead:

```typescript
apollo({ typeDefs, resolvers,
  context: async ({ request }) => ({ authorization: request.headers.get('Authorization') }) })
```

Gotcha: `enablePlayground` keys off `process.env.ENV` (not NODE_ENV), so set `ENV=production` to hide the playground.

## Checked

Checked 2026-11-07 against the Elysia documentation source (plugins/graphql-yoga.html, plugins/graphql-apollo.html); each claim, option name and default was compared with the page text. Removed the invented Verify step and the unread cheat-sheet source.

Method: documentation only; no commands were run.
