---
id: computing-software.database-administration.couchdb.cluster-setup-wizard
name: cluster-setup-wizard
category: computing-software
field: database-administration
product: couchdb
tags: [cluster, fauxton, setup-wizard, membership, haproxy]
level: intro
status: docs-checked
description: "Build a CouchDB cluster with the Fauxton Setup Cluster wizard and confirm it with GET /_membership, comparing all_nodes and cluster_nodes."
sources:
  - https://raw.githubusercontent.com/apache/couchdb/main/src/docs/src/setup/cluster.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
At least 3 nodes are strongly recommended.

1. Install and start all nodes, ensure they are reachable, and complete the pre-configuration steps.
2. Visit `http://<server1>:5984/_utils#setup` and choose "Setup Cluster".
3. Re-enter admin credentials and specify the total number of nodes you expect to add.
4. Enter each node's IP or FQDN with the server admin username and password.
5. Click "Setup".

Verify on each node with `GET http://<server>:5984/_membership`:

```json
{"all_nodes": ["couchdb@server1.test.com", ...],
 "cluster_nodes": ["couchdb@server1.test.com", ...]}
```

`cluster_nodes` lists the expected nodes; `all_nodes` lists those actually connected. The two must match. You can then send requests to any node.

For production, put an HTTP reverse proxy in front for load balancing and SSL termination. HAProxy is recommended, and sample configurations are in the best-practices section.

## Checked

2026-11-04. Confirmed against the CouchDB setup/cluster page: three-node recommendation, wizard steps, _membership verification, meaning of cluster_nodes and all_nodes, HAProxy recommendation. Nothing removed.

Method: documentation only; no commands were run.
