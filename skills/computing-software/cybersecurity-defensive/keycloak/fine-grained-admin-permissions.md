---
id: computing-software.cybersecurity-defensive.keycloak.fine-grained-admin-permissions
name: fine-grained-admin-permissions
category: computing-software
field: cybersecurity-defensive
product: keycloak
tags: [cybersecurity-defensive, keycloak, fine-grained-permissions, delegated-admin, policy-based-access, admin-permissions]
level: practitioner
status: docs-checked
description: "Limit delegated realm administrators to a subset of users, groups and clients using Keycloak fine-grained admin permissions v2."
sources:
  - https://github.com/keycloak/keycloak/blob/main/docs/documentation/server_admin/topics/admin-console-permissions/fine-grain-v2.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# fine grained admin permissions
Fine-grained admin permissions delegate realm management with policy-based access control over realm resources and the operations (scopes) on them. It is an alternative to the coarse RBAC roles such as `view-users` or `manage-clients`, not a replacement: granting those administrative roles skips this feature's checks. Enforcement applies only to the administration console and the Admin API. Supported resource types: Users, Groups, Clients, Roles, Organizations. Federated resources are not supported; users from external storage providers (such as LDAP) with import disabled are never visible when access is controlled this way.

Administrator types:
- Server administrators: `admin` role in the master realm, manage any realm.
- Realm administrators: `realm-admin` role in a specific realm, full access to that realm.
- Delegated realm administrators: other users or service accounts granted access only through this feature.
Server and realm administrators are not affected by the permissions you define, so review who holds `admin` or `realm-admin` to avoid privilege escalation.

Workflow: in the Admin Console go to *Realm settings*, enable *Admin Permissions* and save; a *Permissions* section appears in the left menu. *Create permission*, choose the resource type, then set Name, Authorization scopes, *Enforce access to* (all resources of the type or specific ones) and Policies.

Scopes are independent with no transitive dependency: granting `manage` does not grant `view`, and assigning only `manage` without `view` makes the user invisible. Users scopes: `view`, `manage`, `manage-group-membership`, `map-roles`, `impersonate`, `reset-password`. Group member scopes (`view-members`, `manage-members`, `impersonate-members`) cascade to child groups and a deny on a parent takes precedence over user-level permissions.

## Checked
2026-11-03. Confirmed against server_admin/topics/admin-console-permissions/fine-grain-v2.adoc. Removed (not on the page): the `--features` flag, the list of policy types, the v1/v2 comparison, the "cannot grant beyond own scope" claim and the Verify step.
Method: documentation only; no commands were run.
