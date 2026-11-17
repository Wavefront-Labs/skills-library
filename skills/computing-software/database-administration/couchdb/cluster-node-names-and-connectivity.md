---
id: computing-software.database-administration.couchdb.cluster-node-names-and-connectivity
name: cluster-node-names-and-connectivity
category: computing-software
field: database-administration
product: couchdb
tags: [cluster, vm-args, node-name, erlang-cookie, connectivity-test]
level: practitioner
status: docs-checked
description: "Set CouchDB node names and the distribution port range in etc/vm.args, and verify node-to-node connectivity with an erl shell and net_kernel:connect_node."
sources:
  - https://raw.githubusercontent.com/apache/couchdb/main/src/docs/src/setup/cluster.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
In `etc/vm.args` on every node, change `-name couchdb@127.0.0.1` to `-name couchdb@<reachable-ip-address|fully-qualified-domain-name>`.

- The name part can be `couchdb` everywhere, unless several nodes share a host: then use `couchdb1`, `couchdb2` and so on.
- Prefer the FQDN so you can renumber IPs without disrupting the cluster.
- Changing the name later is cumbersome (shards must move), so set it once.

Also add, on all nodes:

```
-kernel inet_dist_listen_min 9100
-kernel inet_dist_listen_max 9200
```

**Test connectivity** between two servers with the same cookie and range. On each, start `erl -name <name>@<ip> -setcookie '<cookie>' -kernel inet_dist_listen_min 9100 -kernel inet_dist_listen_max 9200`. In the first shell run, ending with a period:

```
net_kernel:connect_node('<other-name>@<other-ip>').
```

`true` means the firewalls are open and nodes can communicate. `false` or nothing points to firewall, DNS or settings. Repeat for all pairs of servers.

## Checked

2026-11-04. Confirmed against the CouchDB setup/cluster page: vm.args node name, naming rules, FQDN preference, the rename warning, the 9100-9200 distribution range, the erl connectivity test and net_kernel:connect_node results. Nothing removed.

Method: documentation only; no commands were run.
