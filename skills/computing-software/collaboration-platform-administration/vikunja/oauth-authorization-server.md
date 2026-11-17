---
id: computing-software.collaboration-platform-administration.vikunja.oauth-authorization-server
name: oauth-authorization-server
category: computing-software
field: collaboration-platform-administration
product: vikunja
tags: [vikunja, oauth-server, pkce-s256, vikunja-redirect-scheme, refresh-token-rotation]
level: advanced
status: docs-checked
description: "Use Vikunja as an OAuth 2.0 authorization server for native apps: mandatory PKCE, vikunja- redirect schemes, the four-step flow and token refresh."
sources:
  - https://raw.githubusercontent.com/go-vikunja/website/main/src/content/docs/integrations/oauth-server.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Available from 2.3.0: Authorization Code flow with mandatory PKCE (S256 only). No client registration; `client_id` is any string, but must match between steps. Redirect URIs must use a custom scheme starting `vikunja-` (for example `vikunja-flutter://callback`); http(s) is not supported. Bodies are JSON, not form-encoded. There is no consent screen.

Flow:
1. Open `https://<host>/oauth/authorize?response_type=code&client_id=..&redirect_uri=..&code_challenge=..&code_challenge_method=S256&state=..`. The frontend logs the user in if needed.
2. Vikunja redirects to `redirect_uri?code=..&state=..`. Verify `state`. The code is single-use and expires in 10 minutes.
3. `POST /api/v1/oauth/token` with JSON `grant_type: authorization_code`, `code`, `client_id`, `redirect_uri`, `code_verifier`. Response has `access_token` (JWT), `token_type`, `expires_in` (from `service.jwtttlshort`, default 600) and `refresh_token`.
4. Refresh: `grant_type: refresh_token` and `refresh_token`. Refresh tokens rotate; the previous one is invalid after use.

PKCE: `code_verifier` is 43 to 128 random characters from `A-Za-z0-9-._~`; `code_challenge` is base64url (no padding) of its SHA-256. Errors come back as HTTP 400 with a `code` field.

## Checked

2026-11-04. Confirmed against the Vikunja OAuth 2.0 Authorization Server page (integrations/oauth-server): 2.3.0 availability, key characteristics, the four-step flow and parameters, code expiry, token response, expires_in from service.jwtttlshort, refresh rotation, PKCE generation and error format. Nothing removed.

Method: documentation only; no commands were run.
