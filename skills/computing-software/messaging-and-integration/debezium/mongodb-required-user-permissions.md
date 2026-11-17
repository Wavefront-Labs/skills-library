---
id: computing-software.messaging-and-integration.debezium.mongodb-required-user-permissions
name: mongodb-required-user-permissions
category: computing-software
field: messaging-and-integration
product: debezium
tags: [mongodb, permissions, user, capture-scope]
level: practitioner
status: docs-checked
description: "Grant the MongoDB user Debezium needs: read access matching capture.scope, the hello command, and config.shards when required."
sources:
  - https://debezium.io/documentation/reference/stable/connectors/mongodb.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The MongoDB user for Debezium needs to read from the database and to run the `hello` command. It may also need to read `config.shards`.

Read access depends on `capture.scope`:

- `deployment`: permission to read any database.
- `database`: permission to read the database named in `capture.target`.
- `collection`: permission to read the collection named in `capture.target`.

Regardless of scope, the user must be allowed to run `hello`.

Explicit permission to read the `config.shards` system collection is required so the connector can perform offset consolidation, in two environments:

- Connectors upgraded from Debezium 2.5 or earlier.
- Connectors capturing from a sharded MongoDB cluster.

The connection itself is set in `mongodb.connection.string`, which replaces the old `mongodb.hosts` property:

```json
"mongodb.connection.string": "mongodb://dbz_user:secret@mongo1:27017/?replicaSet=rs0",
"capture.scope": "database",
"capture.target": "inventory"
```

Use a placeholder credential from your secret store, not a literal password, in real configurations.

Gotcha: `deployment` scope watches all non-system collections across all databases except `admin`, `local` and `config`, so it needs permission to read any database.

Check: confirm the user can run the `hello` command and read a captured collection.

## Checked

2026-11-03. Page used: the Debezium mongodb connector reference, https://debezium.io/documentation/reference/stable/connectors/mongodb.html.
Confirmed against it: read permission per capture.scope, the hello command, config.shards for 2.5-or-earlier upgrades and sharded clusters, mongodb.connection.string replacing mongodb.hosts.
Removed or reworded: the custom-role advice and the db.hello() shell form.
Method: documentation only; no commands were run.
