---
id: computing-software.database-administration.couchdb.single-node-setup
name: single-node-setup
category: computing-software
field: database-administration
product: couchdb
tags: [setup, single-node, system-databases, fauxton, port-5984]
level: intro
status: docs-checked
description: "Set up CouchDB as a single node: the Fauxton wizard, [couchdb] single_node=true, or creating _users, _replicator and _global_changes manually."
sources:
  - https://raw.githubusercontent.com/apache/couchdb/main/src/docs/src/setup/single-node.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A single node is operationally roughly equivalent to the CouchDB 1.x series and gets none of the 2.x scaling or fault-tolerance benefits.

**Wizard.** Open Fauxton at `http://127.0.0.1:5984/_utils#setup`, choose "Single-Node-Setup", and enter an admin username and password. Bind to `127.0.0.1` to stay private, or `0.0.0.0` for all addresses. The wizard creates `_users`, `_replicator` and `_global_changes`.

**Config.** Set `[couchdb] single_node=true` in `local.ini`. CouchDB then creates the system databases on restart.

**Manual.** With an admin already in a config file, create them yourself:

```
curl -X PUT http://adm:pass@127.0.0.1:5984/_users
curl -X PUT http://adm:pass@127.0.0.1:5984/_replicator
curl -X PUT http://adm:pass@127.0.0.1:5984/_global_changes
```

`_global_changes` is only needed if you use the global changes feed. You may delete it if it has grown and you do not need it, avoiding the cost of compacting it regularly.

## Checked

2026-11-04. Confirmed against the CouchDB setup/single-node page: 1.x-equivalent operation, the Fauxton wizard URL and bind options, the three system databases, [couchdb] single_node=true, manual creation commands, and the optional _global_changes note. Nothing removed.

Method: documentation only; no commands were run.
