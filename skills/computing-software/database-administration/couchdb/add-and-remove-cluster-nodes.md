---
id: computing-software.database-administration.couchdb.add-and-remove-cluster-nodes
name: add-and-remove-cluster-nodes
category: computing-software
field: database-administration
product: couchdb
tags: [cluster, membership, nodes-database, add-node, remove-node]
level: practitioner
status: docs-checked
description: "Add a node to a CouchDB cluster with PUT /_node/_local/_nodes/{name}, check /_membership, and remove one by deleting its node document after moving shards."
sources:
  - https://raw.githubusercontent.com/apache/couchdb/main/src/docs/src/cluster/nodes.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`GET /_membership` shows the node's name and its peers: `all_nodes` are all nodes this node knows about, `cluster_nodes` are those connected.

**Add a node:**

```
curl -X PUT "http://xxx.xxx.xxx.xxx/_node/_local/_nodes/node2@yyy.yyy.yyy.yyy" -d {}
```

Check `/_membership` again; both lists should now include the new node. The other node shows the same, so you only add it once.

**Remove a node.** First move all shards off it. Then fetch the node document to learn its revision:

```
curl "http://xxx.xxx.xxx.xxx/_node/_local/_nodes/node2@yyy.yyy.yyy.yyy"
```

and delete it using that `_rev`:

```
curl -X DELETE "http://xxx.xxx.xxx.xxx/_node/_local/_nodes/node2@yyy.yyy.yyy.yyy?rev=<rev>"
```

## Checked

2026-11-04. Confirmed against the CouchDB cluster/nodes page: _membership fields, the PUT to add a node, the GET and DELETE with rev to remove one, moving shards first. Removed a claim that existing shards are not rebalanced onto a new node (not on the page).

Method: documentation only; no commands were run.
