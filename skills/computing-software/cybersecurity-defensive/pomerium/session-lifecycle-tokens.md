---
id: computing-software.cybersecurity-defensive.pomerium.session-lifecycle-tokens
name: session-lifecycle-tokens
category: computing-software
field: cybersecurity-defensive
product: pomerium
tags: [session-lifecycle, id-token-refresh, oauth-access-token, relying-party, refresh-session-at-id-token-expiration]
level: advanced
status: docs-checked
description: "Trace the Pomerium login flow and session data, how ID and access tokens are refreshed, and the runtime flag that controls ID token refresh."
sources:
  - https://raw.githubusercontent.com/pomerium/documentation/main/content/docs/internals/sessions.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Login flow**
1. User requests a route on the Proxy.
2. Authorize checks the policy; if sign-in is needed it redirects to Authenticate.
3. Authenticate runs OIDC login with the IdP.
4. IdP redirects back; Authenticate verifies, creates a session in the Databroker and sets a cookie referencing it.
5. User returns to the original route; Authorize re-evaluates with the session loaded from the Databroker.

**Tokens**: Pomerium is a Relying Party. The ID token is a point-in-time authentication event; policy can use its claims via `claim`. The OAuth access token queries UserInfo and represents an active IdP session; Pomerium refreshes it periodically and ends the session if refresh fails. UserInfo is also read periodically so IdP changes apply without a new login.

**Refresh timing**: shortly before the access token expires; from v0.31 also shortly before the ID token expires, if the IdP issues a new ID token on refresh. This matters only when forwarding the ID token upstream with Set Request Headers. Revert with the runtime flag `refresh_session_at_id_token_expiration` set to `false`.

**Session data**: `id`, `user_id`, `issued_at`, `expires_at` (default 14 hours after creation), `id_token`, `oauth_token`, `claims`. One user can have several sessions. Directory data (from a directory provider) adds group IDs and display names.

Tune lifetime with `cookie_expire` (see cookie-settings).

## Checked

2026-11-04. Confirmed against the Sessions page: login flow steps, token roles, refresh scheduling and v0.31 change, refresh_session_at_id_token_expiration flag, session fields and 14 hour default expiry, directory data, cookie_expire. Nothing removed.

Method: documentation only; no commands were run.
