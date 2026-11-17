---
id: computing-software.messaging-and-integration.nats.cluster-route-configuration
name: cluster-route-configuration
category: computing-software
field: messaging-and-integration
product: nats
tags: [cluster, routes, cluster-config, route-authorization, pool-size, compression]
level: practitioner
status: docs-checked
description: "Configure a nats-server cluster block: name, listen, routes with credentials, advertise, connect_retries/backoff, pool_size, compression."
sources:
  - https://github.com/nats-io/nats.docs/blob/master/running-a-nats-service/configuration/clustering/cluster_config.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: form a full-mesh NATS cluster with a correct `cluster` block.

Keys documented for the `cluster` map: `name` (recommended since v2.2; each cluster in a super-cluster needs a distinct name), `host`/`port` or `listen` (`<host>:<port>` for inbound routes), `routes` (list of URLs; self-routes ignored; put credentials in the URL when route auth is required), `authorization` (route credentials with `user`, `password`, `timeout`), `tls` (always verifies; `cert_file` serves for both client and server roles), `advertise`/`cluster_advertise` (host:port other members should use, important behind NAT and with TLS since it controls the hostname used for discovered routes), `no_advertise` (stop gossiping server URLs to clients; also disables `client_advertise`), `connect_retries` (default 0; retries once a second; only for discovered routes, not explicit ones), `connect_backoff` (2.12.0; exponential from 1s up to 30s), `pool_size` (default 3, connections used for non-pinned accounts), `accounts` (accounts with a pinned route), `compression` (default `accept`).

Example shape from the page:
```
cluster {
  name: example
  listen: localhost:4244
  authorization { user: route_user  password: pwd  timeout: 0.5 }
  routes = [ nats://route_user:pwd@127.0.0.1:4245, nats://route_user:pwd@127.0.0.1:4246 ]
}
```

Gotchas: the same credentials are what this server expects from peers and uses when it dials discovered routes; use TLS and placeholders, never plain shared passwords, outside tests.

## Checked

2026-11-03. Read against the nats.docs repository (the pages listed in `sources`, plus the neighbouring concept, release-note and nsc/nk tool pages): configuration keys, flags, CLI commands, defaults, limits, subjects, header names and version gates were confirmed there.
Removed: the unsourced Verify step, plus statements that no page supports (see the PR notes for the per-skill list).
Method: documentation only; no commands were run.
