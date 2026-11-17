---
id: computing-software.web-development.hasura.hasura-admin-secret-and-rotation
name: hasura-admin-secret-and-rotation
category: computing-software
field: web-development
product: hasura
tags: [hasura, authentication, admin-secret, rotation, security]
level: practitioner
status: docs-checked
description: "Secure Hasura with HASURA_GRAPHQL_ADMIN_SECRET, test roles via headers, and rotate with HASURA_GRAPHQL_ADMIN_SECRETS or multiple JWT secrets."
sources:
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/auth/authentication/admin-secret-access.mdx
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/auth/authentication/multiple-admin-secrets.mdx
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/auth/authentication/multiple-jwt-secrets.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: protect the endpoint and rotate secrets without downtime.

Set the secret with env var `HASURA_GRAPHQL_ADMIN_SECRET` or flag `--admin-secret`. Requests send:

```bash
curl -H 'X-Hasura-Admin-Secret: <ADMIN_SECRET>' <HASURA_URL>/v1/graphql ...
```
The admin secret bypasses permission rules. Adding `X-Hasura-Role` and other X-Hasura user headers alongside it makes Hasura process the request as that role, which is how you test permissions. Never expose the secret in front-end clients.

Rotation (Cloud Professional and Enterprise Edition): `HASURA_GRAPHQL_ADMIN_SECRETS` takes a list of admin secrets; if both it and `HASURA_GRAPHQL_ADMIN_SECRET` are set, only the plural one is used. Procedure from the docs: add the new secret to the list, update applications using the old secret to the new one, then remove the old secret. Self-hosted: use a rolling deployment when changing env vars to avoid downtime.

Multiple JWT secrets (same editions): `HASURA_GRAPHQL_JWT_SECRETS` is a list of JWT configs and wins over `HASURA_GRAPHQL_JWT_SECRET` if both are set. Tokens are matched on the `issuer` field (or an absent issuer); with no match the unauthenticated flow runs, and if several tokens match an error is raised because the token is ambiguous.

Gotcha: the plural variables are documented only for Cloud Professional and Enterprise Edition.

## Checked

2026-11-04. Confirmed against the cited pages: admin-secret-access, multiple-admin-secrets and multiple-jwt-secrets pages plus the flags reference (`--admin-secret`). Removed or corrected: the Community Edition claim reworded to what the pages state, and the Verify step.

Method: documentation only; no commands were run.
