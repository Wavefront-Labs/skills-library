---
id: computing-software.web-development.node-express.graphql-server-with-dataloader
name: graphql-server-with-dataloader
category: computing-software
field: web-development
product: node-express
tags: [graphql-server, dataloader, graphql-yoga, apollo-server, query-complexity, api-design]
level: advanced
status: verified
description: "Production GraphQL server in Node: resolvers, per-request DataLoader for N+1, auth in context, depth/complexity limits, error masking, persisted queries."
sources:
  - https://the-guild.dev/graphql/yoga-server/docs
  - https://github.com/graphql/dataloader
  - https://escape.tech/graphql-armor/docs/getting-started
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GraphQL server with DataLoader

## 1. Server
```ts
import { createSchema, createYoga } from "graphql-yoga";
const yoga = createYoga({
  schema: createSchema({ typeDefs, resolvers }),
  context: async ({ request }) => ({ user: await authenticate(request), loaders: createLoaders() }),
  maskedErrors: true,             // unexpected errors become "Unexpected error." to clients
});
app.use(yoga.graphqlEndpoint, yoga);
```
Ran on graphql-yoga 5.24.6, graphql 16.14.2, dataloader 2.2.3, Express 5.3.0: mounting `app.use(yoga.graphqlEndpoint, yoga)` served `/graphql`; with `maskedErrors: true` a resolver that threw `secret db password` reached the client as `Unexpected error.` (code `INTERNAL_SERVER_ERROR`). Apollo Server is the main alternative; in Apollo Server 5 `expressMiddleware` is no longer inside `@apollo/server` but in `@as-integrations/express5` (or `@as-integrations/express4`; migration guide).

## 2. N+1 and DataLoader
```ts
import DataLoader from "dataloader";
function createLoaders() {
  return {
    userById: new DataLoader<string, User | null>(async ids => {
      const rows = await db.user.findMany({ where: { id: { in: [...ids] } } });
      const byId = new Map(rows.map(r => [r.id, r]));
      return ids.map(id => byId.get(id) ?? null);      // same order and length as ids
    }),
  };
}
const resolvers = { Post: { author: (post, _, ctx) => ctx.loaders.userById.load(post.authorId) } };
```
Create loaders **per request** (caching across users leaks data and serves stale results). Fetching 50 posts then 50 authors becomes 2 queries (ran: 50 posts with authors made 1 author query; two requests made 2, so loaders are not shared across requests). A batch function returning the wrong number of values makes every `load()` reject with "did not return a Promise of an Array of the same length as the Array of keys".

## 3. Authorization
Authenticate in context; authorise in resolvers or a shared business layer per field/object (`post.visibility`, tenant checks). Directive-based (`@auth`) or graphql-shield are options, but object-level checks still belong in data access code.

## 4. Abuse protection
- Depth, alias, token and cost limits (GraphQL Armor plugins for Yoga/Apollo, `graphql-query-complexity`). Ran `EnvelopArmor().protect()` plugins on Yoga with @escape.tech/graphql-armor 3.2.0: a 3-level query ran, a 20-level query was rejected (by the default cost limit of 5000 before the depth limit).
- Persisted queries / trusted documents in production so only your clients' operations run.
- Pagination with enforced `first <= 100` (Relay connection pattern).
- Consider disabling introspection publicly for private APIs (not a security boundary on its own).
- Timeouts and rate limits per user, weighted by query cost.

## 5. Operate
Tracing (OpenTelemetry plugin), per-operation metrics by `operationName`, schema checks in CI (`graphql-inspector diff old.graphql new.graphql`, ran with @graphql-inspector/cli 7.0.2: reported "Field b was removed from object type Query" and "Detected 1 breaking change"), `@deprecated` fields with usage tracking before removal.

## Verify
- [ ] Query listing 50 posts with authors issues 2 DB queries (log/trace); a 20-level deep query is rejected; internal errors show masked messages.
