---
id: computing-software.cloud-infrastructure-engineering.portainer.portainer-server-and-agent-architecture
name: portainer-server-and-agent-architecture
category: computing-software
field: cloud-infrastructure-engineering
product: portainer
tags: [architecture, server, agent, edge-agent, air-gapped]
level: intro
status: docs-checked
description: "Explain how Portainer Server and Agent fit together, why one server manages many clusters, and why the Edge Agent is preferred over the classic Agent."
sources:
  - https://github.com/portainer/portainer-docs/blob/HEAD/2.39-lts/start/architecture.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Portainer has two components, the Portainer Server and the Portainer Agent, both lightweight containers on your existing infrastructure. Deploy an Agent to each node in a cluster and point it back at the Server.

One Server accepts connections from any number of Agents, so you manage several clusters from a single interface. The Server container needs data persistence because it holds the state; Agents are stateless and ship their data back to it.

Running multiple Server instances against the same clusters is not supported. Run the Server on a specific management node and deploy Agents on the rest.

Agent versus Edge Agent: the docs recommend the Edge Agent in most cases. With the classic Agent the Server connects out to each environment (Server to Agent), so every environment must be reachable on the Server's network. With the Edge Agent the environment connects back to the Server over an encrypted TLS tunnel, so only the Server needs to be reachable. This matters for internet-connected or firewalled sites. The classic Agent remains for legacy and local-network use, and features such as Fleet Governance Policies are not available with it.

Portainer runs only on your own servers behind your own firewalls, and it works fully air-gapped. Because Portainer does not host your infrastructure, it holds no SOC or PCI/DSS compliance of its own.

## Checked

2026-11-04. Checked against the Portainer 2.39 LTS documentation pages in `sources` (portainer-docs on GitHub, fetched this batch): commands, flags, ports, paths, defaults and UI steps. Corrected the per-node Agent guidance to match the page.

Method: documentation only; no commands were run.
