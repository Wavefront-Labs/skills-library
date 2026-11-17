---
id: computing-software.messaging-and-integration.nats.leaf-node-configuration
name: leaf-node-configuration
category: computing-software
field: messaging-and-integration
product: nats
tags: [leafnodes, leaf-node, remotes, handshake-first, deny-exports, hub]
level: practitioner
status: docs-checked
description: "Configure leaf nodes: accepting leafnodes block (port 7422, tls, authorization) and remotes entries (urls, credentials, account, deny lists)."
sources:
  - https://github.com/nats-io/nats.docs/blob/master/running-a-nats-service/configuration/leafnodes/leafnode_conf.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: connect an edge server (leaf) to a hub, bound to an account, with the right TLS and subject limits.

The `leafnodes` block configures both incoming connections (`host`, `port` default 7422, `listen`, `tls`, `advertise`, `no_advertise`, `authorization`, `compression` default `s2_auto`) and outgoing ones (`remotes`, `reconnect` in seconds).

Accepting side authorization: `user`/`password`/`account`/`timeout`, or a `users` list each bound to an `account`; the block is optional if matching users already exist in accounts.

Each `remotes` entry: `url` or `urls` (scheme `nats-leaf://`, several for discovery), `account` (the local account whose traffic is forwarded), `credentials` (creds file) or `nkey`, `deny_imports` and `deny_exports` (subjects not propagated in each direction), `compression`, `hub` (default false; true reverses roles so the hub dials the leaf), `first_info_timeout` (default 1s), plus `ws_compression` and `ws_no_masking` for WebSocket URLs.

TLS-first (since 2.10.0): put `handshake_first: true` in the accepting side's `leafnodes { tls { ... } }` and also in the remote's `tls`. If only one side has it, the connection fails because one side starts a TLS handshake while the other sends a clear INFO.

Example accepting side:
```
leafnodes { port: 7422  authorization { user: leaf  password: <secret>  account: TheAccount } }
```

## Checked

2026-11-03. Read against the nats.docs repository (the pages listed in `sources`, plus the neighbouring concept, release-note and nsc/nk tool pages): configuration keys, flags, CLI commands, defaults, limits, subjects, header names and version gates were confirmed there.
Removed: the unsourced Verify step, plus statements that no page supports (see the PR notes for the per-skill list).
Method: documentation only; no commands were run.
