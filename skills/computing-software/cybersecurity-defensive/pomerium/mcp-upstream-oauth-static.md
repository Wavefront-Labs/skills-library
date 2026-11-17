---
id: computing-software.cybersecurity-defensive.pomerium.mcp-upstream-oauth-static
name: mcp-upstream-oauth-static
category: computing-software
field: cybersecurity-defensive
product: pomerium
tags: [upstream-oauth2, pre-registered-credentials, oauth-callback, mcp-allowed-as-metadata-domains, client-secret]
level: advanced
status: docs-checked
description: "Configure Pomerium MCP upstream_oauth2 with pre-registered client credentials so MCP servers get an upstream access token without clients seeing it."
sources:
  - https://raw.githubusercontent.com/pomerium/documentation/main/content/docs/capabilities/mcp/mcp-upstream-oauth.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Use when the upstream authorization server needs manual app registration and supports neither CIMD nor DCR. MCP clients hold only a Pomerium-issued token; upstream credentials stay inside Pomerium.

Config: add `upstream_oauth2` under the route's `mcp.server` with `client_id`, `client_secret`, `scopes`, `endpoint` (`auth_url`, `token_url`) and optional `authorization_url_params` (e.g. `access_type`, `prompt`). Supplying credentials skips automatic registration; also supplying endpoints skips RFC 9728 discovery. Pomerium can still discover endpoints from the upstream if you omit `endpoint`.

Steps:
1. Register an OAuth app at the provider (GitHub: Settings, Developer settings, OAuth Apps, New). Set the callback to `https://<route-from-domain>/.pomerium/mcp/client/oauth/callback`, and note the Client ID and Secret.
2. Add the `upstream_oauth2` block to the route.
3. Run the MCP server. It receives the upstream access token as `Authorization: Bearer` on every proxied request.
4. Connect a client: sign in to Pomerium, then authorize with the provider.

Docs list GitHub (`https://github.com/login/oauth/authorize`, `.../access_token`), Google and Notion endpoints.

Caveat: a third-party auth domain not derivable from the route (e.g. `accounts.google.com`) must be added to `mcp_allowed_as_metadata_domains`. The `auth_style` option is in the MCP Full Reference.

## Checked

2026-11-04. Read the MCP + Upstream OAuth page: when to use pre-registered credentials, config keys, discovery-skipping rules, GitHub setup steps, callback path, bearer token behaviour, provider endpoints and the allowed-domains caveat confirmed. Nothing removed.

Method: documentation only; no commands were run.
