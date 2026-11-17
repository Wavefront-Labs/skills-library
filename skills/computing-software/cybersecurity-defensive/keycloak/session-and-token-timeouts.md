---
id: computing-software.cybersecurity-defensive.keycloak.session-and-token-timeouts
name: session-and-token-timeouts
category: computing-software
field: cybersecurity-defensive
product: keycloak
tags: [cybersecurity-defensive, keycloak, session-idle, sso-session-max, access-token-lifespan, remember-me]
level: practitioner
status: docs-checked
description: "Tune Keycloak realm SSO session idle and max, client session, offline session and token lifespans, and the two-minute idle window."
sources:
  - https://github.com/keycloak/keycloak/blob/main/docs/documentation/server_admin/topics/sessions/timeouts.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# session and token timeouts
Session, cookie and token timeouts are set in *Realm settings* on the *Sessions* and *Tokens* tabs.

Sessions tab:
- **SSO Session Idle**: OIDC clients only. Inactivity longer than this invalidates the user session; the timer resets when clients request authentication or send a refresh token request.
- **SSO Session Max**: maximum time before a user session expires.
- **SSO Session Idle Remember Me / SSO Session Max Remember Me**: only available when Remember me is enabled; users who tick Remember Me get these longer values; if not greater than zero they use the standard SSO Session Idle / Max.
- **Client Session Idle / Max**: per client session; they never affect the single parent SSO user session. They should be shorter than the SSO values and can be overridden per client in the client's *Advanced Settings* tab; zero means use the SSO value.
- **Offline Session Idle**; **Offline Session Max Limited** (if Enabled, Offline Session Max applies regardless of activity; if Disabled, offline sessions expire only by idle); **Offline Session Max**; **Client Offline Session Max** (overridable per client).
- **Login timeout**: total time a login may take. **Login action timeout**: maximum time on any one page during authentication.

Tokens tab: Default Signature Algorithm, Revoke Refresh Token, **Access Token Lifespan**, Access Token Lifespan For Implicit Flow, Client login timeout (Authorization Code Flow), User-Initiated Action Lifespan (keep short), Default Admin-Initiated Action Lifespan (keep long; an administrator can override it), and independent timeouts for Email Verification, IdP account email verification, Forgot password and Execute actions.

Idle window: when persistent user sessions are not active, idle timeouts get an extra two-minute window, so a 30 minute setting expires after 32 minutes. This covers cluster and cross-data-center cases where a refresh on one node has not yet reached the others.

## Checked
2026-11-03. Confirmed against server_admin/topics/sessions/timeouts.adoc (all labels, remember-me fallback, client overrides, two-minute window and its persistent-sessions condition). Removed: generic lifespan advice, the "no max means indefinite" and "issued tokens not shortened" gotchas and the invented Verify step, none of which are on the page.
Method: documentation only; no commands were run.
