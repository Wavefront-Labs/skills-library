---
id: computing-software.cybersecurity-defensive.keycloak.client-scopes-and-optional-scopes
name: client-scopes-and-optional-scopes
category: computing-software
field: cybersecurity-defensive
product: keycloak
tags: [cybersecurity-defensive, keycloak, client-scope, default-scope, optional-scope, scope-parameter]
level: practitioner
status: docs-checked
description: "Use shared client scopes (roles, web-origins, microprofile-jwt, offline_access) to control mappers and role scope mappings for many clients."
sources:
  - https://github.com/keycloak/keycloak/blob/main/docs/documentation/server_admin/topics/clients/con-client-scopes.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# client scopes and optional scopes
A client scope defines shared client configuration: protocol mappers and role scope mappings for multiple clients. It also supports the OAuth 2 `scope` parameter so applications can request claims or roles in the access token. All clients linked to one scope must use the same protocol.

Built-in scopes per realm:
- SAML: `role_list` (one mapper for the roles list in the assertion).
- OIDC: `roles` (mappers adding user roles to the access token and audiences for clients with at least one client role; not added to the `scope` claim by default), `web-origins` (adds the `allowed-origins` claim), `microprofile-jwt` (user property mapper for `upn`, realm role mapper for `groups`), `offline_access` (clients that need offline tokens), and `profile`, `email`, `address`, `phone` (protocol mappers for the spec's claims, no role scope mappings).

Linking (client's *Client scopes* tab):
- Default: applied to every token or assertion regardless of the `scope` parameter (SAML and OIDC).
- Optional: OIDC only; applied only when requested in `scope`. With `profile` and `email` default and `phone`, `address` optional, `scope=openid phone` yields mappers and role scope mappings from profile, email and phone.
- *Include in token scope* controls whether a scope's name appears in the token `scope` claim and introspection response.
- Every client has a dedicated scope (shown as `<client>-dedicated`) for mappers and role scope mappings specific to that client; it cannot be unlinked or linked elsewhere.
- A scope with role scope mappings applies to a user only if the user holds at least one of those roles (composites counted); a scope without any applies to everyone.

Warning from the docs: assigning a scope to a client needs permission to manage both clients and client scopes (the `manage-clients` role grants both), and scopes can carry mappers and role mappings, so grant that carefully.

## Checked
2026-11-03. Confirmed against server_admin/topics/clients/con-client-scopes.adoc. Removed: the `service1-scope` example (replaced with the page's `scope=openid phone` example), the claim about `realm_access`/`resource_access` disappearing when `roles` is removed, and the unverified Verify step.
Method: documentation only; no commands were run.
