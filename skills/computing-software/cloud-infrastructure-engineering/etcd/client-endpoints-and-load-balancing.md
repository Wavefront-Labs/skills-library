---
id: computing-software.cloud-infrastructure-engineering.etcd.client-endpoints-and-load-balancing
name: client-endpoints-and-load-balancing
category: computing-software
field: cloud-infrastructure-engineering
product: etcd
tags: [client, endpoints, load-balancing, retry, clientv3, failover, dial-timeout, keepalive]
level: practitioner
status: docs-checked
description: "Connect clients reliably: advertised client URLs, forwarding to the leader and gRPC keepalive flags."
sources:
  - "https://etcd.io/docs/v3.5/faq/"
  - "https://etcd.io/docs/v3.5/op-guide/configuration/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Clients are expected to cope with member failures by themselves.

Practices:

- Members advertise their client URLs with `--advertise-client-urls`; these must be reachable from the machines that talk to etcd, because client libraries parse them to connect to the cluster. Do not advertise `localhost` or `0.0.0.0` in production.
- `--listen-client-urls` is the local address a member binds to; `0.0.0.0` listens on all interfaces.
- A client does not need to know the leader: a request that needs consensus sent to a follower is forwarded to the leader, and requests that do not need consensus (for example serialized reads) can be served by any member.

Server-side gRPC keepalive flags: `--grpc-keepalive-min-time` (default 5s) is the minimum interval a client should wait before pinging the server; `--grpc-keepalive-interval` (default 2h) is the frequency of server-to-client pings to check a connection is alive (0 disables); `--grpc-keepalive-timeout` (default 20s) is the additional wait before closing a non-responsive connection (0 disables).

## Checked

2026-11-08. Read in full: etcd v3.5 FAQ and Configuration options pages. Confirmed the URL flags, the advertise-address warning, forwarding to the leader, serialized reads and the three keepalive flags with defaults. Removed: dial-timeout and context-deadline advice, learners rejecting client requests, DNS SRV for clients (the flag is for server bootstrap), staleness wording, and TCP load balancer and watch-stickiness claims (not on the pages read).
Method: documentation only; no commands were run.
