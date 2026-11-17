---
id: computing-software.database-administration.mongodb.rbac-custom-roles
name: rbac-custom-roles
category: computing-software
field: database-administration
product: mongodb
tags: [database-administration, mongodb, mongodb-security, mongodb-rbac, custom-roles, createrole, built-in-roles, least-privilege, privilege-actions, usersinfo]
level: practitioner
status: docs-checked
description: "Give MongoDB users least privilege with built-in roles and custom roles (createRole with resources and actions), and audit who can do what."
sources:
  - https://www.mongodb.com/docs/manual/core/authorization/
  - https://www.mongodb.com/docs/manual/reference/built-in-roles/
  - https://www.mongodb.com/docs/manual/reference/method/db.createRole/
  - https://www.mongodb.com/docs/manual/reference/privilege-actions/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Role-based access control and custom roles

**Goal:** every application and person gets exactly the privileges they need, with authorization enforced.

## Enforce authorization
```yaml
security:
  authorization: enabled
  keyFile: /etc/mongo/keyfile        # replica sets/sharded: implies authorization
```

## Built-in roles worth knowing
| Role | Scope |
|---|---|
| `read`, `readWrite` | One database |
| `dbAdmin` | Schema tasks, indexing and statistics on one DB (no user/role management) |
| `userAdmin` | Manage users/roles in one DB: can grant itself anything, treat as admin |
| `clusterMonitor` | Monitoring agents |
| `backup` / `restore` | Backup and restore |
| `readAnyDatabase`, `readWriteAnyDatabase`, `dbAdminAnyDatabase`, `userAdminAnyDatabase` | All DBs (admin DB) |
| `root` | Everything |

## Custom role
```javascript
use admin
db.createRole({
  role: "ordersAppRole",
  privileges: [
    { resource: { db: "shop", collection: "orders" }, actions: ["find", "insert", "update"] },
    { resource: { db: "shop", collection: "products" }, actions: ["find"] },
    { resource: { db: "shop", collection: "" }, actions: ["listCollections"] }
  ],
  roles: [],
  authenticationRestrictions: [ { clientSource: ["10.20.0.0/16"] } ]
})
db.createUser({ user: "orders_app", pwd: passwordPrompt(), roles: [ { role: "ordersAppRole", db: "admin" } ] })
db.grantRolesToUser("orders_app", [ { role: "read", db: "reports" } ])
```
Note: no `remove` action means the app cannot delete.

## Audit
```javascript
db.getSiblingDB("admin").system.users.find({}, { user: 1, db: 1, roles: 1 })
db.runCommand({ usersInfo: "orders_app", showPrivileges: true })
db.runCommand({ rolesInfo: "ordersAppRole", showPrivileges: true })
```

## Gotchas
- Users are scoped to their authentication database (`authSource`); the same name in two DBs is two users.
- `root` should be break-glass only; app users never need `userAdmin*`, which can grant any privilege to any user, including itself.
- A role created in the `admin` database can include privileges on other databases or the cluster and inherit roles from other databases; a role in any other database is limited to its own.

## Verify
`mongosh -u orders_app ...` then `db.orders.deleteOne({})` fails with an authorization error.

## Checked
2026-10-31. Confirmed against the MongoDB manual: built-in roles reference (role names and
scopes, `userAdmin` can grant any privilege to itself, `readAnyDatabase` excludes `local` and
`config`), `db.createRole` and `db.createUser` (`authenticationRestrictions.clientSource`,
admin-database role scope), Users (authentication database, `system.users` in `admin`).
Removed: `__system` and the Atlas line, and the exact error text.
Method: documentation only; no commands were run.
