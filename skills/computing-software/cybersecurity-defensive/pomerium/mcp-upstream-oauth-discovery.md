---
id: computing-software.cybersecurity-defensive.pomerium.mcp-upstream-oauth-discovery
name: mcp-upstream-oauth-discovery
category: computing-software
field: cybersecurity-defensive
product: pomerium
tags: [rfc-9728, cimd, dynamic-client-registration, ssrf-allowlist, mcp-allowed-client-id-domains]
level: advanced
status: docs-checked
description: "Let Pomerium auto-discover a third-party MCP server's OAuth requirements (RFC 9728, CIMD, DCR) and set the SSRF allowlists correctly."
sources:
  - https://raw.githubusercontent.com/pomerium/documentation/main/content/docs/capabilities/mcp/mcp-upstream-oauth.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
For third-party hosted MCP servers where you do not register an OAuth app. Define the route's `mcp.server` without `upstream_oauth2`; Pomerium tries CIMD (recommended) first, then DCR.

Discovery flow:
1. Pomerium forwards the request upstream.
2. Upstream replies 401 with `WWW-Authenticate`.
3. Pomerium finds Protected Resource Metadata (PRM) from a `resource_metadata` hint or well-known endpoints.
4. PRM leads to the Authorization Server metadata and scopes.
5. Pomerium identifies itself via CIMD or falls back to DCR.
6. User completes upstream consent.
7. Pomerium caches upstream tokens and injects them later.

Optional route settings: `mcp.server.path` (sub-path for the MCP endpoint) and `mcp.server.authorization_server_url` (HTTPS fallback if PRM discovery fails). The docs example is a Notion route to `https://mcp.notion.com` with path `/mcp`.

Global SSRF allowlists for URLs that come from upstream responses (wildcards supported):
- `mcp_allowed_client_id_domains`: domains that may serve CIMD documents; required when clients use URL-based client IDs.
- `mcp_allowed_as_metadata_domains`: domains Pomerium may contact during discovery (`resource_metadata` URLs and `authorization_servers` entries).

Keep both lists as narrow as your real providers allow.

## Checked

2026-11-04. Read the MCP + Upstream OAuth page: CIMD-then-DCR order, the seven-step flow, optional route settings, Notion example and both SSRF allowlist settings confirmed. The closing advice is a judgement call, not a documented claim.

Method: documentation only; no commands were run.
