---
id: computing-software.web-development.hasura.hasura-unauthorized-role
name: hasura-unauthorized-role
category: computing-software
field: web-development
product: hasura
tags: [hasura, authentication, unauthenticated-access, anonymous, roles]
level: intro
status: docs-checked
description: "Allow unauthenticated GraphQL access in Hasura by setting HASURA_GRAPHQL_UNAUTHORIZED_ROLE to a role with limited permissions."
sources:
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/auth/authentication/unauthenticated-access.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: let anonymous visitors read a safe subset of data.

With an admin secret configured, Hasura rejects unauthenticated requests by default. To handle them through the permissions system, set the env var (or flag `--unauthorized-role`):

```bash
HASURA_GRAPHQL_UNAUTHORIZED_ROLE=anonymous
```
Then configure permissions for that role the usual way. Unauthenticated requests are then handled as that role instead of being rejected.

What counts as unauthenticated (when the request has no admin secret header):
- no JWT or webhook mode configured: every request;
- JWT mode: a request with no JWT;
- webhook mode: the webhook returns 200 with `{"X-Hasura-Role": "your-unauthorized-role-name"}`. To deny the request, the webhook returns 401; any other non-200 response raises a 500 Internal Server Error in Hasura.

Gotcha: do not use session variables in the unauthorized role's permissions. Session variables can be passed as request headers and are not verified by JWT, webhook or admin secret on these requests, so a user can set any value and bypass the permissions.

## Checked
2026-11-07. Read in full the single cited page (unauthenticated-access.mdx, GitHub file view; no snippet files; the "guide for setting up permissions" link text was not followed).
Confirmed: default rejection with admin secret, env var and flag, definitions of unauthenticated requests, 401/500 webhook behaviour, the session variable warning and its reason.
Removed: "with no permissions queries just fail" and "admin secret and role headers override" (not stated as such), the restart/redeploy and `hasura metadata apply` sentence, the inaccurate reason for the gotcha, the invented Verify step.
Method: documentation only; no commands were run.
