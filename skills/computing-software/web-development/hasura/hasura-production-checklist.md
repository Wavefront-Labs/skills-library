---
id: computing-software.web-development.hasura.hasura-production-checklist
name: hasura-production-checklist
category: computing-software
field: web-development
product: hasura
tags: [hasura, security, production, deployment, cors, hardening]
level: intro
status: docs-checked
description: "Harden a Hasura deployment: admin secret, secrets in env vars, row limits, disabled console and dev mode, restricted APIs, CORS, HTTPS and load balancer rules."
sources:
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/deployment/production-checklist.mdx
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/security/security-best-practices.mdx
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/deployment/securing-graphql-endpoint.mdx
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/security/disable-graphql-introspection.mdx
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/deployment/graphql-engine-flags/reference.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: ship a safe production instance.

Checklist items from the docs:
1. Set an admin secret: `HASURA_GRAPHQL_ADMIN_SECRET` (a long string). Hasura Cloud projects get a randomly generated one by default.
2. Move secrets and database connection strings to environment variables.
3. Review the "Schema permissions summary" page (watch roles such as "anonymous"); limit the rows a select can return in the select permission.
4. Set an appropriate `max_connections` (self-hosted) or `total_max_connections` (Cloud).
5. Limit exposed APIs: `HASURA_GRAPHQL_ENABLED_APIS=graphql` (options: metadata, graphql, pgdump, config, metrics; default `metadata,graphql,pgdump,config`). This disables the metadata, pgdump and config APIs; health and version APIs are public and cannot be disabled.
6. Disable the Console: `HASURA_GRAPHQL_ENABLE_CONSOLE=false` or leave it unset (disabled by default).
7. Disable dev mode: `HASURA_GRAPHQL_DEV_MODE=false` or unset (default false). Dev mode includes an `internal` key in the error extensions.
8. Set up an allow-list (it rejects other requests without validating them). The best-practices page also recommends depth, node, rate and time limits for public APIs.
9. Disable schema introspection per role (Console: Security -> Schema Introspection). The page is labelled Cloud Professional and Enterprise Edition; introspection is enabled by default.
10. `HASURA_GRAPHQL_CORS_DOMAIN` with explicit domains (all cross-origin requests are allowed by default in the checklist's wording). A wildcard can be used only in the starting subdomain position, and ports must be explicit.
11. Serve over HTTPS.
12. Load balancer: use Hasura's health endpoint for health checks, idle timeout slightly above the maximum time set in API Limits, no sticky sessions needed.
13. Logging: `HASURA_GRAPHQL_ENABLED_LOG_TYPES` selects log types; enable `query-log` to capture generated SQL (not enabled by default).

Gotcha: `HASURA_GRAPHQL_ADMIN_INTERNAL_ERRORS` defaults to true, so error responses to admin requests include internal information.

## Checked
2026-11-07. Read in full: production-checklist.mdx, security-best-practices.mdx, securing-graphql-endpoint.mdx, disable-graphql-introspection.mdx (GitHub file view; no snippet files). The server flags reference (reference.mdx, about 47k characters) was NOT read in full: only the Admin Internal Errors, Admin Secret, CORS Domain, Dev Mode and Enabled APIs sections were read, to confirm the defaults and options quoted above.
Removed: the claim that introspection settings are stored in `graphql_schema_introspection.yaml` (not stated on the cited pages), the "Enable API limits" wording as a separate checklist item (reworded to what the pages say), and the invented Verify step. Added the flags reference to `sources`.
Method: documentation only; no commands were run.
