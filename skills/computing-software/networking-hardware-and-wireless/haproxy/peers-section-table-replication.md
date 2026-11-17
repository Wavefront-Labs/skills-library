---
id: computing-software.networking-hardware-and-wireless.haproxy.peers-section-table-replication
name: peers-section-table-replication
category: computing-software
field: networking-hardware-and-wireless
product: haproxy
tags: [networking-hardware-and-wireless, haproxy, peers-section, stick-table-sync, peer-replication, table-synchronisation]
level: practitioner
status: docs-checked
description: "Replicate stick tables between HAProxy nodes with a peers section so rate limits and persistence survive reloads and failover."
sources:
  - https://docs.haproxy.org/3.0/configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# peers section table replication
A `peers` section lists nodes by name; the local node name must equal `hostname` or the `-L` argument.

```
peers lbs
    bind :10000
    default-server ssl verify none
    server lb1 10.0.0.1:10000
    server lb2 10.0.0.2:10000
backend st_rl
    stick-table type ip size 500k expire 1m peers lbs store http_req_rate(10s),gpc0
```
With `peers lbs` on a table, entries and counters are pushed to peers and also kept through reloads (the new process learns from the old one via the local peer), which solves the "reload clears my bans" problem.

Details: the stick-table `store` list picks the data kept per entry (`gpc0`, `gpt0`, `server_id` and rate counters such as `http_req_rate` are valid types). Set `localpeer` or `-L` when the hostname differs from the peer name.

Verify: `echo "show peers" | socat stdio /run/haproxy/admin.sock` lists each peer and its connection state; add an entry on lb1 and see it with `show table st_rl` on lb2.

## Checked
2026-11-08: confirmed against the HAProxy 3.0 configuration manual (peers section, localpeer, stick-table store types, peers keyword on a stick-table, reload synchronisation) and the management manual (-L, show peers, show table). Removed: the peers.txt source (404), the conn_cur and per-node rate remarks, the Peer error text, the cleartext remark and state=ESTA.
Method: documentation only; no commands were run.
