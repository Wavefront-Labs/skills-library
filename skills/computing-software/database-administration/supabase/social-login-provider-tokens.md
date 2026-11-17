---
id: computing-software.database-administration.supabase.social-login-provider-tokens
name: social-login-provider-tokens
category: computing-software
field: database-administration
product: supabase
tags: [social-login, oauth, provider-tokens, refresh-token, custom-oidc]
level: practitioner
status: docs-checked
description: "Supabase social login: supported providers, custom OAuth or OIDC providers, and why provider tokens are not refreshed or stored."
sources:
  - https://supabase.com/docs/guides/auth/social-login
  - https://supabase.com/docs/guides/local-development/cli/config
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: add OAuth sign-in and handle the provider's own tokens correctly.

Each listed provider has its own setup guide. The listed providers are Apple, Azure, Bitbucket, Discord, Facebook, Figma, GitHub, GitLab, Google, Kakao, Keycloak, LinkedIn, Notion, Slack, Spotify, Twitter, Twitch, WorkOS and Zoom. Providers not on the list can be added through the Custom OAuth/OIDC Providers guide, which works with any OAuth2 or OIDC-compatible provider.

Local config uses `[auth.external.<provider>]` with `enabled`, `client_id`, `secret` (for example `env(SUPABASE_AUTH_EXTERNAL_<PROVIDER>_SECRET)`), `redirect_uri` and optional `skip_nonce_check`.

Provider tokens:
- Supabase Auth does not refresh provider tokens. The application must use the provider's refresh token to get a new access token.
- If no refresh token comes back, either the provider does not issue them or you must request additional scopes.
- Provider tokens are intentionally not stored in the project's database. If they must be used outside the browser that completed the OAuth flow, send them to a trusted server you control.

## Checked

Confirmed against the social login page: the 19 listed providers, custom OAuth/OIDC providers for unlisted ones, provider token refresh and storage rules. Confirmed against the CLI config reference: auth.external provider enabled, client_id, secret default, redirect_uri and skip_nonce_check keys. Removed the guide URL pattern, the local callback URL, and the local development overview source, none of which was confirmed.

Method: docs-checked 2026-11-09 against supabase.com/docs/guides/auth/social-login and supabase.com/docs/guides/local-development/cli/config (HTML converted to text and read).
