---
id: computing-software.messaging-and-integration.nats.gateway-configuration
name: gateway-configuration
category: computing-software
field: messaging-and-integration
product: nats
tags: [gateway, super-cluster, gateways, reject-unknown-cluster, cluster-name, gateway-tls]
level: practitioner
status: docs-checked
description: "Join clusters with a gateway block: unique cluster name, listen, gateways list with URLs, authorization, tls, advertise, reject_unknown_cluster."
sources:
  - https://github.com/nats-io/nats.docs/blob/master/running-a-nats-service/configuration/gateways/gateway.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: link independent clusters into a super-cluster so interest and messages flow between them.

The `gateway` block mirrors `cluster`, but you list `gateways` instead of `routes`. Self-gateway entries are ignored, so all servers can share one gateway list. Page example:
```
gateway {
  name: "A"
  listen: "localhost:7222"
  authorization { user: gwu  password: gwp }
  gateways: [
    {name: "A", url: "nats://gwu:gwp@localhost:7222"},
    {name: "B", url: "nats://gwu:gwp@localhost:7333"},
    {name: "C", url: "nats://gwu:gwp@localhost:7444"},
  ]
}
```
Start each with `nats-server -c A.conf`; logs show "Gateway name is A" and inbound/outbound gateway connections registering.

Properties: `name` (all servers of a cluster share it), `host`/`port`/`listen`, `gateways`, `authorization`, `tls` (verify always on; `cert_file` is the default client certificate), `advertise` (host:port reachable from other gateways, for NAT or a network load balancer), `connect_retries` (default 0, once per second, not for explicit gateways), `connect_backoff` (2.12.0, 1s up to 30s), and `reject_unknown_cluster`, which rejects incoming connections from clusters not in `gateways` and so stops gossip of new clusters.

Gotchas: every cluster needs a distinct name; gateway tls always verifies, so certificates must be valid for both client and server use.

## Checked

2026-11-03. Read against the nats.docs repository (the pages listed in `sources`, plus the neighbouring concept, release-note and nsc/nk tool pages): configuration keys, flags, CLI commands, defaults, limits, subjects, header names and version gates were confirmed there.
Removed: the unsourced Verify step, plus statements that no page supports (see the PR notes for the per-skill list).
Method: documentation only; no commands were run.
