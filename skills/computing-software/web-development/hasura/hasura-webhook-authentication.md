---
id: computing-software.web-development.hasura.hasura-webhook-authentication
name: hasura-webhook-authentication
category: computing-software
field: web-development
product: hasura
tags: [hasura, authentication, webhook, auth-hook, session-variables]
level: practitioner
status: docs-checked
description: "Authenticate requests through your own HTTP webhook with HASURA_GRAPHQL_AUTH_HOOK, in GET or POST mode, returning session variables or a 401."
sources:
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/auth/authentication/webhook.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: delegate authentication to a service you control.

Prerequisite per the docs: secure the GraphQL endpoint first, otherwise webhook mode does not take effect.

Configure (flag or env var; the value is the webhook endpoint):
- `--auth-hook` / `HASURA_GRAPHQL_AUTH_HOOK=<WEBHOOK_URL>`
- `--auth-hook-mode` / `HASURA_GRAPHQL_AUTH_HOOK_MODE`: GET (default) or POST

Modes per the docs:
- GET: Hasura forwards all client headers except a listed set (for example Content-Length, Content-Type, User-Agent, Host, Origin, Cache-Control).
- POST: the webhook receives a JSON body with the client `headers` plus the `request` (variables, operationName, query).

Webhook response:
- 200 with the session variables as a JSON body, at least `X-Hasura-Role`, for example `{ "X-Hasura-User-Id": "25", "X-Hasura-Role": "user" }`. Unlike JWT mode, `X-Hasura-Allowed-Roles` and `X-Hasura-Default-Role` are not needed. Values should be strings.
- 401 to deny the request.
- Anything other than 200 or 401 raises a 500 Internal Server Error in Hasura.
- To use the unauthorized role, return 200 with `X-Hasura-Role` set to that role's name.

Expiry and caching: a `Cache-Control` (for example `max-age=600`) or `Expires` field (format `%a, %d %b %Y %T GMT`) in the response body sets when a websocket connection is re-authenticated. The same fields drive webhook auth caching, which needs v2.22.0 or later; it is available on Hasura Cloud without configuration, and self-hosted EE needs a Redis instance.

If the container runs in Docker, the webhook must be reachable from it.

Gotcha: the configured webhook is ignored when the `X-Hasura-Admin-Secret` header is present and admin access is granted.

## Checked
2026-11-07. Read in full the single cited page (webhook.mdx, GitHub file view; no snippet files, only Thumbnail and ProductBadge components). Linked pages (server options, securing the endpoint) were not read.
Confirmed: flags and env vars, GET default, forwarded-header list (partial list quoted), POST body shape, response rules, 401/500 behaviour, unauthorized role, expiry and caching fields and version/Redis notes, admin secret note.
Removed: "admin secret must also be set" (page says to secure the endpoint), `HASURA_GRAPHQL_PRESERVE_401_ERRORS` and the HTTP 200 error-body claim (not on the page), the claim that Cache-Control/Expires are HTTP headers (the page puts them in the body), and the invented Verify step.
Method: documentation only; no commands were run.
