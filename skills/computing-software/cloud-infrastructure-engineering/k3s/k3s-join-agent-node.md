---
id: computing-software.cloud-infrastructure-engineering.k3s.k3s-join-agent-node
name: k3s-join-agent-node
category: computing-software
field: cloud-infrastructure-engineering
product: k3s
tags: [k3s, agent, k3s-url, k3s-token]
level: intro
status: docs-checked
description: "Join an agent node to a K3s server using K3S_URL and K3S_TOKEN with the install script."
sources:
  - https://docs.k3s.io/quick-start
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: add a worker (agent) node to an existing K3s server.

Run on the new machine:

```
curl -sfL https://get.k3s.io | K3S_URL=https://myserver:6443 K3S_TOKEN=mynodetoken sh -
```

Setting K3S_URL makes the installer configure K3s as an agent instead of a server; the agent registers with the server listening at that URL. Setting K3S_URL without explicitly choosing an exec command defaults the command to agent, and when running the agent K3S_TOKEN must also be set.

The value for K3S_TOKEN is stored on the server node at:

```
/var/lib/rancher/k3s/server/node-token
```

The agent service is named k3s-agent by default (INSTALL_K3S_NAME).

Environment variables beginning with K3S_ are preserved for the systemd and openrc services to use.

Failure mode: every machine must have a unique hostname. If hostnames are not unique, set K3S_NODE_NAME to a valid unique hostname for each node.

Version skew: the Kubernetes version skew policy applies.

Verify: run `kubectl get nodes` on a server and confirm the agent appears.

## Checked

2026-11-03: read docs.k3s.io quick-start (and reference/env-variables). Confirmed: the K3S_URL/K3S_TOKEN join command, the node-token path, agent defaulting, K3S_ variable preservation and the unique hostname rule. Removed: stop commands, the agent uninstall script path and the server-newer-than-agent skew statement, none of which a fetched page states.

Method: documentation only; no commands were run.
