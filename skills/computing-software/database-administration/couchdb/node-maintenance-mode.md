---
id: computing-software.database-administration.couchdb.node-maintenance-mode
name: node-maintenance-mode
category: computing-software
field: database-administration
product: couchdb
tags: [maintenance-mode, load-balancer, haproxy, health-check, up-endpoint]
level: practitioner
status: docs-checked
description: "Put a CouchDB node into maintenance mode so /_up returns 404 and load balancers drain it, and verify before and after shard changes."
sources:
  - https://raw.githubusercontent.com/apache/couchdb/main/src/docs/src/cluster/sharding.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Maintenance mode makes `GET /_up` return `404 Not Found` and stops the node taking part in normal interactive clustered requests for its shards. A load balancer that health-checks `/_up` removes it from rotation. Use it before telling the cluster about new shard replicas on a node, otherwise the cluster may return incorrect responses from that node.

HAProxy settings from the page:

```
http-check disable-on-404
option httpchk GET /_up
```

Enable:

```
curl -X PUT -H "Content-type: application/json" \
  $COUCH_URL:5984/_node/{node-name}/_config/couchdb/maintenance_mode -d "\"true\""
```

Verify with `GET /_up` on that node: `404` with `{"status":"maintenance_mode"}`. Also check the load balancer dropped the node.

Disable by putting `"false"` to the same endpoint, verify `/_up` again, and confirm the balancer returned the node to the pool. Do this only after internal replication has caught up.

## Checked

2026-11-04. Confirmed against the CouchDB cluster/sharding page (Set the target node to maintenance mode, Clear maintenance mode): /_up 404, HAProxy lines, the PUT to maintenance_mode, verification and load balancer checks. Nothing removed.

Method: documentation only; no commands were run.
