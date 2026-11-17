---
id: computing-software.cybersecurity-defensive.keycloak.role-scope-mappings-and-full-scope
name: role-scope-mappings-and-full-scope
category: computing-software
field: cybersecurity-defensive
product: keycloak
tags: [cybersecurity-defensive, keycloak, role-scope-mapping, full-scope-allowed, least-privilege, access-token]
level: practitioner
status: docs-checked
description: "Limit roles in Keycloak access tokens: turn off Full Scope Allowed, declare role scope mappings per client or client scope, enforce with a client policy."
sources:
  - https://github.com/keycloak/keycloak/blob/main/docs/documentation/server_admin/topics/roles-groups/con-role-scope-mappings.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# role scope mappings and full scope
Role scope mappings limit the roles declared in an access token: the token contains only the role mappings explicitly specified for the client's scope, so each token's permissions are limited instead of covering all of the user's permissions.

By default each client gets all the user's role mappings: the effective roles of scopes are every declared role in the realm (*Full Scope Allowed* ON). The docs warn that Full Scope Allowed is deprecated and will be removed in a future release; leaving it on puts every role the user holds in every access token, widening the blast radius if a token is compromised. The docs say to disable it on every client and configure the required role scope mappings explicitly.

Procedure to view or change a client's mappings: *Clients* > the client > *Client scopes* tab > the link in the row "Dedicated scope and mappers for this client" > *Scope* tab. Toggle *Full Scope Allowed* OFF and declare the specific roles for that client. Client scopes can define the same role scope mappings for a set of clients.

To enforce this realm-wide for new and updated clients, configure a client policy with the *Full Scope Disabled* executor (the page points to its "Enforcing Full Scope Allowed to be disabled" section; see client-policies-profiles-and-executors). The algorithm that puts roles into the token is in the guide's Token Role mappings section.

## Checked
2026-11-03. Confirmed against server_admin/topics/roles-groups/con-role-scope-mappings.adoc. Removed: the `<client>-dedicated` naming, "Assign role" button, the intersection/service-account sentence, the roll-out gotcha and the Evaluate Verify step, none of which are on the page.
Method: documentation only; no commands were run.
