---
id: computing-software.cloud-infrastructure-engineering.portainer.deploy-portainer-on-docker-swarm
name: deploy-portainer-on-docker-swarm
category: computing-software
field: cloud-infrastructure-engineering
product: portainer
tags: [install, docker-swarm, agent, stack, manager-node]
level: practitioner
status: docs-checked
description: "Deploy Portainer Server and global Agent onto a Docker Swarm with the agent stack manifest, and avoid the mistakes that inflate node counts."
sources:
  - https://github.com/portainer/portainer-docs/blob/HEAD/2.39-lts/start/install/server/swarm/linux.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Requirements: Swarm mode enabled with the overlay network working, sudo on a manager node, UI port 9443, optional tunnel port 8000 for Edge, and port 9001 open between manager and worker nodes for the Agent. Docker must be reached over the Unix socket; TCP is not supported in Swarm. SELinux should be off and Docker running as root.

Fetch the stack manifest and deploy it once, from a manager node:

```
curl -L https://downloads.portainer.io/ee-lts/portainer-agent-stack.yml -o portainer-agent-stack.yml
docker stack deploy -c portainer-agent-stack.yml portainer
```

The manifest deploys a single Portainer Server instance and the Portainer Agent as a global service on every node. Do this only once per cluster. You do not add each node as its own environment; doing so consumes more of your licensed node count than expected.

The instructions assume a single manager node. With more than one manager, read the FAQ on retaining Portainer's configuration first, because the Server data must live somewhere that survives rescheduling. If nodes communicate by DNS names, those records must resolve across the whole cluster.

## Checked

2026-11-04. Checked against the Portainer 2.39 LTS documentation pages in `sources` (portainer-docs on GitHub, fetched this batch): commands, flags, ports, paths, defaults and UI steps. No wrong claims found; nothing removed.

Method: documentation only; no commands were run.
