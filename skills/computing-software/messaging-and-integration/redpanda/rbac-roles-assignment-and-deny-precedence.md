---
id: computing-software.messaging-and-integration.redpanda.rbac-roles-assignment-and-deny-precedence
name: rbac-roles-assignment-and-deny-precedence
category: computing-software
field: messaging-and-integration
product: redpanda
tags: [rbac, roles, rpk-security-role, deny-precedence, enterprise, acl]
level: practitioner
status: docs-checked
description: "Create roles with rpk security role, attach ACLs with --allow-role, assign users, and predict conflicts between ACLs and roles (DENY wins)."
sources:
  - https://docs.redpanda.com/streaming/current/manage/security/authorization/rbac/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
RBAC (enterprise license) groups ACLs into roles you assign to many users. It works with every authentication method. Roles and permissions can be managed with `rpk security`, the Admin API or Redpanda Console (Security, Roles tab).

```bash
rpk security role create DataAnalysts
rpk security acl create --operation read,describe \
  --topic 'analytics-' --resource-pattern-type prefixed \
  --allow-role DataAnalysts
rpk security acl create --operation write,describe \
  --topic 'reports-' --resource-pattern-type prefixed \
  --allow-role DataAnalysts
rpk security role assign DataAnalysts --principal alice,bob,charlie
rpk security role describe DataAnalysts
```

Changing a role's ACLs changes every assigned user at once. A user can hold any number of roles. A new cluster has no roles; create the first with a superuser account. When upgrading from older versions, existing SASL/SCRAM users are assigned a placeholder `User` role with no ACLs, which is convenient for granting something to everyone, for example:

```bash
rpk security acl create --operation write --topic private-software-versions --allow-role User
```

**Conflict resolution.** An operation is permitted if and only if no matching DENY exists and a matching ALLOW exists. Examples from the page: a direct ALLOW READ on a topic loses to a role DENY READ; a specific DENY WRITE beats a wildcard role ALLOW; a role-only ALLOW applies when there are no direct ACLs.

Best practices on the page: descriptive, focused role names; minimal permissions; avoid DENY rules where specific ALLOW rules will do; review roles quarterly; use time-limited roles for temporary access.

## Checked

2026-11-08. Read the whole Configure Role-Based Access Control page and confirmed the enterprise license note, management interfaces and Console path, the DataAnalysts command sequence, one-to-many role assignment, no roles on a new cluster and the superuser requirement, the placeholder User role on upgrade (no ACLs) and its example, the permission resolution rules with the examples, and the best practices. Nothing removed.

Method: documentation only; no commands were run.
