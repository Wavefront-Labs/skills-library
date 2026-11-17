---
id: computing-software.rpa-and-low-code.n8n.deployment-env-vars
name: deployment-env-vars
category: computing-software
field: rpa-and-low-code
product: n8n
tags: [n8n, environment-variables, proxy, n8n-host, encryption-key, proxy-hops]
level: practitioner
status: docs-checked
description: "Key n8n deployment variables: host, port, protocol, editor base URL, outbound proxy precedence, user agent, encryption key, public API toggles, push backend and proxy hops."
sources:
  - https://docs.n8n.io/deploy/host-n8n/configure-n8n/basic-configuration/use-environment-variables/deployment
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: set the instance's identity and network behaviour correctly. Defaults in brackets.

## Where it listens
`N8N_HOST` (`localhost`), `N8N_PORT` (5678), `N8N_LISTEN_ADDRESS` (`::`), `N8N_PROTOCOL` (`http` or `https`; with https also `N8N_SSL_KEY` and `N8N_SSL_CERT`), `N8N_PATH` (`/`). Combining `N8N_PATH` with a reverse proxy causes folder navigation issues: use a subdomain such as `n8n.example.com` instead. `N8N_EDITOR_BASE_URL` is the public editor URL, also used in emails and as the SAML redirect URL. `N8N_PROXY_HOPS` (0) is the number of reverse proxies in front of n8n.

## Outbound proxy
`HTTP_PROXY`, `HTTPS_PROXY`, `ALL_PROXY` (fallback when the specific ones are absent), and `NO_PROXY` (comma-separated bypass list). The `proxy-from-env` package gives lowercase variants (`http_proxy`) precedence over uppercase when both exist. `N8N_ENFORCE_GLOBAL_USER_AGENT=true` replaces the bare `n8n` User-Agent with an RFC-compliant `Mozilla/5.0 (compatible; n8n/<version>; +https://n8n.io/)` so WAFs stop blocking requests; `N8N_GLOBAL_USER_AGENT_VALUE` overrides it with your own string.

## Secrets and features
`N8N_ENCRYPTION_KEY` defaults to a random key generated on first launch. `N8N_ENV_FEAT_ENCRYPTION_KEY_ROTATION` must be set on all instances (main and workers) and is a one-way change, so back up the database first. `N8N_USER_FOLDER` sets where `.n8n` is created.

## Misc
`N8N_PUSH_BACKEND` (`websocket` or `sse`), `N8N_PUBLIC_API_DISABLED`, `N8N_PUBLIC_API_SWAGGERUI_DISABLED`, `N8N_PUBLIC_API_ENDPOINT` (`api`), `N8N_GRACEFUL_SHUTDOWN_TIMEOUT` (30 s), `N8N_TEMPLATES_ENABLED` (true), `N8N_TEMPLATES_HOST`, `N8N_DISABLE_UI`, `N8N_REINSTALL_MISSING_PACKAGES`. Setting `N8N_DIAGNOSTICS_ENABLED=false` means Ask AI in the Code node cannot be enabled. MCP and OAuth server endpoints are rate limited per IP per 5 minutes (`N8N_MCP_SERVER_RATE_LIMIT` 100, `N8N_OAUTH_SERVER_TOKEN_RATE_LIMIT` 20).

## Checked

2026-11-03. Read against the official n8n documentation pages:
- https://docs.n8n.io/deploy/host-n8n/configure-n8n/basic-configuration/use-environment-variables/deployment

Confirmed: parameter names, defaults, limits, commands and behaviour in this skill match those pages. Nothing removed; every concrete claim matched the page.

Method: documentation only; no commands were run.
