---
id: computing-software.cybersecurity-defensive.keycloak.offline-tokens-and-offline-access
name: offline-tokens-and-offline-access
category: computing-software
field: cybersecurity-defensive
product: keycloak
tags: [cybersecurity-defensive, keycloak, offline-token, offline-access, refresh-token, revoke-refresh-token]
level: practitioner
status: docs-checked
description: "Control Keycloak offline tokens: request scope, lifetime, idle limits, per-client overrides, one-time use and revocation."
sources:
  - https://github.com/keycloak/keycloak/blob/main/docs/documentation/server_admin/topics/sessions/offline.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# offline tokens and offline access
With offline access the client asks for an offline token instead of a refresh token (add `scope=offline_access` to the authorization request) and persists it itself, to get new access tokens later, even after the user logs out. Direct Access Grant and Service Accounts also support offline tokens if the request body includes `scope=offline_access`.

An offline token is not subject to the *SSO Session Idle* timeout or *SSO Session Max* lifespan and stays valid after logout. It must be used for a refresh at least once per thirty days or per the value of *Offline Session Idle*.

Limits:
- If *Offline Session Max Limited* is enabled, offline tokens expire after 60 days even when used; change that with *Offline Session Max* in the Admin Console.
- *Client Offline Session Idle* and *Client Offline Session Max* in the client's *Advanced Settings* tab give a specific app shorter timeouts. Client Offline Session Max is evaluated only if Offline Session Max Limited is enabled at realm level. Client session values never affect the global offline user SSO session.
- With *Revoke Refresh Token* enabled each offline token can be used once only; after a refresh store the new offline token from the response.

Requirements: the user needs the realm-level `offline_access` role mapping, the client needs that role in its scope, and the `offline_access` client scope must be an Optional client scope of the client (the default).

Revocation: users can view and revoke offline tokens in the User Account Console; administrators can revoke for one user in the Admin Console *Consents* tab, see all offline tokens in each client's *Offline Access* tab, and revoke by setting a revocation policy.

Cache: Keycloak limits its internal cache of offline user and client sessions to 10000 entries by default; evicted items load on demand from the database. The server configuration guide covers changing that.

## Checked
2026-11-03. Confirmed against server_admin/topics/sessions/offline.adoc. Removed: memory/db-size and key-rotation gotchas, the "Offline token type claim" Verify step and the unsupported "60 days default" phrasing (the page says 60 days when Max Limited is on).
Method: documentation only; no commands were run.
