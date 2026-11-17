---
id: computing-software.database-administration.couchdb.prepare-cluster-nodes
name: prepare-cluster-nodes
category: computing-software
field: database-administration
product: couchdb
tags: [cluster, uuid, http-secret, admin, bind-address]
level: practitioner
status: docs-checked
description: "Pre-join settings every CouchDB cluster node needs: vm.args, an admin, reachable bind_address, and identical uuid and chttpd_auth secret."
sources:
  - https://raw.githubusercontent.com/apache/couchdb/main/src/docs/src/setup/cluster.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Before joining, nodes must listen on an address reachable by the others, and these must match across nodes:

1. `etc/vm.args` settings (name, distribution ports).
2. At least one server admin (same password on all nodes).
3. Clustered interface (5984) bound to a reachable IP.
4. A consistent `[couchdb] uuid`: it identifies the cluster in replication; if inconsistent, replications may rewind the changes feed to zero (excess memory, CPU, network).
5. A consistent `[chttpd_auth] secret`, used for cookie and proxy auth; avoids repeated session cookie requests.

From CouchDB 3.0 the setup API does steps 4 and 5 for you.

With configuration management, distribute an `.ini` file; pre-encrypt the password so CouchDB does not rewrite the file. Otherwise, per server:

```
curl http://<server>:5984/_uuids?count=2
curl -X PUT http://<server>:5984/_node/_local/_config/admins/admin -d '"password"'
curl -X PUT http://<server>:5984/_node/_local/_config/chttpd/bind_address -d '"0.0.0.0"'
curl -X PUT http://<server>:5984/_node/_local/_config/couchdb/uuid -d '"FIRST-UUID"'
curl -X PUT http://<server>:5984/_node/_local/_config/chttpd_auth/secret -d '"SECOND-UUID"'
```

Use the same two UUIDs on every node.

## Checked

2026-11-04. Confirmed against the CouchDB setup/cluster page: the five pre-join settings, uuid and secret reasons, the 3.0 setup API note, configuration-management advice and the curl sequence. Nothing removed.

Method: documentation only; no commands were run.
