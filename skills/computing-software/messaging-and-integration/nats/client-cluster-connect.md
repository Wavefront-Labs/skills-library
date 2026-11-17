---
id: computing-software.messaging-and-integration.nats.client-cluster-connect
name: client-cluster-connect
category: computing-software
field: messaging-and-integration
product: nats
tags: [client-connect, cluster, seed-servers, server-urls, failover]
level: practitioner
status: docs-checked
description: "Connect NATS clients to a cluster with seed server URLs, randomized order and server-advertised URLs for reconnects."
sources:
  - https://github.com/nats-io/nats.docs/blob/master/using-nats/developing-with-nats/connecting/cluster.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: make a client resilient to a single server being down at connect time and later.

How the page says it works:
- On first connect the library tries the URLs you supply, usually in random order so not every client lands on the same server; the first success wins. Randomization can be disabled explicitly through a connection option.
- After connecting, the server can send a list of other known servers, so the client holds alternatives for reconnect even if you configured only some members. This lets the cluster mesh grow and change without redeploying clients.
- You should still pass a sensible list of front-line (seed) servers so the initial connect can succeed; you do not need to list every member.

Go example pattern: build the list `[]string{"nats://127.0.0.1:1222", "nats://127.0.0.1:1223", "nats://127.0.0.1:1224"}`, join with commas and pass to `nats.Connect(strings.Join(servers, ","))`, then `defer nc.Close()`.

Gotchas: failure behavior when all URLs fail is library dependent (some retry, some return an error), so read your client's docs.

## Checked

2026-11-03. Read against the nats.docs repository (the pages listed in `sources`, plus the neighbouring concept, release-note and nsc/nk tool pages): configuration keys, flags, CLI commands, defaults, limits, subjects, header names and version gates were confirmed there.
Removed: the unsourced Verify step, plus statements that no page supports (see the PR notes for the per-skill list).
Method: documentation only; no commands were run.
