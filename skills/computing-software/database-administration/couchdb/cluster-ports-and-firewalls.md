---
id: computing-software.database-administration.couchdb.cluster-ports-and-firewalls
name: cluster-ports-and-firewalls
category: computing-software
field: database-administration
product: couchdb
tags: [cluster, firewall, epmd, port-5984, port-4369, erlang-distribution]
level: practitioner
status: docs-checked
description: "Which ports a CouchDB cluster uses (5984, 4369, Erlang distribution range), where to bind them, and the cookie warning for exposed distribution ports."
sources:
  - https://raw.githubusercontent.com/apache/couchdb/main/src/docs/src/setup/cluster.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
| Port | Use | Recommended binding |
|---|---|---|
| 5984/tcp | all HTTP API requests | as desired; `localhost` by default |
| 4369/tcp | Erlang port mapper daemon (epmd) | `localhost` for single node; private interface if clustered |
| random above 1024 | traffic with other CouchDB nodes | private interface |

- Clustered mode uses 5984 just like standalone. Port 5986 (CouchDB 2.x) is removed in 3.x: its endpoints are now under `/_node/{node-name}/...` on 5984.
- All servers must reach each other on 4369. Erlang nodes form a full mesh.
- Erlang picks the inbound distribution ports automatically (random), which breaks with a firewall. Force a range with `inet_dist_listen_min` and `inet_dist_listen_max` (the page uses TCP 9100-9200, and notes one port per CouchDB node on a machine suffices, for example `9100-9100` for one node).

Warning: if the distribution port is exposed to the Internet or an untrusted network, the only protection is the Erlang cookie.

## Checked

2026-11-04. Confirmed against the CouchDB setup/cluster page: port table, 5986 removed in 3.x, epmd mesh, random inbound ports, the 9100-9200 range and single-port note, the cookie warning. Nothing removed.

Method: documentation only; no commands were run.
