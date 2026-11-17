---
id: computing-software.cloud-infrastructure-engineering.portainer.edge-agent-standard-vs-async
name: edge-agent-standard-vs-async
category: computing-software
field: cloud-infrastructure-engineering
product: portainer
tags: [edge-agent, standard-mode, async-mode, tunnel, edge-insecure-poll]
level: practitioner
status: docs-checked
description: "Choose between Edge Agent Standard and Async, which ports each needs open on the Server, and when to set EDGE_INSECURE_POLL."
sources:
  - https://github.com/portainer/portainer-docs/blob/HEAD/2.39-lts/admin/environments/add/docker/edge.md
  - https://github.com/portainer/portainer-docs/blob/HEAD/2.39-lts/admin/environments/add/docker/edge-async.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The Edge Agent lets you manage an environment the Server cannot reach: the agent connects out, so no inbound ports are opened at the environment.

Standard mode establishes an on-demand TLS tunnel from the agent to the Server, so you interact with the environment in real time. It needs two Server ports reachable: the UI port (9443, or 30779 on Kubernetes NodePort) and the tunnel port (8000, or 30776).

Async mode has no tunnel. Instead you browse snapshots of the remote environment, captured recently and sent to the Server, and you can use a snapshot to perform actions. It uses very little data, so it suits limited or intermittent links and capped mobile connections. It needs only the UI port. Async is Business Edition only.

If the Server uses TLS the agent polls over HTTPS. If the Server has a self-signed certificate, deploy the Edge Agent with `-e EDGE_INSECURE_POLL=1`, otherwise it cannot communicate with the Server.

To add one: Environment-related, Environments, Add environment, pick the platform, Start Wizard, then choose Edge Agent Standard or Async and fill the form; the wizard generates the deploy command.

## Checked

2026-11-04. Checked against the Portainer 2.39 LTS documentation pages in `sources` (portainer-docs on GitHub, fetched this batch): commands, flags, ports, paths, defaults and UI steps. No wrong claims found; nothing removed.

Method: documentation only; no commands were run.
