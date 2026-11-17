---
id: computing-software.database-administration.couchdb.cluster-setup-api
name: cluster-setup-api
category: computing-software
field: database-administration
product: couchdb
tags: [cluster, cluster-setup, enable-cluster, add-node, finish-cluster]
level: practitioner
status: docs-checked
description: "Script CouchDB cluster creation with POST /_cluster_setup actions enable_cluster, add_node and finish_cluster, and repair node lists via /_nodes."
sources:
  - https://raw.githubusercontent.com/apache/couchdb/main/src/docs/src/setup/cluster.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
First enable each node locally (POST with `Content-Type: application/json`):

```
curl -X POST -H "Content-Type: application/json" http://admin:password@127.0.0.1:5984/_cluster_setup -d '{"action": "enable_cluster", "bind_address":"0.0.0.0", "username": "admin", "password":"password", "node_count":"3"}'
```

Pick one node as the setup coordination node; it has no special role after setup (CouchDB has no primary node). All nodes must be online and preconfigured. For each other node, run against the coordinator an `enable_cluster` call that adds `port`, `remote_node`, `remote_current_user` and `remote_current_password`, then:

```
-d '{"action": "add_node", "host":"<remote-node-ip>", "port": <remote-node-port>, "username": "admin", "password":"password"}'
```

Finish, which also adds the system databases:

```
-d '{"action": "finish_cluster"}'
```

Verify: `GET /_cluster_setup` returns `{"state":"cluster_finished"}`, and `GET /_membership` should list matching `all_nodes` and `cluster_nodes`.

If they do not match, add a node with `PUT /_node/_local/_nodes/couchdb@<ip-or-fqdn>` and remove one with `DELETE` on the same path.

## Checked

2026-11-04. Confirmed against the CouchDB setup/cluster page (The Cluster Setup API): enable_cluster, add_node and finish_cluster request bodies, the setup coordination node and no primary node, all nodes online, system databases added by finish_cluster, cluster_finished state, _membership all_nodes and cluster_nodes check, PUT and DELETE on /_node/_local/_nodes. Nothing removed.

Method: documentation only; no commands were run.
