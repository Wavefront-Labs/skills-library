---
id: computing-software.web-development.hasura.hasura-session-variables-and-roles
name: hasura-session-variables-and-roles
category: computing-software
field: web-development
product: hasura
tags: [hasura, authorization, roles, session-variables, x-hasura-role]
level: intro
status: docs-checked
description: "Understand Hasura roles and X-Hasura session variables: how roles are created, the built-in admin role, header case rules and how requests pick a role."
sources:
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/auth/authorization/roles-variables.mdx
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/auth/authentication/admin-secret-access.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: use roles and session variables correctly.

Facts from the docs:
- Roles are created "on-the-fly" when a permission is configured for them; defining a permission for a role creates it. Roles are flat (non-hierarchical): each role needs its own access scope.
- By default there is an `admin` role that can perform any operation on any table.
- Hasura publishes a different GraphQL schema for every role.
- Session variables are data returned from your authentication service for each request: encoded in the JWT payload in JWT mode, or returned as a JSON object in the webhook response body in webhook mode. They are case-insensitive and Hasura only has access to those beginning with `X-Hasura-`.
- Use them in permission rules, for example `{ "user_id": { "_eq": "X-Hasura-User-Id" } }`.
- Session variables are expected to be strings in Postgres literal format: an integer array is passed as `"{1,2,3}"`.

Testing a role with the admin secret: if the request has `X-Hasura-Admin-Secret` plus `X-Hasura-Role` and other user headers such as `X-Hasura-User-Id`, Hasura applies the access-control rules of that role instead of admin access.

```bash
curl -H 'X-Hasura-Admin-Secret: <ADMIN_SECRET>' \
     -H 'X-Hasura-Role: user' \
     -H 'X-Hasura-User-Id: 1' \
     -d '{"query":"{ author { id } }"}' <HASURA_URL>/v1/graphql
```
The admin secret alone (no other session variables) bypasses permissions. Never expose it in front-end clients.

Gotcha: Hasura only sees session variables beginning with `X-Hasura-`, so custom ones must use that prefix.

## Checked
2026-11-07. Read in full both cited pages (roles-variables.mdx and admin-secret-access.mdx; GitHub file view, no snippet files, only Thumbnail, Tabs and TabItem components). Pages linked from them were not read.
Confirmed: every bullet above.
Removed: the claim that `X-Hasura-Role` must be in `x-hasura-allowed-roles` with a default role fallback (that lives on the JWT page, not read for this skill), "headers when using the admin secret" as a session-variable source, and the invented Verify step. Added the admin-secret page to `sources` for the curl example.
Method: documentation only; no commands were run.
