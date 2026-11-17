---
id: computing-software.cloud-infrastructure-engineering.portainer.install-classic-portainer-agent-on-docker
name: install-classic-portainer-agent-on-docker
category: computing-software
field: cloud-infrastructure-engineering
product: portainer
tags: [agent, docker-standalone, port-9001, agent-secret]
level: practitioner
status: docs-checked
description: "Connect a Docker Standalone host with the classic Portainer Agent, including port 9001, AGENT_SECRET and why it is a legacy option."
sources:
  - https://github.com/portainer/portainer-docs/blob/HEAD/2.39-lts/admin/environments/add/docker/agent.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The classic Agent on Docker Standalone is a legacy option: it supports neither edge features nor policy management, and the docs recommend the Edge Agent for most use cases.

Requirements beyond the generic Docker ones: port 9001 on the host must be reachable from the Portainer Server (if not, use the Edge Agent). On Windows you need WSL (WSL2 for new installs) or Windows Container Services. The Agent reaches Docker over the Unix socket (named pipe on WCS), never TCP. On Linux SELinux must be off, or deploy with `--privileged`.

If you set a custom `AGENT_SECRET` on the Server, give the Agent the same value as an environment variable at deploy time, for example `-e AGENT_SECRET=yoursecret`.

In the UI: expand Environment-related, click Environments, Add environment, choose Docker Standalone, Start Wizard, then under More options pick Agent and your platform. Copy the generated command (the Linux and Windows WSL variant, or the WCS variant) and run it on the target Docker host, then complete the wizard form to register it.

## Checked

2026-11-04. Checked against the Portainer 2.39 LTS documentation pages in `sources` (portainer-docs on GitHub, fetched this batch): commands, flags, ports, paths, defaults and UI steps. No wrong claims found; nothing removed.

Method: documentation only; no commands were run.
