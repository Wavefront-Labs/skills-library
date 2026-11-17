---
id: computing-software.cybersecurity-defensive.keycloak.master-realm-admin-roles
name: master-realm-admin-roles
category: computing-software
field: cybersecurity-defensive
product: keycloak
tags: [cybersecurity-defensive, keycloak, master-realm, admin, create-realm, realm-management]
level: practitioner
status: docs-checked
description: "Delegate Keycloak administration with the master realm admin and create-realm roles, the per-realm <realm>-realm client roles and multi-realm token-size effects."
sources:
  - https://github.com/keycloak/keycloak/blob/main/docs/documentation/server_admin/topics/admin-console-permissions/master-realm.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# master realm admin roles
Users in the `master` realm can be granted permission to manage zero or more realms. When a realm is created Keycloak creates roles that grant access to it; mapping them to master-realm users controls access to the Admin Console and Admin REST endpoints, so you can have several superusers and users limited to particular realms.

Global roles (realm-level, in master):
- `admin`: superuser with full access to manage any realm.
- `create-realm`: may create realms and gets full access to those. Without `admin` they also need the realm-specific `query-realms` role to create and list realms in the Admin Console.

Realm-specific roles: each realm is represented in master by a client named `<realm name>-realm`, whose client roles are `create-client`, `impersonation`, `manage-authorization`, `manage-clients`, `manage-events`, `manage-identity-providers`, `manage-organizations`, `manage-realm`, `manage-users`, `query-clients`, `query-groups`, `query-organizations`, `query-realms`, `query-users`, `view-authorization`, `view-clients`, `view-events`, `view-identity-providers`, `view-organizations`, `view-realm` and `view-users`. A user with `manage-users` can only assign admin roles they hold themselves.

Granting: assign admin roles explicitly, by direct role mapping (including via identity provider mappers) or via a group with the role mappings, even for master users. Protocol mappers that put admin roles in tokens are ignored: admin roles authorise only Admin Console and Admin REST access.

Multi-realm considerations:
- `admin` is a composite role containing every admin role of every realm's `<realm name>-realm` client (the page's example: 100 realms give over 2,000 role mappings, about 21 roles per realm).
- Full access tokens carry all those roles, which can exceed HTTP header limits at load balancers or proxies with hundreds of realms. Use lightweight access tokens; `security-admin-console` and `admin-cli` use them by default since Keycloak 26.
- Size the realms, users and authorization local caches for many realms (see the server caching guide).
- With fine-grained admin permissions, role policies consider the intersection of the token's roles and the user's actual roles. *Fetch Roles* on a role policy (disabled by default) bypasses the token and client scope when enabled; keep it disabled when several clients authenticate administrators with different access levels.

## Checked
2026-11-03. Confirmed against server_admin/topics/admin-console-permissions/master-realm.adoc. Removed: the unsourced "recommended practice" (break-glass admin, MFA), the realm-management/realm-admin sentence, the view-users/manage-users exposure gotcha and the Verify step; added the full role list and the multi-realm section.
Method: documentation only; no commands were run.
