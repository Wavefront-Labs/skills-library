---
id: computing-software.database-administration.mongodb.built-in-roles-and-least-privilege-users
name: built-in-roles-and-least-privilege-users
category: computing-software
field: database-administration
product: mongodb
tags: [database-administration, mongodb, mongodb-security, mongodb-built-in-roles, mongodb-rbac, createuser, least-privilege]
level: practitioner
status: docs-checked
description: "Pick MongoDB built-in roles for apps, operators, backup and monitoring accounts, scope them to databases, and audit who holds powerful roles like root or dbOwner."
sources:
  - https://www.mongodb.com/docs/manual/reference/built-in-roles/
  - https://www.mongodb.com/docs/manual/tutorial/create-users/
  - https://www.mongodb.com/docs/manual/reference/method/db.getUsers/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Built-in roles and least-privilege users

## Map accounts to roles
| Account | Roles | Notes |
|---|---|---|
| application | `readWrite` on its own db(s) | never `dbOwner` or anything on `admin` |
| read-only reporting | `read` on specific dbs | |
| ops DBA | `clusterMonitor`, `dbAdminAnyDatabase`, `readWriteAnyDatabase` as needed | keep `root` to break-glass |
| backup (mongodump / agents) | `backup`; restores: `restore` | `backup` is enough to use mongodump on a whole mongod |
| monitoring (exporters) | `clusterMonitor` | read-only access to monitoring tools |
| user admin | `userAdmin` (db) / `userAdminAnyDatabase` | can grant itself any privilege on its scope: treat like root |
| sharded cluster ops | `clusterManager` | cluster management actions |
`root` = readWriteAnyDatabase + dbAdminAnyDatabase + userAdminAnyDatabase + clusterAdmin + restore + backup.
`dbOwner` on a db = readWrite + dbAdmin + userAdmin for that db (can create users there).

## Create users
```js
use admin
db.createUser({
  user: "orders_app",
  pwd: passwordPrompt(),
  roles: [ { role: "readWrite", db: "orders" } ],
  authenticationRestrictions: [ { clientSource: ["10.0.20.0/24"] } ],   // optional IP restriction
  mechanisms: ["SCRAM-SHA-256"]
})
db.grantRolesToUser("orders_app", [{ role: "read", db: "catalog" }])
db.revokeRolesFromUser("orders_app", [{ role: "read", db: "catalog" }])
```
Create users in `admin` (authentication database) consistently so connection strings use
`authSource=admin`.

## Custom roles when built-ins are too broad
Example: an app allowed to insert into `audit.events` but not read it:
```js
db.getSiblingDB("admin").createRole({ role: "auditWriter",
  privileges: [{ resource: { db: "audit", collection: "events" }, actions: ["insert"] }], roles: [] })
```

## Audit
```js
db.getSiblingDB("admin").system.users.find({}, { user: 1, db: 1, roles: 1 })
db.getSiblingDB("admin").aggregate([{ $listLocalSessions: { allUsers: true } }])   // who is connected
db.getUsers({ showCredentials: false, filter: { "roles.role": { $in: ["root", "userAdminAnyDatabase", "dbOwner"] } } })
```
Review quarterly; remove users of departed staff; rotate application passwords
(`db.changeUserPassword`) via your secret manager.

## Gotchas
- `__system` and internal roles are not for users.
- In sharded clusters, create users through `mongos`; shard-local users exist only on that shard, are for direct shard maintenance, and cannot connect to `mongos`.
- `readAnyDatabase` and `readWriteAnyDatabase` cover every database except `local` and `config`; still avoid them for apps.

## Verify
`db.runCommand({ connectionStatus: 1, showPrivileges: true })` as the app user shows only the
intended roles; a forbidden action returns `not authorized on ... to execute command`.

## Checked

2026-10-25, against the MongoDB manual source (mongodb/docs repository, content/manual/manual, latest commit 2026-10-23). Confirmed: root composition (readWriteAnyDatabase, dbAdminAnyDatabase, userAdminAnyDatabase, clusterAdmin, restore, backup), dbOwner = readWrite + dbAdmin + userAdmin, backup role sufficient for mongodump of a whole mongod, clusterMonitor, userAdmin can assign itself any privilege on its database, readAnyDatabase excludes local and config (the previous text said the opposite), db.createUser fields authenticationRestrictions, mechanisms and passwordPrompt(), db.getUsers showCredentials (5.2+) and filter, connectionStatus showPrivileges, shard-local users. Removed unconfirmed monitoring-on-local and config-server user claims.

Method: documentation only; no commands were run.
