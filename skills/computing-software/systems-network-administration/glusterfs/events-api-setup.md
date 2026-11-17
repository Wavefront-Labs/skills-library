---
id: computing-software.systems-network-administration.glusterfs.events-api-setup
name: events-api-setup
category: computing-software
field: systems-network-administration
product: glusterfs
tags: [glusterfs, events-api, glustereventsd, gluster-eventsapi, webhook]
level: advanced
status: docs-checked
description: "Run the GlusterFS Events API: enable glustereventsd on every node, register webhooks with gluster-eventsapi, sync nodes, and configure port and log level."
sources:
  - https://raw.githubusercontent.com/gluster/glusterdocs/master/docs/Administrator-Guide/Events-APIs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Events API setup and webhooks

On all peer nodes (systemd):

```
systemctl enable glustereventsd
systemctl start glustereventsd
gluster-eventsapi status
```

If SELinux is enforcing, install the `glusterfs-selinux` package. The default eventsd port is 55555 and must be in the ephemeral range.

Webhooks: test first, add only after every peer reports OK.

```
gluster-eventsapi webhook-test <url> [--bearer_token <token>]
gluster-eventsapi webhook-add <url> [--bearer_token <token>]
gluster-eventsapi webhook-del <url>
gluster-eventsapi sync
```

The webhook receives POSTs with JSON containing `nodeid`, `ts`, `event` and `message`. Gluster nodes must be able to reach the webhook server.

Config:

```
gluster-eventsapi config-get [--name <name>]
gluster-eventsapi config-set <name> <value>
gluster-eventsapi config-reset <name|all>
```

Names and defaults: `log-level` INFO, `port` 55555, `disable-events-log` False.

If a node was down or its sync status is not OK, run `gluster-eventsapi sync` from a peer once it is back. When adding a node, enable and start eventsd on it, then run `sync` from a different peer.

## Checked

2026-11-04. Confirmed against the glusterdocs Events APIs page: glustereventsd enable and start, status, glusterfs-selinux when SELinux is enforcing, port 55555 in the ephemeral range, webhook-test, webhook-add, webhook-del, sync, config-get, config-set, config-reset (name or all), config defaults, the JSON attributes, the sync-after-node-down note and the add-a-node steps. Nothing removed.

Method: documentation only; no commands were run.
