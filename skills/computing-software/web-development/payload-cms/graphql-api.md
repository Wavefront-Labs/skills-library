---
id: computing-software.web-development.payload-cms.graphql-api
name: graphql-api
category: computing-software
field: web-development
product: payload-cms
tags: [graphql, graphql-playground, maxcomplexity, introspection]
level: practitioner
status: docs-checked
description: "Use the generated GraphQL API: query and mutation names per collection, and GraphQL config options such as maxComplexity."
sources:
  - https://payloadcms.com/docs/graphql/overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# GraphQL API

Goal: query Payload with GraphQL (install the `graphql` package).

The GraphQL endpoint is `/api/graphql` by default and the playground is at `/api/graphql-playground` (configurable under `routes`; the Admin Panel page lists the route settings as `/graphql` and `/graphql-playground` without the `/api` prefix). For a collection with slug `public-users`:

- Queries: `PublicUser` (find by ID), `PublicUsers` (find), `countPublicUsers`, `mePublicUser`.
- Mutations: `createPublicUser`, `updatePublicUser`, `deletePublicUser`, plus auth: `loginPublicUser`, `logoutPublicUser`, `refreshTokenPublicUser`, `forgotPasswordPublicUser`, `resetPasswordPublicUser`, `unlockPublicUser`, `verifyPublicUser`. The authentication operations page names the verify and logout operations differently (`verifyEmail[label]`, `logoutUser`), so confirm in the playground Schema.

Root `graphQL` options: `mutations`, `queries`, `maxComplexity`, `disablePlaygroundInProduction` (default true), `disableIntrospectionInProduction` (default true), `disable`, `validationRules`.

```ts
export default buildConfig({
  graphQL: { maxComplexity: 1000, disable: false },
})
```

Per-collection `graphQL` options include `singularName`, `pluralName`, `disableQueries`, `disableMutations`.

Collection and global queries accept `select: true` to project fields at the database level. File uploads are REST-only. A Global gets a query named after it and an `update<Name>` mutation.

Clients mentioned: `graphql-request` and `@apollo/client`.

Gotcha: changing a field's returned type in a field hook breaks the typed GraphQL schema.

The playground is on by default in development and off in production; use its Schema and Docs buttons to see the generated names.

## Checked

2026-11-04. Read graphql/overview, configuration/collections (graphQL options) and authentication/operations in the payloadcms/payload docs. Confirmed: options table and defaults, query and mutation names, per-collection options, field hook typing warning. Fixed: the default endpoint is /api/graphql, not /graphql. Flagged: the operations page and GraphQL page disagree on verify and logout names. Removed: the verify step.
Method: documentation only; no commands were run.
