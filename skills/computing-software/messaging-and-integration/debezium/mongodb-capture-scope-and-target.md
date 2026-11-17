---
id: computing-software.messaging-and-integration.debezium.mongodb-capture-scope-and-target
name: mongodb-capture-scope-and-target
category: computing-software
field: messaging-and-integration
product: debezium
tags: [mongodb, capture-scope, capture-target, change-streams]
level: practitioner
status: docs-checked
description: "Choose capture.scope deployment, database or collection and set capture.target to narrow a MongoDB change stream."
sources:
  - https://debezium.io/documentation/reference/stable/connectors/mongodb.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`capture.scope` sets the breadth of the change stream the connector opens (default `deployment`):

- `deployment`: one cursor for a replica set or sharded cluster, watching all non-system collections in all databases except `admin`, `local` and `config`.
- `database`: one cursor for a single database and all of its non-system collections.
- `collection`: one cursor for a single collection.

`capture.target` names what to watch:

- scope `database`: the database name, for example `inventory`.
- scope `collection`: the fully qualified name `databaseName.collectionName`, for example `inventory.orders`.

```json
"capture.scope": "collection",
"capture.target": "inventory.orders"
```

Matching permissions are needed (see mongodb-required-user-permissions): read any database for `deployment`, the named database for `database`, the named collection for `collection`.

Connector identity: `topic.prefix` is the logical name for the replica set or cluster. It prefixes all topic names so give every connector a unique name. The docs say to use only alphanumeric characters, hyphens, dots and underscores, and not to change the value after deployment.

The connector writes all insert, update and delete events for each collection to a single Kafka topic.

Check: insert into a collection outside the target and confirm no event appears.

## Checked

2026-11-03. Page used: the Debezium mongodb connector reference, https://debezium.io/documentation/reference/stable/connectors/mongodb.html.
Confirmed against it: capture.scope values and the excluded databases, capture.target formats, the permissions per scope, topic.prefix rules.
Removed or reworded: the resume-token gotcha, the claim that topic.prefix identifies stream position, the letter-or-underscore naming rule (page allows hyphens and dots).
Method: documentation only; no commands were run.
